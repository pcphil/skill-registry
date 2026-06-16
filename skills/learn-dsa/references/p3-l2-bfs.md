# P3-L2: BFS & Shortest Path on Unweighted Graphs

## Concept

**Breadth-First Search (BFS)** explores a graph level by level — all neighbors of the source first, then their neighbors, and so on. It uses a **queue** (FIFO) to process nodes in discovery order.

**BFS template:**
```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()
        # process node
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

**Why BFS finds shortest paths (unweighted):**
BFS visits nodes in order of their distance from the source. The first time BFS reaches a node, it has taken the fewest possible edges to get there. This guarantee breaks for weighted graphs (use Dijkstra instead).

**Shortest path with BFS:**
Track distance as you enqueue, or track the parent of each node to reconstruct the path:
```python
dist = {start: 0}
while queue:
    node = queue.popleft()
    for neighbor in graph[node]:
        if neighbor not in dist:
            dist[neighbor] = dist[node] + 1
            queue.append(neighbor)
```

**Time/Space complexity:** O(V + E) — every node and edge is processed at most once.

## Analogy

Imagine dropping a stone into a still pond. Ripples spread outward in perfect circles — all points at distance 1 are hit before any points at distance 2, which are all hit before distance 3.

BFS is that ripple. The source is the stone. The queue holds the current wavefront. Every time you pop a node (the current ripple), you enqueue its unvisited neighbors (the next ripple). By the time you reach your destination, you've taken the minimum number of steps — because ripples can't skip rings.

## Workshop

**File:** `shortest_path.py`

**Problem:** Given an undirected, unweighted graph and two nodes `src` and `dst`, return the length of the shortest path between them. If no path exists, return `-1`.

```
n = 6
edges = [[0,1],[0,2],[1,3],[2,3],[3,4],[4,5]]

Graph:  0 - 1
        |   |
        2 - 3 - 4 - 5

shortest_path(n, edges, 0, 5)  # 4  (0→1→3→4→5 or 0→2→3→4→5)
shortest_path(n, edges, 0, 4)  # 3  (0→1→3→4)
shortest_path(n, edges, 0, 0)  # 0  (already there)
```

What if node 5 has no connection to the rest?
```
n = 7
edges = [[0,1],[0,2],[1,3],[2,3],[3,4]]
# node 5 and 6 are isolated

shortest_path(n, edges, 0, 5)  # -1 (no path)
```

Implement `shortest_path(n, edges, src, dst)`.

**Constraints:**
- 1 ≤ n ≤ 10⁴
- edges contains undirected edges as [u, v]
- 0 ≤ src, dst < n

## Acceptance Criteria / Edge Cases

- `src == dst` → `0`.
- Direct edge between src and dst → `1`.
- No path exists → `-1`.
- Disconnected graph — BFS from `src` won't reach `dst`.
- Graph with cycles — `visited` set prevents re-visiting.
- Must build the adjacency list from the edge list — don't assume it's provided.

## Complexity Target

- O(V + E) time.
- O(V) space for the visited set and queue.

## Common Mistakes

- Marking visited *when popping* instead of *when enqueuing* — this causes nodes to be enqueued multiple times, degrading to O(E²) in dense graphs and potentially giving wrong distances.
- Returning the path length one step off (forgetting to initialize `dist[src] = 0`).
- Not handling `src == dst` before starting BFS.
- Using a list's `.pop(0)` for the queue (O(n) per pop) instead of `deque.popleft()` (O(1)).

## Interview vs Fundamentals Note

**Fundamentals:** BFS's level-by-level property is the reason it finds shortest paths. Internalize this: "BFS processes all nodes at distance k before any node at distance k+1." This makes it the go-to for any "minimum steps/hops/moves" question on unweighted graphs.

**Interview prep:** BFS shortest path is a building block for many harder problems — word ladder (treat each word as a node, edges to words differing by one letter), 01 matrix (BFS from all 0s simultaneously), walls and gates. All use the same template. The "multi-source BFS" variant (start with multiple sources in the queue) is a key technique to know.

## Bridge

BFS finds shortest paths by exploring outward layer by layer. Next: DFS — explores as deep as possible before backtracking, enabling a different class of graph problems like connected components and cycle detection.
