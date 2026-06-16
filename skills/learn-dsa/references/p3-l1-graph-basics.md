# P3-L1: Graph Representations

## Concept

A graph is a set of **nodes (vertices)** connected by **edges**. Unlike trees, graphs have no root, no parent-child constraint, and can contain **cycles**.

**Key graph properties:**
- **Directed vs Undirected:** edges have direction (A→B ≠ B→A) or don't.
- **Weighted vs Unweighted:** edges carry a cost/distance or just existence.
- **Cyclic vs Acyclic:** a path can loop back to a visited node, or not.
- A tree is a special case: a connected, acyclic, undirected graph.

**Two representations:**

**Adjacency List** — a dict (or list of lists) mapping each node to its neighbors:
```python
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0],
    3: [1]
}
```
- Space: O(V + E) where V = vertices, E = edges.
- Check if edge exists: O(degree of node).
- Iterate neighbors: O(degree of node).
- **Default choice** for sparse graphs (most real-world graphs).

**Adjacency Matrix** — a 2D boolean array where `matrix[i][j] = True` means edge i→j:
```python
# 4 nodes, 0-indexed
matrix = [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [0, 1, 0, 0]
]
```
- Space: O(V²).
- Check if edge exists: O(1).
- Iterate neighbors: O(V) — must scan entire row.
- Best for dense graphs or when O(1) edge lookup is critical.

**Building from an edge list** (common in interview problems):
```python
def build_adjacency_list(n, edges):
    graph = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)  # undirected
    return graph
```

## Analogy

A graph is a map of cities and roads. Cities are nodes; roads are edges. If roads are one-way, it's a directed graph. If roads have speed limits (costs), it's weighted.

An **adjacency list** is like each city keeping a contact list of cities it's directly connected to. To find where you can go from Chicago, just look up Chicago's list.

An **adjacency matrix** is like a giant spreadsheet with every city on both axes. Cell (Chicago, Denver) = 1 means there's a direct road. Fast to check any pair — but 95% of the spreadsheet is empty for a typical map (sparse graph).

## Workshop

**File:** `build_graph.py`

**Problem:** Implement graph construction and basic queries.

**Part 1 — Build adjacency list:**
Given `n` nodes (labeled 0 to n-1) and a list of undirected edges, build and return an adjacency list as a dict.

```
n = 5
edges = [[0,1],[0,2],[1,3],[2,4]]

Result: {0: [1, 2], 1: [0, 3], 2: [0, 4], 3: [1], 4: [2]}
```

Implement `build_graph(n, edges)`.

**Part 2 — Count nodes and edges:**
Given an adjacency list, return the number of nodes and the number of edges.

```
graph = {0: [1, 2], 1: [0, 3], 2: [0, 4], 3: [1], 4: [2]}

nodes = 5
edges = 4   # each undirected edge counted once
```

Implement `count_nodes_edges(graph)`. For undirected graphs, each edge appears twice in the adjacency list (once per endpoint) — account for this.

**Part 3 — Has path (using any traversal):**
Given a graph (adjacency list), a source node `src`, and a destination node `dst`, return `True` if there is any path from `src` to `dst`.

```
graph = {0: [1, 2], 1: [0, 3], 2: [0, 4], 3: [1], 4: [2]}
has_path(graph, 0, 4)  # True
has_path(graph, 3, 4)  # True
has_path(graph, 3, 2)  # True (3→1→0→2)
```

Implement `has_path(graph, src, dst)`. Use either BFS or DFS — your choice. Must handle cycles (track visited nodes).

## Acceptance Criteria / Edge Cases

**Part 1:**
- `n = 1, edges = []` → `{0: []}`.
- Self-loop edge `[0, 0]` → add 0 to its own neighbor list.
- Isolated node (not in any edge) → still present in dict with empty list.

**Part 2:**
- Sum all neighbor list lengths, divide by 2 (undirected).
- Node count is `len(graph)`.

**Part 3:**
- `src == dst` → `True`.
- No path exists → `False`.
- Cyclic graph → does not infinite loop (visited set required).

## Complexity Target

- Build: O(V + E).
- Count: O(V + E).
- Has path: O(V + E) — must visit every node and edge in the worst case.

## Common Mistakes

- Forgetting to add both directions for undirected edges in Part 1.
- Counting edges as the sum of all adjacency list lengths (gives 2E, not E).
- Has path without a `visited` set — infinite loop on any cycle.
- Using `graph.keys()` to count nodes when some nodes might not appear as keys (use `n` from Part 1 to initialize all nodes).

## Interview vs Fundamentals Note

**Fundamentals:** The adjacency list is the default. Before solving any graph problem, always ask: directed or undirected? Weighted or unweighted? Cyclic or acyclic? These properties determine which algorithm to use.

**Interview prep:** Graph problems almost always give you an edge list and expect you to build the adjacency list yourself. This is boilerplate — have the `build_adjacency_list` pattern memorized so you can write it in 5 lines and move on to the actual problem.

## Bridge

You can now represent any graph and traverse it to answer reachability questions. Next: BFS — the traversal that finds shortest paths in unweighted graphs.
