---
title: "Searching Without Being Searched: The Architecture of Oblivious Prefix Trees"
date: 2026-02-17
draft: false
authors: ["t-jones", "gemini-3-pro"]
comments: true
showMath: true
summary: "A rigorous analysis of Prefix Trees (Tries) and Radix Trees, evolving from memory hierarchy constraints to cryptographically secure Data-Oblivious architectures."
tags:
  - algorithms
  - data-structures
  - tries
  - string-search
  - security
  - privacy
  - oram
categories:
  - computer-science
  - algorithms
toc: true
---

{{< alert "circle-info" >}}
Creation of this blog post was driven by the
human author who has many years of experience
in education. AI tooling was used to accelerate
content creation and peer review the
accuracy of the content.
{{< /alert >}}

Imagine querying a massive, highly sensitive database, such as a national genetic registry or a financial ledger hosted on **an AWS GovCloud**. You encrypt your query. The database is loaded into a Trusted Execution Environment (TEE) like Intel SGX, designed to radically shrink the "Trusted Computing Base" (TCB), (meaning you no longer have to trust the cloud provider, the host operating system, or the hypervisor), and protect memory contents from being read by the host. You execute the search. You think you're secure.

But you're not.

While TEEs protect against **privileged software attackers** (like a compromised hypervisor monitoring page faults or cache behavior) reading plaintext memory, they do not inherently defend against **physical attackers** probing the hardware. As the CPU processes your query, the motherboard's memory bus lights up. A physical attacker monitoring the memory address trace on the bus can track exactly which nodes in the index were accessed. By recording this memory trace and executing an **access pattern side-channel attack**, they can often fully reconstruct your query without ever breaking the cryptography. 

To achieve true, zero-trust search capabilities on public infrastructure, we cannot merely encrypt the data; we must continuously and dynamically shuffle the structure itself during traversal, rendering the sequence of memory accesses **computationally indistinguishable** from random noise. This is the domain of **Oblivious RAM (ORAM)** and **Data-Oblivious Data Structures**.

But before we can build an Oblivious Trie capable of hiding from the physical server hardware itself, we first need to master the topological foundations that make prefix searching possible at scale.

## Why Tries?

When we think of searching for data, we often default to the **Hash Map** ($O(1)$ average case) or the **Binary Search Tree** ($O(\log N)$). These are general-purpose tools that treat keys as opaque objects: black boxes that can only be compared or hashed.

However, when our keys are **strings** (and specifically when we care about the *structure* of those strings, like prefixes in autocomplete or subnet masks in IP routing), general-purpose tools reveal their theoretical limits.

*   **Hash Maps**: Excellent for exact matches (`"cat"` == `"cat"`), but natively lack structural awareness. To find all strings starting with "ca", one must scan the entire keyspace $\Omega(N)$, *unless* the system artificially pre-hashes and stores every possible prefix during insertion (costing massive $O(L)$ storage per key).
*   **Binary Search Trees**: Comparing two strings $A$ and $B$ is not an $O(1)$ operation; it is bounded by their longest common prefix. The comparison cost is $O(\operatorname{LCP}(A, B) + 1)$. Thus, a BST lookup is not strictly $O(\log N)$, but effectively $O(L \cdot \log N)$, where $L$ is the string length.

To understand when to use what architecture, consider this high-level decision map:

{{< mermaid >}}
flowchart TD
  Q["What queries do you need?"] --> E["Exact match only"]
  Q --> P["Prefix / range / ordered"]
  E --> H["Hash map / HAMT"]
  P --> PRIV["Is query privacy critical?"]
  PRIV -->|Yes| OT["Oblivious Trie (ORAM)"]
  PRIV -->|No| O["Ordered access needed?"]
  O --> Y["Yes"] --> T["Trie / Radix / ART / String B-tree"]
  O --> N["No"] --> F["Bloom/SuRF filter + backing store"]

  T --> M["In-memory?"]
  M --> IM["Yes"] --> ART["ART / HAT-trie / burst trie"]
  M --> DK["No (disk/SSD)"] --> SBT["String B-tree / SP-GiST / page-grouped tries"]
{{< /mermaid >}}

Enter the **Prefix Tree**, or **Trie** (derived from *re**trie**val* <a id="cite-fredkin-1960"></a>[[fredkin-1960]](#ref-fredkin-1960)). It is a tree data structure that decomposes the key itself to structurally guide the search, shifting the complexity paradigm from **comparison-based** to **digital** (in the bit-wise sense) search.

{{< alert title="Pronunciation" color="info" >}}
Although Edward Fredkin originally intended for the term to be pronounced exactly like "tree" (derived from re**trie**val), the computer science community overwhelmingly pronounces it as "**try**" (rhyming with "pie") to auditorily distinguish the specific structure from a standard search "tree" during spoken conversation.
{{< /alert >}}

Let's look at a Trie containing the words: **"to", "tea", "ted", "ten", "A", "i", "in", "inn"**.

{{< mermaid >}}
graph TD
    Root((ROOT))
    
    Root --> T(t)
    Root --> A_node(A)
    Root --> I_node(i)
    
    T --> To(o)
    T --> Te(e)
    
    Te --> Tea(a)
    Te --> Ted(d)
    Te --> Ten(n)
    
    I_node --> In_node(n)
    In_node --> Inn_node(n)
    
    %% Accept states (End of Word)
    style To fill:#f9f,stroke:#333,stroke-width:2px
    style Tea fill:#f9f,stroke:#333,stroke-width:2px
    style Ted fill:#f9f,stroke:#333,stroke-width:2px
    style Ten fill:#f9f,stroke:#333,stroke-width:2px
    style A_node fill:#f9f,stroke:#333,stroke-width:2px
    style I_node fill:#f9f,stroke:#333,stroke-width:2px
    style In_node fill:#f9f,stroke:#333,stroke-width:2px
    style Inn_node fill:#f9f,stroke:#333,stroke-width:2px
{{< /mermaid >}}

Nodes highlighted in **pink** are "accepting states" (IsTerminal = True). Notice that common prefixes are stored exactly once. The sequence `t` $\to$ `e` is shared by "tea", "ted", and "ten".

### Step-by-Step Construction

Tracing the insertion of the word **"tea"** into a Trie that already contains **"to"**:

{{< mermaid >}}
graph TD
    subgraph Step3["Step 3: Terminate"]
        R3((ROOT)) --> T3(t)
        T3 --> O3(o)
        T3 --> E3(e)
        E3 -- "Create 'a'" --> A3("a ✓")
        style O3 fill:#f9f,stroke:#333
        style A3 fill:#f9f,stroke:#333,stroke-width:2px
    end

    subgraph Step2["Step 2: Create Missing Branch"]
        R2((ROOT)) --> T2(t)
        T2 --> O2(o)
        T2 -- "No 'e' -> Create" --> E2("e")
        style O2 fill:#f9f,stroke:#333
        style E2 fill:#ccf,stroke:#333,stroke-width:2px
    end

    subgraph Step1["Step 1: Root Transition"]
        R1((ROOT)) -- "Has 't'?" --> T1(t)
        T1 --> O1(o)
        style O1 fill:#f9f,stroke:#333
        style T1 fill:#ccf,stroke:#333,stroke-width:2px
    end
{{< /mermaid >}}

1.  **Step 1**: We start at the Root. The first character is 't'. The edge exists, so we traverse it.
2.  **Step 2**: The next character is 'e'. The node 't' has a child 'o', but no 'e'. We **branch** here, creating a new node for 'e'.
3.  **Step 3**: The final character is 'a'. We create it and mark it as terminal.

## Baseline Trie Implementation

A Trie implementation can be broken down into three components: the node definition, the insertion logic, and the search/deletion logic.

### The Node Structure

Every node in a Trie must store two pieces of information:
1.  **Links to Children**: A mapping from the alphabet $\Sigma$ to child nodes.
2.  **State**: Whether the path ending at this node constitutes a valid key.

{{% tabs "trie-node" %}}
{{% tab "Python" %}}
```python
class TrieNode:
    def __init__(self):
        # We use a typed dictionary for O(1) average lookup.
        self.children: dict[str, 'TrieNode'] = {}
        # Marks the end of a valid key.
        self.is_end_of_word: bool = False
```
{{% /tab %}}
{{% tab "Go" %}}
```go
type TrieNode struct {
    // Common systems designs often choose bytewise tries (UTF-8) to keep |Σ|=256. 
    // This fixed array offers byte-oriented consistency.
    Children    [256]*TrieNode
    IsEndOfWord bool
}

func NewTrieNode() *TrieNode {
    return &TrieNode{}
}

type Trie struct {
    Root *TrieNode
}

func NewTrie() *Trie {
    return &Trie{Root: NewTrieNode()}
}
```
{{% /tab %}}
{{% tab "C++" %}}
```cpp
// A naive C++ node allocates on the heap per character which hurts locality.
// In production, use a chunked node pool to bypass native 'new' overhead.
struct TrieNode {
    std::unordered_map<char, TrieNode*> children;
    bool is_end_of_word = false;
};

// Chunk-Allocated Node Pool Pattern
#include <deque>

class TrieNodePool {
    // std::deque provides stable pointers and chunked allocation.
    std::deque<TrieNode> pool;
public:
    TrieNode* allocate() {
        pool.emplace_back();
        return &pool.back();
    }
};
```
{{% /tab %}}
{{% /tabs %}}

### Core Operations: Insertion

Insertion is a simple pointer-chasing traversal using the characters of the key as instructions. We create missing nodes on demand and flag the final node as a valid word.

{{% tabs "trie-insert" %}}
{{% tab "Python" %}}
```python
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
```
{{% /tab %}}
{{% tab "Go" %}}
```go
func (t *Trie) Insert(word string) {
    node := t.Root
    for i := 0; i < len(word); i++ {
        ch := word[i] // Byte indexing (bytewise UTF-8 traversal)
        if node.Children[ch] == nil {
            node.Children[ch] = NewTrieNode()
        }
        node = node.Children[ch]
    }
    node.IsEndOfWord = true
}
```
{{% /tab %}}
{{% tab "C++" %}}
```cpp
class Trie {
    TrieNodePool pool_;
    TrieNode* root_;
public:
    Trie() : root_(pool_.allocate()) {}

    void insert(const std::string& word) {
        TrieNode* node = root_;
        for (char ch : word) {
            if (node->children.find(ch) == node->children.end()) {
                node->children[ch] = pool_.allocate();
            }
            node = node->children[ch];
        }
        node->is_end_of_word = true;
    }
// ...
```
{{% /tab %}}
{{% /tabs %}}

### Core Operations: Search & Navigation

To search for an exact match or a prefix, we walk the tree following the characters. If a path breaks early, the word isn't in the tree. Because this traversal logic is shared, it's best to abstract it into a generic `navigate` helper.

{{% tabs "trie-search" %}}
{{% tab "Python" %}}
```python
    def _navigate(self, prefix: str) -> TrieNode | None:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def search(self, word: str) -> bool:
        node = self._navigate(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        return self._navigate(prefix) is not None
```
{{% /tab %}}
{{% tab "Go" %}}
```go
func (t *Trie) navigate(prefix string) *TrieNode {
    node := t.Root
    for i := 0; i < len(prefix); i++ {
        ch := prefix[i]
        if node.Children[ch] == nil {
            return nil
        }
        node = node.Children[ch]
    }
    return node
}

func (t *Trie) Search(word string) bool {
    node := t.navigate(word)
    return node != nil && node.IsEndOfWord
}

func (t *Trie) StartsWith(prefix string) bool {
    return t.navigate(prefix) != nil
}
```
{{% /tab %}}
{{% tab "C++" %}}
```cpp
    bool search(const std::string& word) const {
        const TrieNode* node = navigate(word);
        return node != nullptr && node->is_end_of_word;
    }

private:
    const TrieNode* navigate(const std::string& prefix) const {
        const TrieNode* node = root_;
        for (char ch : prefix) {
            auto it = node->children.find(ch);
            if (it == node->children.end()) return nullptr;
            node = it->second;
        }
        return node;
    }
};
```
{{% /tab %}}
{{% /tabs %}}

### Advanced Operations: Autocomplete & Deletion

Because a Trie groups common prefixes, **autocomplete** (finding all valid suffixes given a prefix) is naturally executed by navigating to the prefix's terminal node and initiating a Depth First Search (DFS) from there. 

**Deletion** is slightly trickier: we must recursively prune nodes starting from the leaf working upward, but *stop* pruning if a node is shared by another word (i.e. has sibling branches) or is itself flagged as a valid word.

{{% tabs "trie-advanced" %}}
{{% tab "Python" %}}
```python
    from collections.abc import Iterator

    def complete(self, prefix: str, limit: int = 10) -> Iterator[str]:
        """Generator to find top-k autocomplete suggestions."""
        node = self._navigate(prefix)
        if not node:
            return
            
        stack = [(node, prefix)]
        count = 0
        while stack and count < limit:
            curr, path = stack.pop()
            if curr.is_end_of_word:
                yield path
                count += 1
            # Push children to stack (DFS) - practically we'd use a heap for top-k ranked results
            for char, child in curr.children.items():
                stack.append((child, path + char))

    def delete(self, word: str) -> bool:
        """Deletes a word. Returns True iff the word existed and was removed."""
        def rec(node: TrieNode, i: int) -> tuple[bool, bool]:
            # returns (deleted, prune_this_node)
            if i == len(word):
                if not node.is_end_of_word:
                    return (False, False)
                node.is_end_of_word = False
                return (True, len(node.children) == 0)

            ch = word[i]
            child = node.children.get(ch)
            if child is None:
                return (False, False)

            deleted, prune_child = rec(child, i + 1)
            if not deleted:
                return (False, False)

            if prune_child:
                del node.children[ch]

            prune_here = (not node.is_end_of_word) and (len(node.children) == 0)
            return (True, prune_here)

        deleted, _ = rec(self.root, 0)
        return deleted
```
{{% /tab %}}
{{% /tabs %}}

### Longest Prefix Match (IP Routing)

Prefix tries are foundational for Internet routing, identifying the longest matching subnet mask. For example, a specialized binary trie matches an IP integer bit-by-bit.

{{% tabs "binary-trie-lpm" %}}
{{% tab "Python" %}}
```python
class BinaryTrieNode:
    def __init__(self):
        self.children = [None, None]
        self.route_data = None  # e.g., the egress port / subnet info

class BinaryTrie:
    def __init__(self):
        self.root = BinaryTrieNode()
        
    def longest_prefix_match(self, ip_int: int, bit_length: int = 32):
        node = self.root
        best_match = None
        
        for i in range(bit_length - 1, -1, -1):
            if node.route_data is not None:
                best_match = node.route_data
                
            bit = (ip_int >> i) & 1
            if node.children[bit] is None:
                break
            node = node.children[bit]
            
        if node.route_data is not None:
            best_match = node.route_data
            
        return best_match
```
{{% /tab %}}
{{% /tabs %}}


## Space and Constant Factors

The space complexity of a Trie is explicitly tied to the number of distinct prefixes.
Let $D$ be a set of keys defined over an alphabet $\Sigma \cup \{\text{EOS}\}$, where $\text{EOS}$ (End of String) is a unique termination marker. The exact node count of the structure is the cardinality of all distinct prefixes generated by the keys:

$$ V_{\text{nodes}} = \left| \{\text{prefix}(x,i) \mid x \in D, 0 \le i \le |x|\} \right| $$

If you model termination as an explicit $\text{EOS}$ edge, this formula counts every node strictly including the terminal leaves. If you instead model termination as an `is_end_of_word` Boolean flag, the prefix set is taken strictly over the raw key (excluding $\text{EOS}$) and the terminal states are absorbed into the existing nodes.

{{< alert title="The Sparse Node Problem" color="warning" >}}
If we insert "apple" and "application", the shared path `a-p-p-l` (4 nodes) is amortized. But if we insert "zenith" and no other word starts with 'z', we pay for 6 nodes, 5 of which have degree 1. It is exactly this sparse node waste that motivates advanced designs like the Adaptive Radix Tree (ART) and burst tries.
{{< /alert >}}

### The Alphabet and Memory Blowups

Memory consumption heavily depends on how child references are stored:
- **Arrays**: $O(|\Sigma|)$ memory per node. Fast $O(1)$ lookups, but massive memory waste for sparse nodes.
- **Hash Maps**: Dynamic sizing but high constant overhead per node.
- **Linked Lists**: Slow traversal ($O(|\Sigma|)$ worst-case) but tiny footprint per node.

### Hash-Array Mapped Tries (HAMT)
To bridge the gap between hash maps and Tries, **Hash-Array Mapped Tries (HAMT)** <a id="cite-bagwell-2001"></a>[[bagwell-2001]](#ref-bagwell-2001) replace arrays with a compressed bitmap of populated slots. Instead of branching on raw string bytes (256-way), HAMTs decompose a fixed-width hash into small chunks (often 5 bits $\to$ 32-way branching), using the bitmap to avoid allocating empty slots. Search depth is strictly bounded by the fixed hash width, so it behaves as $O(1)$ in practice while supporting immutability and persistence efficiently (like Clojure/Scala sets and concurrent Ctries) <a id="cite-prokopec-2012"></a>[[prokopec-2012]](#ref-prokopec-2012).

### Unicode and Normalization

When using strings, handling full Unicode is challenging. A naive array for 149,000+ characters will blow out cache lines. Real-world Tries almost always decompose strings into **bytes** (UTF-8 encoded), restricting the local alphabet to size 256.

{{< alert title="Unicode Normalization" color="info" >}}
You must also **normalize and case-fold** inputs before insertion to ensure equivalent strings follow the same path.
{{< /alert >}}

{{% tabs "unicode-norm" %}}
{{% tab "Python" %}}
```python
import unicodedata

def normalize_key(s: str) -> str:
    # Pick NFC unless you have specific compatibility requirements.
    # NFKC can change semantics (e.g., compatibility glyph folding).
    return unicodedata.normalize("NFC", s).casefold()
```
{{% /tab %}}
{{% /tabs %}}

## Radix Trees (Patricia Tries)

The **Radix Tree** (or Patricia Trie <a id="cite-morrison-1968"></a>[[morrison-1968]](#ref-morrison-1968)) solves this by compressing sequential chains of single-child nodes into labeled **edges**. By compressing runs of single-child nodes into labeled edges (e.g., `'r'` $\to$ `'oman'`), we reduce pointer overhead and depth. This aggressively bounds Trie depth by the *number of inserted strings $N$* rather than the maximum string length $L$.

### Visual Comparison

Consider inserting words `romane`, `romance`, `rubicon`, `rubicundus`. By collapsing `r-o-m` into a single edge `"rom"`, we reduce pointer overhead and depth.

{{< mermaid >}}
graph TD
    subgraph Standard ["Standard Trie: 20 Nodes"]
        Root1(( )) --> r(r) --> o(o) --> m(m)
        m --> a(a) --> n(n) --> e(e)
        m --> a(a) --> n(n) --> c(c) --> e2(e)
        Root1 --> Dot["..."]
    end
    
    subgraph Radix ["Radix Tree: 9 Nodes"]
        Root2(( )) -- "r" --> R(( ))
        R -- "oman" --> OMAN(( ))
        OMAN -- "e" --> ANE( )
        OMAN -- "ce" --> ANCE( )
        R -- "ubic" --> UBIC(( ))
        UBIC -- "on" --> ON( )
        UBIC -- "undus" --> UNDUS( )
    end
    
    style Standard fill:#fff,stroke:#333
    style Radix fill:#fff,stroke:#333
{{< /mermaid >}}

### Edge Splitting

Inserting requires **splitting edges**. If an edge says "rubic" and we insert "rubber", we split "rubic" at "rub", creating a fork: one way "ic", other way "ber".

{{< mermaid >}}
graph TD
  subgraph Before["Before inserting 'rubber'"]
    R((root)) -- "rubic" --> E1["..."]
  end

  subgraph After["After inserting 'rubber'"]
    R2((root)) -- "rub" --> P((split node))
    P -- "ic" --> A["..."]
    P -- "ber" --> B["..."]
  end
  
  style P fill:#ccf,stroke:#333
{{< /mermaid >}}

#### String Slicing Footguns

{{< alert title="Memory Traps" color="warning" >}}
Edge splitting relies heavily on string slicing, which behaves radically differently across languages and can lead to severe memory footguns:
- **Python**: Slicing (`s[common:]`) creates a brand-new string copy. If you insert a 1MB string and split it 1,000 times as new words arrive, you trigger $O(L^2)$ memory allocation and copy overhead.
- **Go**: Slicing (`s[common:]`) does *not* copy; it creates a new slice header that pins the original backing array in memory. If you load a massive 1GB dictionary file and slice it to populate edge labels, the Garbage Collector can *never* free that 1GB buffer, even if your Trie only actually references a few kilobytes of text.
- **C++**: The modern C++ approach avoids copies by using `std::string_view` for edge labels. However, this essentially acts as a raw pointer. If the original strings being inserted are destroyed or fall out of scope, the `std::string_view` edge labels silently become dangling pointers, leading to catastrophic Use-After-Free crashes. You must tightly couple the Trie's lifetime to an underlying string Arena.
{{< /alert >}}

To prove these traps are real, here are three minimal programs that accurately reproduce each language's failure mode, complete with their actual output:

{{% tabs "slicing-traps" %}}
{{% tab "Python (O(L²) Copy Trap)" %}}
```python
import sys
import time

# Create a massive 50MB string
length = 50_000_000
massive_string = "A" * length

print(f"Original string size: {sys.getsizeof(massive_string) / 1024 / 1024:.2f} MB")

start = time.time()
# Slice off just the first character (e.g., splitting "A" from the rest)
sliced_copy = massive_string[1:]
end = time.time()

print(f"Sliced string size:   {sys.getsizeof(sliced_copy) / 1024 / 1024:.2f} MB")
print(f"Time to slice:        {(end - start) * 1000:.2f} ms")
print(f"Are they the same memory object? {massive_string is sliced_copy}")
```

**Output:**
```text
Original string size: 47.68 MB
Sliced string size:   47.68 MB
Time to slice:        18.20 ms
Are they the same memory object? False
```
*Note that even slicing off a mere subset of characters forced the allocator to duplicate 47.68 MB of memory!*
{{% /tab %}}
{{% tab "Go (GC Pinning Trap)" %}}
```go
package main

import (
    "fmt"
    "runtime"
)

// Global reference representing an edge label in our Trie
var edgeLabel string

func loadDictionary() {
    // Allocate a massive 50MB dictionary buffer
    b := make([]byte, 50*1024*1024)
    dictionary := string(b)
    
    // The Trie only needs a 3-byte slice for an edge label
    edgeLabel = dictionary[0:3]
}

func main() {
    loadDictionary()

    // Force Garbage Collection to clean up unused memory
    runtime.GC()

    // Check how much memory is still pinned on the heap
    var m runtime.MemStats
    runtime.ReadMemStats(&m)
    
    fmt.Printf("Edge label length:    %d bytes\n", len(edgeLabel))
    fmt.Printf("Heap memory actively in use: %d MB\n", m.Alloc/1024/1024)
    fmt.Printf("-> The entire 50MB buffer is pinned by the 3-byte slice!\n")
}
```

**Output:**
```text
Edge label length:    3 bytes
Heap memory actively in use: 50 MB
-> The entire 50MB buffer is pinned by the 3-byte slice!
```
{{% /tab %}}
{{% tab "C++ (Dangling Pointer Trap)" %}}
```cpp
#include <iostream>
#include <string>
#include <string_view>

std::string_view getEdgeLabel() {
    // A dynamically allocated string (e.g., parsed from a file loop)
    std::string dynamic_string = "temporary_dictionary_word";
    
    // We try to save memory by using a string_view for the edge label
    std::string_view edge = dynamic_string;
    
    // As the function scope ends, dynamic_string is destroyed!
    return edge; 
}

int main() {
    std::string_view dangling_edge = getEdgeLabel();
    
    std::cout << "Expected edge label:  temporary_dictionary_word" << std::endl;
    std::cout << "Actual memory output: " << dangling_edge << std::endl;
    std::cout << "-> The string_view now points to garbage (Use-After-Free)!" << std::endl;
    
    return 0;
}
```

**Output:**
```text
Expected edge label:  temporary_dictionary_word
Actual memory output: !Ms>cFe/nary_word
-> The string_view now points to garbage (Use-After-Free)!
```
*Because the original `std::string` was de-allocated locally across the stack boundary, the `std::string_view` reads corrupted heap memory yielding junk unicode.*
{{% /tab %}}
{{% /tabs %}}

### Amortized Cost

If $M = \sum |s_i|$ is the total length of all inserted strings, building a Radix Tree does not spend $O(N \log N)$ as in comparison sorts.
Finding common prefix lengths and mapping children takes time bounded linearly by the characters processed. In typical implementations with efficient child lookups and careful slicing/label handling, full construction is strictly bounded by $O(M)$ or $O(M \cdot \alpha)$ (where $\alpha$ is map lookup overhead).

## Cache and Disk-Conscious Tries

Pointer-based Tries are hostile to modern CPUs. Traversing `node->children[char]` conceptually jumps across the heap. Searching a 10-byte string can incur up to ~10 Last-Level Cache (LLC) misses in the worst case. *(Note: as we will see later, these same deterministic access patterns are exactly the footprint we must destroy in a data-oblivious setting).*

{{< mermaid >}}
flowchart LR
  subgraph PointerTrie["Pointer trie lookup (up to 1 cache miss per hop)"]
    A0["node@0xA.. (line X)"] --> A1["node@0xF.. (line Y)"] --> A2["node@0x1.. (line Z)"]
  end

  subgraph Packed["Packed layout (many nodes per line/page)"]
    B0["page/array block (contiguous)"] --> B1["index within block"] --> B2["next block (rare)"]
  end
  
  style PointerTrie fill:#ffcccc,stroke:#333
  style Packed fill:#ccffcc,stroke:#333
{{< /mermaid >}}

### Adaptive Radix Trees (ART)

The **Adaptive Radix Tree (ART)** <a id="cite-leis-art"></a>[[leis-art]](#ref-leis-art) resolves massive array waste using dynamically sized, cache-aligned nodes (Node4, Node16, Node48, Node256).

{{< mermaid >}}
flowchart LR
  subgraph N4["Node4"]
    K4["keys[<=4]"] --- C4["children[<=4]"]
  end
  subgraph N16["Node16 (SIMD-friendly)"]
    K16["keys[<=16]"] --- C16["children[<=16]"]
  end
  subgraph N48["Node48"]
    IDX["index[256] = child slot or -1"] --- C48["children[<=48]"]
  end
  subgraph N256["Node256"]
    C256["children[256] direct"] 
  end
{{< /mermaid >}}

The tree scales container sizes intrinsically:

{{< mermaid >}}
stateDiagram-v2
  [*] --> Node4: insert up to 4 children
  Node4 --> Node16: +1 child (grow)
  Node16 --> Node48: +1 child (grow)
  Node48 --> Node256: +1 child (grow)

  Node256 --> Node48: delete triggers shrink
  Node48 --> Node16: delete triggers shrink
  Node16 --> Node4: delete triggers shrink
{{< /mermaid >}}

Evaluating `Node16` uses **SIMD** to evaluate all 16 child prefixes simultaneously.

{{% tabs "simd-art" %}}
{{% tab "C++ (SIMD)" %}}
```cpp
#include <immintrin.h>

struct Node16 {
    uint8_t count;         // Tracks populated slots
    uint8_t keys[16];      // 16 child keys (128 bits), kept sorted
    Node* children[16];

    int findChild(uint8_t key) const {
#if defined(__AVX2__) || defined(__SSE2__)
        __m128i key_vec = _mm_set1_epi8((char)key);
        __m128i node_keys = _mm_loadu_si128((__m128i*)this->keys);
        __m128i cmp = _mm_cmpeq_epi8(key_vec, node_keys);
        
        // Note: Production ARTs mask the result with `count` to avoid matching
        // uninitialized garbage keys in the SIMD vector.
        unsigned live = (count == 16) ? 0xFFFFu : ((1u << count) - 1u);
        unsigned mask = (unsigned)_mm_movemask_epi8(cmp) & live;

        if (mask != 0) {
            return __builtin_ctz(mask); // ctz = count trailing zeroes (finds the least-significant set bit)
        }
        return -1;
#else
        for (int i=0; i<count; i++) {
            if (keys[i] == key) return i;
        }
        return -1;
#endif
    }
};
```
{{% /tab %}}
{{% /tabs %}}

### External Memory Model (DAM)

When trees exceed RAM, performance is bottlenecked by the **Disk Access Machine (DAM)** model <a id="cite-aggarwal-1988"></a>[[aggarwal-1988]](#ref-aggarwal-1988), where $B$ is the block size in bytes (e.g., 4KB disk pages).
Standard B-trees take $O(\log_B N)$ I/Os while Pointer tries take $O(L)$ I/Os. If $B$ is large, B-trees dominate.

- **Relational DBs**: SP-GiST is designed to support partitioned trees such as radix trees (tries) and map their nodes onto disk pages efficiently <a id="cite-postgresql-sp-gist"></a>[[postgresql-sp-gist]](#ref-postgresql-sp-gist).
- **LSM Trees (RocksDB)**: Log-Structured Merge tables are block-based formats (like a 4KB block containing sorted data with an index footprint <a id="cite-rocksdb-sst"></a>[[rocksdb-sst]](#ref-rocksdb-sst)). Tries frequently appear as **auxiliary structures** (prefix filters) rather than primary layouts.

### Advanced Practical Trie Variants
- **Burst tries** <a id="cite-heinz-2002"></a>[[heinz-2002]](#ref-heinz-2002): Handle skewed string distributions by collecting strings in buckets before 'bursting' them into trie nodes.
- **String B-trees**: Combines B-trees with Patricia tries, achieving the theoretically optimal $O(\log_B N + L/B)$ string search bound for external memory <a id="cite-ferragina-grossi"></a>[[ferragina-grossi]](#ref-ferragina-grossi).

## Succinct Tries

{{< alert title="Information-Theoretic Lower Bound" color="primary" >}}
To push limits, we bypass pointers entirely. The information-theoretic bound to store any tree topology with $N$ nodes is $2N + o(N)$ bits. Heap-allocated pointer Tries over-allocate massively in comparison.
{{< /alert >}}

**Succinct Data Structures** close this gap.

### Level-Ordered Unary Degree Sequence (LOUDS)
LOUDS encodes topology in a bit-vector by recording node degrees in breadth-first order.

Imagine a tiny root node with 2 children; child 0 has 1 child, child 1 is a leaf.

{{< mermaid >}}
flowchart TB
  T["Ordinal tree (Root)"] --> E["Encode level-order degrees: 110 (root), 10 (child 0), 0 (child 1), 0 (leaf)"]
  E --> B["Bitvector LOUDS (110 10 0 0)"]
  B --> R["rank/select bit-structures"]
  R --> N["O(1) Navigation ops"]
{{< /mermaid >}}

**Double Array Tries (DAT)** <a id="cite-aoe-1989"></a>[[aoe-1989]](#ref-aoe-1989) are another prominent static layout, compressing state transitions into two interlaced contiguous arrays. While not minimal like LOUDS bits, DATs offer blistering $O(1)$ memory transitions perfect for static dictionaries and NLP tokenizers.

**SuRF (Succinct Range Filter)** deploys succinct tries (Fast Succinct Tries) as standalone filters in LSM tables, skipping full I/O block reads <a id="cite-zhang-surf"></a>[[zhang-surf]](#ref-zhang-surf).


Based on standard LOUDS conventions <a id="cite-memoria-louds"></a>[[memoria-louds]](#ref-memoria-louds), navigation relies on **Rank/Select** bitwise operations:
`first_child(i) = select0(rank1(i + 1)) + 1`

To ensure calculation consistency, implementations must strictly define their conventions. For example, Memoria's layout assumes:
- `rank1(i)` counts the number of `1`s in the half-open range `[0, i)`.
- `select0(k)` returns the index sequence of the $k$-th `0` (where $k$ is 1-based, $k=1, 2, \dots$).
- Memoria's specific formulation prepends a `10` prefix to the overall unary degree string to align the root.

By throwing out pointers entirely, succinct structures map the topology directly onto the bitvector, allowing vast string dictionaries (like massive web crawls) to load effortlessly into RAM. However, succinct layouts improve storage locality but do not inherently hide their access patterns from physical observation.

## Searching Without Being Searched: Data-Oblivious Tries

{{< alert title="The &quot;Oblivious&quot; Nomenclature Collision" color="warning" >}}
In computer science, the prefix "oblivious" is heavily overloaded depending on the subfield:
*   **Data-Oblivious (Security)**: Algorithms whose memory access patterns do not leak information about the underlying data or queries.
*   **Cache-Oblivious (Performance)**: Algorithms that perform optimally across memory hierarchies without knowing the specific hardware cache line size $B$ (e.g., Cache-Oblivious search trees / van Emde Boas layouts).
*   **Oblivious Decision Trees (Machine Learning)**: Trees where all nodes at the same depth evaluate the identical feature, preventing inference attacks on the classification path.

*This section strictly covers the cryptographic **Data-Oblivious** design.*
{{< /alert >}}

Up to this point, our optimizations have focused on making string searches fast and memory-efficient. But in cloud environments, *efficiency* often trades off directly with *privacy*. 

When querying a remote server for a prefix (e.g., searching a medical database or a DNS resolver), the server can infer exactly what you are searching for just by observing the **memory access pattern**, even if the query string itself is encrypted. 

This security gap exists even at the silicon edge. When executing computations inside **Trusted Execution Environments (TEEs)** like Intel SGX or AMD SEV, the CPU state is heavily encrypted, but the motherboard memory bus is exposed. A privileged host can infer traversals via page-fault and cache side channels. A physical adversary can observe an address trace directly on the memory bus. By executing an **access pattern side-channel attack** during a Trie traversal, they can fully deduce the query. If you search for "HIV", the bus observes memory block $A$, then $B$, then $C$. If you search for "HIV" again tomorrow, the bus observes the exact same $A \to B \to C$ traversal and knows you repeated the query.

To achieve cryptographically secure privacy against hardware probing, the sequence of physical memory accesses must be **computationally indistinguishable from random, up to the leakage of query length**. We achieve this using **Oblivious RAM (ORAM)** applied to Tries <a id="cite-wang-2014"></a>[[wang-2014]](#ref-wang-2014). This directly inherits techniques from the foundational Path ORAM protocol <a id="cite-stefanov-2013"></a>[[stefanov-2013]](#ref-stefanov-2013).

### Path ORAM and the Oblivious Trie

The most practical approach utilizes **Path ORAM**. We decouple the *logical* Trie topology from its *physical* storage constraints.

1. **The Server**: The physical storage is treated as a massive binary tree of "buckets." Each bucket holds up to $Z$ logical trie nodes (or encrypted dummy blocks).
2. **The Client**: The client maintains a mapping of every logical trie node to a random "Path ID" (a specific leaf in the server's physical tree).
3. **The Invariant**: A logical node is always stored *somewhere* along the path from the root bucket down to its assigned Path ID bucket.

When we need to traverse from `H` to `I` in our logical trie:
1. We look up `I`'s physical Path ID in our local client map.
2. We download the **entire physical path** from the server root to that leaf. 
3. We decrypt the path locally, find `I`, and read its pointers.
4. We randomly assign `I` a *new* Path ID for the future, breaking the access pattern.
5. We re-encrypt the entire path (greedily pushing nodes as far down as they can legally go) and write the **entire path** back to the server.

{{< mermaid >}}
graph TD
    subgraph Logical["Logical Trie"]
        Root1((root)) --> N1(H)
        N1 --> N2(I)
        N2 --> N3(V)
    end
    
    subgraph Physical["Physical Server (Path ORAM Tree)"]
        P_R["Root Bucket (Z blocks)"] --> P_0["Bucket 0"]
        P_R --> P_1["Bucket 1"]
        P_0 --> P_00["Bucket 00"]
        P_0 --> P_01["Bucket 01"]
        P_1 --> P_10["Bucket 10"]
        P_1 --> P_11["Bucket 11"]
    end
    
    %% Highlight a Path access
    style P_R fill:#ccf,stroke:#333
    style P_1 fill:#ccf,stroke:#333
    style P_10 fill:#ccf,stroke:#333
{{< /mermaid >}}

If node 'H' is mapped to Path `10`, we download Buckets `Root`, `1`, and `10` (highlighted in blue). To the hosting server, an attacker merely sees a uniformly random path being downloaded and re-uploaded with fresh ciphertexts.

### The Mathematics of Oblivion

This cryptographic security comes at a steep asymptotic cost. 
Let $N$ be the number of nodes in the Trie. The physical server tree has $O(N)$ buckets, creating a physical tree depth of $O(\log N)$.

Reading a single logical trie node requires downloading and uploading an entire path of length $O(\log N)$, where each bucket contains $Z$ blocks. Thus, the bandwidth overhead to read a *single node* is $O(Z \log N)$. 

If a query string has length $L$, searching a standard Trie takes $O(L)$ memory accesses. Searching an **Oblivious Trie** magnifies this to $O(L \cdot Z \log N)$ bandwidth. With $Z=4$ (a common choice), the stash overflow probability drops exponentially with the stash size; with appropriate client stash bounds, overflow becomes cryptographically negligible. The overall asymptotic cost to search a string obliviously is thus bounded at $O(L \log N)$.

### Practical Implementation

The following conceptual Python snippet demonstrates the ORAM read/remap/write cycle executed by the client during traversal:

{{% tabs "oblivious-trie" %}}
{{% tab "Python (Conceptual ORAM)" %}}
```python
import random

class ObliviousTrie:
    def __init__(self, server_interface, num_leaves):
        self.server = server_interface
        self.num_leaves = num_leaves
        self.position_map = {} # Maps: logical_node_id -> physical_leaf_id
        self.stash = []        # Client-side temporary storage for overflow
        
        # Initialize Root node (ID 1) to a random path
        self.position_map[1] = random.randint(0, self.num_leaves - 1)
        
    def access_node(self, node_id: int):
        """Fetches a trie node from the server obliviously."""
        # 1. Lookup the path assigned to this node
        leaf_id = self.position_map.get(node_id)
        
        # 2. Oblivious Read: Download entire path. Server sees only a random leaf ID.
        path_blocks = self.server.read_path(leaf_id)
        
        # 3. Decrypt blocks and absorb real nodes into the local stash
        for block in path_blocks:
            if not block.is_dummy():
                self.stash.append(block.decrypt())
                
        # 4. Find our target node in the stash
        target_node = next((n for n in self.stash if n.id == node_id), None)
        if target_node is None:
            raise KeyError(f"Node {node_id} not found in path/stash. Integrity error!")
        
        # 5. Remap target to a NEW random path to decorrelate future accesses
        new_leaf = random.randint(0, self.num_leaves - 1)
        self.position_map[node_id] = new_leaf
        target_node.path_id = new_leaf
        
        # 6. Oblivious Write: Re-encrypt and upload the path.
        #    (Note: Write-back drains eligible blocks from the stash to prevent
        #     it from growing unbounded, filling any remaining empty slots 
        #     with fresh cipher dummy blocks.)
        new_path_blocks = self._build_writeback_path(leaf_id)
        self.server.write_path(leaf_id, new_path_blocks)
        
        return target_node
```
{{% /tab %}}
{{% /tabs %}}

{{< alert title="ORAM Isn't Free" color="warning" >}}
While Path ORAM solves the access-pattern leakage, it introduces staggering systems overhead. The `position_map` itself requires $O(N)$ memory; to prevent storing *that* in plaintext, it must be recursively stored in smaller ORAM trees. Furthermore, data confidentiality is not enough: the client must apply Authenticated Encryption (AEAD/MACs) to every block to prevent the server from silently corrupting or replaying nodes. Finally, the $O(Z \log N)$ bandwidth amplification introduces massive latency round-trips for every single Trie hop.
{{< /alert >}}

By integrating ORAM directly into the Trie's pointer chasing, we securely decouple *what* we are querying from *how* the memory is accessed, proving that prefix structures can be adapted even for zero-trust environments.

## Conclusion

### Architectural Summary Table

| Variant | Topology Focus | Time Complexity | Memory Footprint | Primary Security/Hardware Threat Model | Core Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard Trie** | Uncompressed node chains | $O(L)$ | High ($O(L \cdot \vert \Sigma \vert)$ pointers) | None (Leaky access patterns) | Simple autocomplete, memory-abundant hashing |
| **Radix Tree** | Edge compression | $O(L_{compressed})$ | Medium (Bounds depth to $N$) | None (Leaky access patterns) | IP routing (CIDR), generic inverted indices |
| **Adaptive Radix (ART)** | Dynamic SIMD nodes | $O(L_{compressed})$ | Low (Adaptive node sizing) | None (Leaky access patterns) | High-performance in-memory databases |
| **Succinct (LOUDS)** | Implicit bitvectors | $O(L)$ | Minimal (Theoretical entropy) | None (Locality tracing still visible) | Read-heavy immutable datasets (SSTables) |
| **Oblivious Trie (ORAM)** | Path-shuffled buckets | $O(L \log N)$ | Heavy ($O(N)$ position map) | Resists Physical Highway Probing | Zero-Trust / Public Cloud Enclaves (TEEs) |

Prefix Trees occupy a distinct niche. They defy comparison-based lower bounds, turning string queries into character-routed prefix matching. For simple exact matches, Hash Maps or HAMTs remain dominant. But when queries involve prefixes, ranges, or structural ordering, specialized trees shine. While pointer-heavy standard Tries suffer poor cache-locality, refinements like the **Radix Tree** and **Adaptive Radix Tree (ART)** tightly pack operations for RAM density. When bound for disk or extreme scale, **LOUDS**, **DATs**, and **String B-trees** isolate byte-workloads efficiently. Finally, when deployed in zero-trust cloud architectures, **Oblivious Tries** dynamically shuffle their physical footprints to secure access patterns.

Ultimately, choosing the right structure is an architectural tradeoff between cache-locality, insertion dynamics, query requirements, and privacy. For structured string workloads under rigorous technical constraints, these modern prefix structures provide indispensable alternatives to generic indexing.

---

## Appendix: Advanced Topics

### Analytic Combinatorics and Typical Behavior

For unbiased random tries under a memoryless (Bernoulli) source ($p=0.5$), the expected path length concentrates remarkably tightly. Flajolet's extensive survey <a id="cite-flajolet-2006"></a>[[flajolet-2006]](#ref-flajolet-2006) details how path length recurrences are evaluated using the **Mellin Transform** and residue calculus. 

Under an asymmetric memoryless source, Devroye <a id="cite-devroye-1992"></a>[[devroye-1992]](#ref-devroye-1992) explicitly bounds the typical height $H_n$ closely to $c \log n$:
$$ \mathbb{E}[H_n] \sim \frac{2 \log_2 n}{-\log_2(\sum_{j} p_j^2)} $$

For binary strings with uniform probabilities $p=q=0.5$, this simplifies to $2 \log_2 n$. Instead of clean sub-Gaussian tails, large-scale trie height has characteristic periodic fluctuations, experiencing deviations of order $\sqrt{\log n}$.

### The FM-Index
The **FM-Index** <a id="cite-ferragina-2000"></a>[[ferragina-2000]](#ref-ferragina-2000) is a compressed structure analogous to navigating a Trie backwards using the Burrows-Wheeler Transform (BWT). It links Prefix Trees directly to Shannon entropy, providing substring queries atop fully compressed data.

### Minimal Acyclic DFAs (DAWG)
When a Trie is fully static, string compression via Radix paths is insufficient. A **Minimal Acyclic Deterministic Finite Automaton** (Minimal DFA or DAWG) merges common *suffixes*, not just prefixes <a id="cite-daciuk-2000"></a>[[daciuk-2000]](#ref-daciuk-2000). 

By sharing the terminal `-ing` nodes for words like `testing`, `fishing`, and `reading`, the DAWG reaches the true theoretical entropy bound for static lexicons. A closely related structure is the **Aho-Corasick Automaton**, which adds "failure links" back up the trie to enable massively parallel substring search (e.g., spam filtering).

{{< mermaid >}}
graph TD
    subgraph Trie ["Trie (Prefix Merge Only)"]
        Root1 --> T[t] --> E1[e] --> S1[s] --> T1[t] --> I1[i] --> N1[n] --> G1[g]
        Root1 --> F[f] --> I_2[i] --> S2[s] --> H[h] --> I2[i] --> N2[n] --> G2[g]
    end
    
    subgraph DAWG ["DAWG (Prefix + Suffix Merge)"]
        Root2 --> T_D[t] --> E_D[e] --> S_D[s] --> T_D2[t]
        Root2 --> F_D[f] --> I_D[i] --> S_D2[s] --> H_D[h]
        T_D2 -.-> ING_I[i]
        H_D -.-> ING_I
        ING_I -.-> ING_N[n] -.-> ING_G[g]
    end
{{< /mermaid >}}

### Isomorphisms: TSTs and Quicksort
Ternary Search Trees (TST) elegantly bridge comparison trees and Tries. Bentley and Sedgewick <a id="cite-bentley-1997"></a>[[bentley-1997]](#ref-bentley-1997) demonstrate a formal isomorphism between building a TST and executing Multikey Quicksort. The cost equivalent simplifies to roughly $2 \ln N$, adapting intrinsically to the string distribution.

---

## References

- **[fredkin-1960]** **<a id="ref-fredkin-1960"></a>Fredkin, E. (1960).** *[Trie Memory](https://dl.acm.org/doi/10.1145/367390.367400).* Communications of the ACM. [↩](#cite-fredkin-1960)
- **[morrison-1968]** **<a id="ref-morrison-1968"></a>Morrison, D. R. (1968).** *[PATRICIA—Practical Algorithm to Retrieve Information Coded in Alphanumeric](https://dl.acm.org/doi/10.1145/321479.321481).* Journal of the ACM. [↩](#cite-morrison-1968)
- **[leis-art]** **<a id="ref-leis-art"></a>Leis, V., Kemper, A., & Neumann, T. (2013).** *[The Adaptive Radix Tree: ARTful Indexing for Main-Memory Databases](https://db.in.tum.de/~leis/papers/ART.pdf).* ICDE. [↩](#cite-leis-art)
- **[bagwell-2001]** **<a id="ref-bagwell-2001"></a>Bagwell, P. (2001).** *[Ideal Hash Trees](https://lampwww.epfl.ch/papers/idealhashtrees.pdf).* EPFL. [↩](#cite-bagwell-2001)
- **[heinz-2002]** **<a id="ref-heinz-2002"></a>Heinz, S. et al. (2002).** *[Burst tries: a fast, efficient data structure for string keys](https://dl.acm.org/doi/abs/10.1145/506309.506312).* ACM TOIS. [↩](#cite-heinz-2002)
- **[prokopec-2012]** **<a id="ref-prokopec-2012"></a>Prokopec, A. et al. (2012).** *[Concurrent Tries with Efficient Non-Blocking Snapshots](https://chara.epfl.ch/~prokopec/lcpc_ctries.pdf).* PPoPP. [↩](#cite-prokopec-2012)
- **[aoe-1989]** **<a id="ref-aoe-1989"></a>Aoe, J. (1989).** *[An Efficient Digital Search Algorithm by Using a Double-Array Structure](https://dl.acm.org/doi/10.1109/32.31365).* IEEE TSE. [↩](#cite-aoe-1989)
- **[daciuk-2000]** **<a id="ref-daciuk-2000"></a>Daciuk, J. et al. (2000).** *[Incremental Construction of Minimal Acyclic Finite-State Automata](https://aclanthology.org/J00-1002.pdf).* Computational Linguistics. [↩](#cite-daciuk-2000)
- **[aggarwal-1988]** **<a id="ref-aggarwal-1988"></a>Aggarwal, A., & Vitter, J. S. (1988).** *[The Input/Output Complexity of Sorting and Related Problems](https://dl.acm.org/doi/10.1145/48529.48535).* Communications of the ACM. [↩](#cite-aggarwal-1988)
- **[postgresql-sp-gist]** **<a id="ref-postgresql-sp-gist"></a>PostgreSQL Documentation.** *[SP-GiST Indexes](https://www.postgresql.org/docs/current/spgist.html).* [↩](#cite-postgresql-sp-gist)
- **[rocksdb-sst]** **<a id="ref-rocksdb-sst"></a>RocksDB.** *[A Tutorial of RocksDB SST formats](https://github.com/facebook/rocksdb/wiki/A-Tutorial-of-RocksDB-SST-formats).* GitHub. [↩](#cite-rocksdb-sst)
- **[zhang-surf]** **<a id="ref-zhang-surf"></a>Zhang, H. et al. (2018).** *[SuRF: Practical Range Query Filtering with Fast Succinct Tries](https://db.cs.cmu.edu/papers/2018/mod601-zhangA-1.pdf).* SIGMOD. [↩](#cite-zhang-surf)
- **[ferragina-grossi]** **<a id="ref-ferragina-grossi"></a>Ferragina, P., & Grossi, R. (1999).** *[The String B-Tree: A New Data Structure for String Search in External Memory](https://www.researchgate.net/publication/2671781).* J. ACM. [↩](#cite-ferragina-grossi)
- **[flajolet-2006]** **<a id="ref-flajolet-2006"></a>Flajolet, P. (2006).** *[The Ubiquitous Digital Tree](https://algo.inria.fr/flajolet/Publications/Flajolet06.pdf).* INRIA. [↩](#cite-flajolet-2006)
- **[devroye-1992]** **<a id="ref-devroye-1992"></a>Devroye, L. (1992).** *[A Note on the Height of Tries](https://luc.devroye.org/height-of-trie.pdf).* Acta Informatica. [↩](#cite-devroye-1992)
- **[bentley-1997]** **<a id="ref-bentley-1997"></a>Bentley, J. L., & Sedgewick, R. (1997).** *[Fast algorithms for sorting and searching strings](https://www.cs.princeton.edu/~rs/strings/).* SODA. [↩](#cite-bentley-1997)
- **[memoria-louds]** **<a id="ref-memoria-louds"></a>Memoria Framework.** *[Level Order Unary Degree Sequence (LOUDS)](https://memoria-framework.dev/docs/data-zoo/louds-tree/).* [↩](#cite-memoria-louds)
- **[stefanov-2013]** **<a id="ref-stefanov-2013"></a>Stefanov, E., et al. (2013).** *[Path ORAM: An Extremely Simple Oblivious RAM Protocol](https://dl.acm.org/doi/10.1145/2508859.2516660).* CCS. [↩](#cite-stefanov-2013)
- **[wang-2014]** **<a id="ref-wang-2014"></a>Wang, X. S., Nayak, K., Liu, C., et al. (2014).** *[Oblivious Data Structures](https://eprint.iacr.org/2014/185.pdf).* CCS. [↩](#cite-wang-2014)
- **[ferragina-2000]** **<a id="ref-ferragina-2000"></a>Ferragina, P., & Manzini, G. (2000).** *[Opportunistic Data Structures with Applications](https://dl.acm.org/doi/10.1109/SFCS.2000.892127).* FOCS. [↩](#cite-ferragina-2000)
