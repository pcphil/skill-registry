# P3-L3: DFS & Applications

## Concept

**Depth-First Search (DFS)** explores as far as possible along one path before backtracking. It uses the **call stack** (recursive) or an explicit **stack** (iterative).

**Recursive DFS template:**
```python
def dfs(graph, node, visited):
    visited.add(node)
    # process node
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

**Iterative DFS template (using an explicit stack):**
```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        # process node
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

**BFS vs DFS — when to use which:**

| | BFS | DFS |
|-|-----|-----|
| Uses | Queue | Stack / recursion |
| Finds | Shortest path | Any path; exhaustive search |
| Space | O(w) — max width | O(h) — max depth |
| Best for | Shortest path, level-order | Connected components, cycle detection, topological sort, backtracking |

**Key DFS applications:**
- **Connected components:** count distinct subgraphs not connected to each other.
- **Cycle detection:** track nodes in the current recursion path (not just visited).
- **Flood fill / island counting:** DFS on a 2D grid — treat each cell as a node with up to 4 neighbors.

**Grid DFS pattern (common in interviews):**
```python
def dfs_grid(grid, row, col, visited):
    rows, cols = len(grid), len(grid[0])
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return
    if (row, col) in visited or grid[row][col] == '0':
        return
    visited.add((row, col))
    dfs_grid(grid, row+1, col, visited)
    dfs_grid(grid, row-1, col, visited)
    dfs_grid(grid, row, col+1, visited)
    dfs_grid(grid, row, col-1, visited)
```

## Analogy

DFS is like exploring a cave system. You pick one tunnel and go as deep as possible, leaving a trail of breadcrumbs. When you hit a dead end (or a place you've already been), you backtrack to the last junction and try the next unexplored tunnel.

BFS, by contrast, is like a search party that expands outward uniformly — everyone walks one step, then another, then another, staying together as a wavefront.

DFS is better when you want to fully explore one region before checking another — ideal for detecting if two points are in the same connected island, or whether a graph contains a cycle.

## Workshop

**File:** `number_of_islands.py`

**Problem:** Given a 2D grid of `'1'` (land) and `'0'` (water), count the number of islands. An island is surrounded by water and is formed by connecting adjacent land cells horizontally or vertically.

```
Input:
grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1

Input:
grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3
```

**Constraints:**
- 1 ≤ rows, cols ≤ 300
- `grid[i][j]` is `'0'` or `'1'`

Implement `num_islands(grid)` in `number_of_islands.py`.

**Hint:** Iterate every cell. When you find an unvisited `'1'`, that's a new island — run DFS to mark all connected land cells as visited, then increment your count.

**Bonus:** Also implement `num_islands_bfs(grid)` using BFS instead of DFS to see how the two traversals differ in code while producing identical results.

## Acceptance Criteria / Edge Cases

- All water (`'0'`) → `0`.
- All land (one big island) → `1`.
- Diagonal adjacency does not count — only horizontal/vertical.
- 1×1 grid with `'1'` → `1`.
- Multiple isolated single-cell islands → count each one.
- Do not mutate the input grid (use a `visited` set with `(row, col)` tuples, or modify and restore — but prefer not mutating).

## Complexity Target

- O(m × n) time: every cell is visited at most once.
- O(m × n) space: visited set or recursion stack (in the worst case, a snake-shaped island spans the entire grid).

## Common Mistakes

- Mutating the grid (`grid[r][c] = '0'`) as the visited marker — works but is a side effect. Visited set is cleaner.
- Checking bounds *after* accessing the cell (causes IndexError). Check bounds *first* in the DFS guard.
- Counting the same island multiple times by not marking cells as visited before recursing into them.
- Only checking up/down, forgetting left/right (or vice versa) — need all four directions.

## Interview vs Fundamentals Note

**Fundamentals:** Grid problems are graph problems in disguise. Every cell is a node; edges connect horizontally/vertically adjacent cells. Once you see this, the DFS/BFS templates apply directly. Practice this mental translation.

**Interview prep:** Number of Islands is one of the most frequently asked graph interview questions. Know the DFS version cold. Common follow-ups: "What if the grid is too large to fit in memory?" (stream rows), "Count the size of each island" (return from DFS), "Find the largest island" (max of island sizes).

## Bridge

You can now traverse graphs with both BFS and DFS and apply them to real 2D grid problems. Next: the Phase 3 capstone — a multi-problem set that integrates everything from all three phases.
