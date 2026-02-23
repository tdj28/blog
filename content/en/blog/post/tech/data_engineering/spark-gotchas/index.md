---
title: "Nominal vs Referential Column Identity in Spark: The Shadowing Hazard"
date: 2026-02-22
draft: false
authors: ["t-jones", "gemini-3-pro"]
comments: true
showMath: true
summary: "An analysis of a common PySpark pitfall where mixing expression-based attribute identity and name-based pruning leads to unexpected data loss."
tags:
  - spark
  - architecture
  - compiler-design
  - debugging
categories:
  - computer-science
  - data-engineering
toc: true
---

{{< alert "circle-info" >}}
Creation of this blog post was driven by the
human author who has many years of experience
in education. AI tooling was used to accelerate
content creation and peer review the
accuracy of the content.
{{< /alert >}}

A common debugging scenario in PySpark occurs when applying a sequence of seemingly straightforward DataFrame transformations results in missing columns. The code executes without stack traces or memory issues, but the output schema is suddenly missing critical identifiers.

This failure mode is often misdiagnosed as a bug in Spark's Catalyst optimizer. In reality, Catalyst is behaving exactly as designed. The programmer's intent diverges from the program's actual semantics because the DataFrame API mixes two different notions of identity: referential attribute identity (internal `ExprId` tracking) and surface-level syntax (nominal name-based pruning). 

This post examines a specific name-shadowing pitfall common in data pipelines, provides a formal model of Spark's dual identity systems, and demonstrates how to align your PySpark code with the compiler's actual execution model.

---

## 1. The Core Hazard: Referential Capture vs Nominal Pruning

The shadowing hazard typically manifests when attempting to flatten nested structures (like a Change Data Capture JSON payload) into a root namespace while preserving root metadata.

Consider an event envelope containing a root `id` (Kafka event UUID) and a nested `payload` containing its own inner `id` (database entity UUID). If we capture the root `id` into an audit struct, promote the nested `payload.id` to the root layer, and then execute a nominal clean-up layer via `drop("id")`, we execute a schema-valid transformation that can evade tests unless you explicitly assert key presence: the flattened inner ID disappears entirely, yet the nested audit ID survives because it captured the earlier binding.

The following minimal PySpark snippet demonstrates this collision:

{{% tabs "spark-buggy" %}}
{{% tab "Python (PySpark)" %}}
```python
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# The existence of ExprId-based identity and nominal APIs is stable across Spark 3.x/4.x.
# Specific optimizer rules and plan shapes may vary slightly.
print(f"PySpark Version: {pyspark.__version__}")

spark = SparkSession.builder.master("local[1]").appName("plan-gotcha").getOrCreate()

# 1. Incoming Event Stream
events = spark.createDataFrame(
    [("event-100", ("entity-200", "data"))],
    "id string, payload struct<id:string, value:string>"
)

# Phase 1: Capture (Referential)
# We capture the root 'id' into an _audit struct. 
# This binds to the exact ExprId of the root column.
out = events.withColumn("_audit", F.struct("id"))

# Phase 2: Substitute / Shadow
# We unpack the nested payload 'id' to the root level.
out = out.withColumn("id", F.col("payload.id"))

# Phase 3: Nominally Prune
# We attempt to clean up our namespace using a string literal drop.
out = out.drop("id", "payload")

# 4. Falsifiable Paradox Output
print("\nParadoxical Schema:")
print("Audit Struct captured Root:", out.select(F.col("_audit.id")).first()[0])
print("Remaining Level Columns:", out.columns)

# If downstream operations attempt to utilize the promoted 'id', they fail loudly.
# out.select("id").show() # AnalysisException: [UNRESOLVED_COLUMN]

# For deep Catalyst JVM plan introspection (Classic Spark only):
# print(out._jdf.queryExecution().analyzed().toString())
# For portable environment inspection (Classic + Connect):
print("\nAnalyzed Logical Plan:")
out.explain(mode="extended")

spark.stop()
```
{{% /tab %}}
{{% /tabs %}}

### The Mental Model

Before looking at the plan execution, remember this rule of thumb:
* **Names are labels.**
* Catalyst binds expressions to an `ExprId` once resolved.
* Some APIs (notably `drop(String)`) operate strictly on labels, not identities.
* **So if you rebind a label and then run a label-based prune, you prune the new binding.**

### The Output Paradox

Running the script forces the contradiction into the console directly:

```text
Paradoxical Schema:
Audit Struct captured Root: event-100
Remaining Level Columns: ['_audit']

== Parsed Logical Plan ==
...
== Analyzed Logical Plan ==
_audit: struct<id:string>
Project [_audit#4]
+- Project [payload#1.id AS id#8, payload#1, _audit#4]
   +- Project [id#0, payload#1, struct(id, id#0) AS _audit#4]
      +- LogicalRDD [id#0, payload#1], false
```

The promoted inner identifier was dropped entirely, yet the `_audit` struct seamlessly retained its value. To understand how exactly these operators behave, we formalize Spark's execution pipeline.

---

## 2. Spark's Identity Mechanics

In Spark SQL, a DataFrame represents an unevaluated **logical plan tree** of relational operators. Catalyst runs optimization rule batches to a fixpoint over these trees <a id="cite-armbrust"></a>[[Armbrust et al., 2015]](#ref-armbrust). But the core failure here requires no complex structural optimization—it stems purely from attribute name rebinding across projections combined with a nominal string-based drop.

When analyzing column references, Spark differentiates attributes not by their lexical name string, but by an internal `ExprId`.

### `ExprId`: Spark's Internal Attribute Identity

While Spark does not natively implement a pure hygienic calculus (as many surface-level operations remain nominal by design), `ExprId` provides the underlying referential identity for attributes inside the plan, separating it from the string name.

Per Catalyst source code, `ExprId` is a Scala case class pairing an `id: Long` and a `jvmId: UUID` <a id="cite-named-expressions"></a>[[namedExpressions.scala]](#ref-named-expressions).

* The `Long` acts as an identifier that is unique within a single JVM. In the Catalyst implementation, this is generated by `NamedExpression.newExprId`, which draws from an `AtomicLong`.
* The `jvmId` acts as a per-process salt for the `Long`. Crucially, it participates in equality semantics whenever attributes are compared (e.g., `sameRef` checks `this.exprId == other.exprId`).

`AttributeReference` equality and `<expr>.sameRef` mechanics internally compare this `exprId` instead of the string token. When you write `F.col("id")`, you create an `UnresolvedAttribute("id")`. During analysis, Catalyst's resolver binds this lexical string to the matching output, yielding an `AttributeReference("id")(exprId = α)`.

Likewise, when you invoke `withColumn("id", ...)`, Catalyst maps the incoming evaluation into an `Alias(..., "id")`. Because `Alias` inherits from `NamedExpression`, instantiation executes `NamedExpression.newExprId`, granting the alias an entirely fresh `ExprId`. 

**Note on "Overwriting" bindings:** It is misleading to say `withColumn` "overwrites the underlying ExprId." Rather, it introduces a *new binding* for the same surface name. The previous `id` attribute still exists in the child plan, but it is no longer projected in the output attribute list of the new `Project` node <a id="cite-withcolumn"></a>[[withColumn docs]](#ref-withcolumn).

### Nominal Name Semantics and the Resolver

In contrast, some dataframe methods operate nominally, filtering directly on the surface-level string. Importantly, they do not default to raw `==` string equality; they use the active configuration's name resolver (respecting properties like `spark.sql.caseSensitive`).

As explicitly defined in Catalyst's `Dataset.scala`, calling the string-literal overload `drop(*colNames: String)` invokes Spark's name resolver (`sparkSession.sessionState.analyzer.resolver`) against the target's analyzed output. It computes a `remainingCols` list and invokes `select(remainingCols: _*)`, explicitly constructing a new projection that excludes the matches <a id="cite-dataset-scala"></a>[[Dataset.scala]](#ref-dataset-scala).

**The "Early Analysis" Compiler Gotcha:** Crucially, `drop(String)` consults the analyzed output to compute the remaining projection, which can force analysis earlier than you might expect in code that assumed resolution would only happen at the first action.

---

## 3. Formal Two-Level Identity Model

We can formalize the two identities as disjoint equivalence relations over a sequence of attributes $\mathcal{O}$ where $a = (\text{name}, \text{exprId}, \tau)$.

1. **Referential Equivalence ($\equiv_r$)**: $a \equiv_r b \iff a.\text{exprId} = b.\text{exprId}$
2. **Nominal Equivalence ($\equiv_n$)**: $a \equiv_n b \iff \text{resolver}(a.\text{name}, b.\text{name})$

Let us formally model the logical objects Spark manipulates:
* A projection list `Project(projectList, child)` dictates the output attributes.
* A substitution operator $S$ introduces a `NamedExpression` like `Alias(expr, "id")(exprId = \beta)` into the `projectList`.
* A nominal filter $D_s$ computes `remaining = [a in projectList : not resolver(a.name, s)]` and applies `Project(remaining, child)`.

### Theorem: Non-Commutation of Identity Systems

Spark's reference mechanics preserve identity ($\equiv_r$) exactly, but API manipulations on strings dictate evaluation bounds via $\equiv_n$. Because these operators are anchored to orthogonal relations, they do not commute.

*Proposition:* If $S$ is a substitution operation injecting a new `Alias` bridging a namespace (e.g., executing `withColumn` to promote nested payload fields), and $D_{\text{s}}$ is the nominal `drop` filter evaluating strings, their composition is algebraically order-dependent:
$$
D_{\text{s}} \circ S \neq S \circ D_{\text{s}}
$$

*Proof:* Given a `Project` list where $S$ has introduced the new binding $a_{\text{inner}} = \text{Alias}(\dots, \text{"id"})(\text{exprId}=\beta)$, the subsequent string-literal evaluation $D_{\text{id}}$ tests against the $\equiv_n$ nominal projection rule. It drops $a_{\text{inner}}$ identically to any other attribute cleanly resolving to `"id"`, ruthlessly ignoring the underlying `ExprId`. Reversing the functional application executes the drop filter on the initial schema output, completely sparing the subsequent substitution layer. 

### The Hazard Mapped to the Plan Delta

Tracing our earlier PySpark collision script through this equivalence model identically matches the extracted Analyzed Logical Plan:

1. **Phase 1 Capture ($before$):** `_audit` references `id#0`. `Project [id#0, payload#1, struct(id, id#0) AS _audit#4]` 
2. **Phase 2 Substitution ($after shadowing$):** Output has the new Alias `id#8` plus the struct `_audit#4`(which still relies on `id#0` behind the scenes). The original `id#0` surface binding is unreachable from the new output schema.
3. **Phase 3 Elimination ($after drop$):** `Project [_audit#4]`. The final `Project` nominally filtered `id#8` from the output list completely because it resolved to `"id"`. The `_audit#4` struct seamlessly unpacks because its sub-field structurally carries the original `ExprId` reference inward.

---

## 4. The Second Hazard: Silent Semantic Drift

Even if you don't nominally drop the shadowed column, rebinding names without preserving semantic intent exposes pipelines to catastrophic logic drift.

The true insidious failure mode isn't a missing column throwing an obvious `AnalysisException` downstream. It's when a schema-valid transformation evades tests (because the key exists) but subsequent valid-but-wrong downstream operations execute against degraded domains.

If a collision silently replaces a primary dimension key, downstream processes will blindly utilize the new semantic domain (the entity UUID) instead of the original domain (the event UUID). No errors are thrown, but entirely valid records disappear.

The following CDC snippet demonstrates deductive failure by comparing the correct Event deduplication baseline against the shadowed Entity output:

```python
# 1. Incoming Event Stream
# Events 1 and 2 possess different Event UUIDs, 
# but they represent modifications to the *same* inner Entity UUID.
events = spark.createDataFrame(
    [
        ("event-100", ("entity-999", "status_created"), "2026-01-01 10:00:00"),
        ("event-101", ("entity-999", "status_updated"), "2026-01-01 10:05:00")
    ],
    "id string, payload struct<id:string, value:string>, ts string"
).withColumn("ts", F.to_timestamp("ts"))

# 2. Baseline latest-per-event window: Keying safely on the original Event ID keeps BOTH events.
# (Each event ID is unique, so each partition has size 1, retaining all records).
from pyspark.sql.window import Window
w_baseline = Window.partitionBy("id").orderBy(F.col("ts").desc())
baseline_dedup = events.withColumn("rn", F.row_number().over(w_baseline)) \
                       .filter("rn = 1").drop("rn")

print("\nBaseline Window (Correct - both events retained):")
baseline_dedup.select("id", "payload.value").show()
```

```text
Baseline Window (Correct - both events retained):
+---------+--------------+
|       id|         value|
+---------+--------------+
|event-100|status_created|
|event-101|status_updated|
+---------+--------------+
```

Now, watch what happens when we flatten the payload exactly as an unsuspecting developer might:

```python
# 3. Flawed flattening: Developer unpacks payload fields.
# The Event UUIDs are silently shielded.
out = events.withColumn("id", F.col("payload.id")) \
            .withColumn("value", F.col("payload.value")) \
            .drop("payload")

# 4. Drifted latest-per-entity window: Operates on Entity ID!
w_drift = Window.partitionBy("id").orderBy(F.col("ts").desc())
drifted_dedup = out.withColumn("rn", F.row_number().over(w_drift)) \
                   .filter("rn = 1").drop("rn")

print("\nSilent Logic Failure (Valid state dropped!):")
drifted_dedup.select("id", "value").show()
```

```text
Silent Logic Failure (Valid state dropped!):
+----------+--------------+
|        id|         value|
+----------+--------------+
|entity-999|status_updated|
+----------+--------------+
```

By accidentally operating on `entity-999` rather than the distinct `event-100` and `event-101`, the deduplicator silently drops the `status_created` event entirely, believing it was merely processing duplicates.

---

## 5. Safe Fix Patterns at Scale

To protect pipelines universally—beyond just being "careful"—adopt Mechanical compiler-esque guardrails:

### A. Treat Flattening as a Projection (Not Iterative Rebinding)

The cleanest fix is avoiding collisions entirely by constructing a unified projection. Iterative `withColumn` invocations are physically nested `Project` operators prone to name clashes.

```python
# Single projection. No intermediate shadowed state, no collision.
safe_out = events.select(
    F.col("id").alias("event_id"),
    F.col("payload.id").alias("entity_id"),
    F.col("payload.value").alias("value"),
    F.struct("id").alias("_audit") # Optional: retain original struct
)
```

### B. Drop Before Shadow

If you absolutely must use iterative `withColumn` mutations in a loop, drop the root attributes *before* introducing the new shadowed identifiers into the namespace. Note the assignment to `tmp` to align with functional programming mindsets and explicitly prevent accidental re-use of mixed plans:

```python
# Drop the root `id` BEFORE promoting the nested payload fields.
tmp = events.withColumn("_audit", F.struct("id")).drop("id")

for field in ["id", "value"]:
    tmp = tmp.withColumn(field, F.col(f"payload.{field}"))

tmp = tmp.drop("payload") # Finish cleanup
```

While this prevents the immediate `drop` bug, it does not prevent semantic drift if a developer later forgets what `id` means. Prefer renaming promoted identifiers (e.g., `entity_id`) entirely instead of reusing ambiguous names.

### C. Enforce Contract Mechanics (CI Pipelines)

Never promote nested fields into the root namespace without an enforced renaming convention. `event_id` and `entity_id` mapping should be mechanically validated. Encode this contract locally into your validation framework and unit tests:

```python
# 1. Pipeline assert protecting against semantic drift and missing columns:
assert "entity_id" in df.columns and "event_id" in df.columns, "Ambiguous identifier risk: Component IDs must be uniquely qualified."

# 2. Aggressive overarching invariant for broad architectures:
assert len(df.columns) == len(set(df.columns)), "Pipeline collision detected."

# 3. Forbid raw 'id' to prevent ambiguous joins downstream:
assert "id" not in df.columns, "Raw 'id' column found. Must be renamed to event_id or entity_id."
```

---

## 6. The Architecture of `drop(Column)` vs `drop(String)`

The `DataFrame.drop` documentation defines a crisp contractual split <a id="cite-dataset-api"></a>[[PySpark drop Docs]](#ref-dataset-api):
* If the input is a **String**, Spark computes nominally via the resolver, builds a selection map, and executes a `Project`. As noted earlier, this explicitly forces plan analysis.
* If the input is a **Column**, Spark applies a fundamentally different structural methodology based on referential matching. 

Internally within the Scala API, invoking `drop(cols: Column*)` injects a `DataFrameDropColumns(dropList, logicalPlan)` logical node. 

The analyzer delegates resolution via the dedicated `ResolveDataFrameDropColumns` rule <a id="cite-drop-columns"></a>[[ResolveDataFrameDropColumns.scala]](#ref-drop-columns). This logic resolves expressions post-hoc and rewrites the node into a `Project` output relying expressly on `semanticEquals`. The rule explicitly notes that it *allows and ignores non-existing columns*. 

Because `drop(Column)` is resolved via analyzer rules and expression semantics (`semanticEquals` referencing resolved attributes), it tends to remove a specific resolved attribute rather than all same-named columns. Ambiguity is naturally surfaced as an analysis error instead of silently bleeding through. 

It is important to note that this is safer, but it evaluates based on expression matching, not a guaranteed single `ExprId` deletion in every contrived physical plan. If multiple outputs are genuinely semantically equal, they might all be dropped. Still, it is mathematically safer when operating amidst highly layered schema evolution.

```python
# Self-joins can trigger ambiguity checks; aliasing and qualified references avoid that. 
# The config below exists for legacy fallback behavior.
# spark.sql.analyzer.failAmbiguousSelfJoin = False
l = df1.alias("l")
r = df2.alias("r")
j = l.join(r, F.col("l.name") == F.col("r.name"))

# Lexical evaluation: Drops BOTH 'name' columns unconditionally
j.drop("name") 

# Expression evaluation loosely attempting resolution: Throws an ambiguous reference AnalysisException!
j.drop(F.col("name")) 

# Expression evaluation strictly utilizing the correctly aliased left-side wrapper: Succeeds
j.drop(l["name"]) 
```

---

## Appendix: Other Noteworthy Catalyst Landmines

### Identifiers Are Not Paths

Because DataFrames frequently deal with nested JSON-like structs, developers often conflate identifiers with paths. 

Spark distinguishes identifiers from paths. If you create a dataframe with a column containing a literal dot `df.withColumn("a.b", ...)`:
`drop("a.b")` treats the input as a string literal and deletes the top-level column literally named `a.b`. It does **not** navigate into a struct `a` to drop field `b`. This is another manifestation of surface syntax operating differently from the underlying mathematical structure.

### The Analysis Overhead of Iterative `withColumn`

A loop calling `withColumn` iteratively is convenient, but each execution nests a new `Project` node in the DataFrame plan tree. Analysis time grows roughly linearly with the number of Project nodes. For schemas containing hundreds of columns, this creates a deeply nested tree that adds marked overhead to the query planner or can even trigger JVM stack limits. Evaluate multiple projections simultaneously via `df.select()` or `df.withColumns()` <a id="cite-withcolumns"></a>[[withColumns docs]](#ref-withcolumns) instead.

### Python UDF Serializations

Python UDFs are notoriously expensive computational boundaries. Executing custom Python functions requires serializing data out of the JVM and Spark's native columnar memory formats, transporting it to a Python worker, executing it via CPython, and serializing it back. While standard built-ins execute entirely within Catalyst and Tungsten, custom UDF logic incurs substantial I/O cost. Vectorized Pandas UDFs optimize this by processing columnar batches (via Apache Arrow) reducing the per-row overhead, though data movement itself remains a bottleneck that scales with data volume.

### The Nuance of `monotonically_increasing_id`

The `monotonically_increasing_id` function provides unique 64-bit integer values, but comes with critical caveats. The generated values are **not sequential** and provide **no guarantees of chronological or ordinal state**. 

According to the Spark docs <a id="cite-monotonic"></a>[[monotonically_increasing_id docs]](#ref-monotonic), the IDs are split: the upper 31 bits represent the partition ID, and the lower 33 bits are the record number within that partition. This makes the function explicitly **nondeterministic**, as its output relies heavily on partition IDs and task layout. It guarantees uniqueness, but not tight numbering or stability between jobs.

---

## References

*Note: Citations are formally pinned to v3.5.1 strictly for durable, permanent repository context and line anchoring. Behavior matches functionally across the 3.4/3.5 generational branch.*

- **<a id="ref-armbrust"></a>[Armbrust et al., 2015]** Spark SQL: Relational Data Processing in Spark. Foundation paper establishing Catalyst tree execution and logical node optimization. [SIGMOD 2015](https://dl.acm.org/doi/10.1145/2723372.2742797) [↩](#cite-armbrust)
- **<a id="ref-dataset-scala"></a>[Dataset.scala]** Definition of `dataset.drop(String)` computing matches via SessionState resolver and dynamically building `select(remainingCols)`. apache/spark. [GitHub Source (v3.5.1)](https://raw.githubusercontent.com/apache/spark/v3.5.1/sql/core/src/main/scala/org/apache/spark/sql/Dataset.scala) [↩](#cite-dataset-scala)
- **<a id="ref-drop-columns"></a>[ResolveDataFrameDropColumns.scala]** Definition of the explicit rewriting of `DataFrameDropColumns` utilizing `semanticEquals`. apache/spark. [GitHub Source (v3.5.1)](https://raw.githubusercontent.com/apache/spark/v3.5.1/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/analysis/ResolveDataFrameDropColumns.scala) [↩](#cite-drop-columns)
- **<a id="ref-named-expressions"></a>[namedExpressions.scala]** Definition of `ExprId` structural case class. apache/spark. [GitHub Source (v3.5.1)](https://raw.githubusercontent.com/apache/spark/v3.5.1/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/namedExpressions.scala) [↩](#cite-named-expressions)
- **<a id="ref-dataset-api"></a>[PySpark drop Docs]** Documentation of `drop(string)` vs `drop(Column)` logic splits over string versus expression matches. Apache Spark. [PySpark API Docs](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.drop.html) [↩](#cite-dataset-api)
- **<a id="ref-rule-executor"></a>[RuleExecutor.scala]** Definition of the Fixed-Point rule execution strategy. apache/spark. [GitHub Source (v3.5.1)](https://raw.githubusercontent.com/apache/spark/v3.5.1/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/rules/RuleExecutor.scala) [↩](#cite-rule-executor)
- **<a id="ref-withcolumn"></a>[PySpark withColumn]** Documentation of `withColumn` showing strict replacement mechanics. Apache Spark. [PySpark API Docs](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.withColumn.html) [↩](#cite-withcolumn)
- **<a id="ref-withcolumns"></a>[withColumns]** Documentation for multi-column `withColumns`. Apache Spark. [PySpark Docs](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.withColumns.html) [↩](#cite-withcolumns)
- **<a id="ref-monotonic"></a>[monotonically_increasing_id]** PySpark Documentation on monotonic IDs, bit layout, and nondeterminism. Apache Spark. [PySpark Docs](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.monotonically_increasing_id.html) [↩](#cite-monotonic)
