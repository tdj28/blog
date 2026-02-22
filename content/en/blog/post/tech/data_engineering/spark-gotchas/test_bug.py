from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

spark = SparkSession.builder.master("local[1]").appName("ast-gotcha").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("id", StringType(), False),  # root identifier
    StructField("timestamp", TimestampType(), True),
    StructField("payload", StructType([
        StructField("id", StringType(), False),  # inner identifier
        StructField("value", StringType(), True),
    ]), True),
])

df = spark.createDataFrame(
    [("root-100", None, ("inner-200", "data"))],
    schema=schema,
)

def flatten_and_audit(frame):
    meta_cols = {"id", "timestamp"}
    payload_fields = [f.name for f in frame.schema["payload"].dataType.fields]

    frame = frame.withColumn("_audit", F.struct(*[F.col(c) for c in sorted(meta_cols)]))
    for name in payload_fields:
        frame = frame.withColumn(name, F.col(f"payload.{name}"))
        
    print("=== EXPLAIN PLAN BEFORE DROP ===")
    frame.explain(extended=True)

    frame = frame.drop(*list(meta_cols), "payload")

    return frame

out = flatten_and_audit(df)
print("=== FINAL EXPLAIN PLAN ===")
out.explain(extended=True)
print("=== ACTUAL OUTPUT ===")
out.show(truncate=False)
