# P3-L4: Capstone

## Overview

The capstone spans all three phases. Four problems — each requires selecting the right structure and algorithm from the full curriculum. There are no hints about which tool to use; that's part of the exercise.

Before starting, confirm in memory that the user has reached the capstone. After completing, save progress as "Capstone complete. Full curriculum finished."

## Workshop

**File:** `p3_capstone.py`

Solve all four problems. Include all required class definitions in the file.

---

### Problem 1 — Longest Consecutive Sequence

Given an unsorted list of integers, return the length of the longest consecutive sequence of integers.

```
Input:  [100, 4, 200, 1, 3, 2]
Output: 4   # sequence: [1, 2, 3, 4]

Input:  [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
Output: 9   # sequence: [0, 1, 2, 3, 4, 5, 6, 7, 8]
```

**Constraint:** Must run in O(n) time.

Implement `longest_consecutive(nums)`.

---

### Problem 2 — Lowest Common Ancestor of a BST

Given a BST and two node values `p` and `q`, find their lowest common ancestor (LCA). The LCA is defined as the deepest node that has both `p` and `q` as descendants (a node is a descendant of itself).

```
BST:
        6
       / \
      2   8
     / \ / \
    0  4 7  9
      / \
     3   5

LCA(2, 8) = 6
LCA(2, 4) = 2   # 2 is its own ancestor
LCA(3, 5) = 4
```

Use the standard `TreeNode` class. Implement `lca_bst(root, p, q)` where `p` and `q` are integer values (not nodes).

---

### Problem 3 — Course Schedule

There are `n` courses labeled 0 to n-1. Some courses have prerequisites: `prerequisites[i] = [a, b]` means you must take course `b` before course `a`. Return `True` if it is possible to finish all courses, or `False` if there is a cycle (making it impossible).

```
n = 2, prerequisites = [[1, 0]]
Output: True   # take 0 then 1

n = 2, prerequisites = [[1, 0], [0, 1]]
Output: False  # 0 requires 1, 1 requires 0 — cycle

n = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: True
```

Implement `can_finish(n, prerequisites)`.

**Hint:** Model courses as nodes and prerequisites as directed edges. When can you not finish all courses?

---

### Problem 4 — Merge K Sorted Lists

You are given a list of k sorted linked lists. Merge all of them into one sorted linked list and return its head.

```
Input:
  1 -> 4 -> 5
  1 -> 3 -> 4
  2 -> 6

Output: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6
```

Use the standard `ListNode` class:
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

Implement `merge_k_lists(lists)`.

---

When all four functions are implemented and tested, say "done".

## Acceptance Criteria / Edge Cases

**Problem 1 — Longest Consecutive:**
- Empty list → `0`.
- All same elements → `1`.
- No consecutive pairs → `1` (single element is a sequence of length 1).
- O(n) solution uses a set: for each number, only start counting if `num-1` is not in the set (it's the start of a sequence).
- Sorting approach is O(n log n) — valid but below the constraint.

**Problem 2 — LCA BST:**
- Uses the BST property: if both `p` and `q` are less than current node, go left; if both greater, go right; otherwise current node is the LCA.
- p and q guaranteed to exist in the tree.
- Works whether p or q is the LCA itself.

**Problem 3 — Course Schedule:**
- Models as a directed graph; cycle detection via DFS with three states: unvisited (0), in-progress (1), done (2).
- If a node in state 1 is encountered during DFS, there's a cycle → return `False`.
- No prerequisites → `True`.
- Self-loop `[0, 0]` → `False`.

**Problem 4 — Merge K Lists:**
- Empty `lists` array → `None`.
- Lists containing `None` entries → skip them.
- Optimal: use a min-heap to always extract the current minimum across all k lists. O(n log k) where n is total nodes.
- Naive: merge two lists at a time, O(n*k) — valid but discuss the improvement.

## Complexity Targets

| Problem | Time | Space |
|---------|------|-------|
| Longest Consecutive | O(n) | O(n) |
| LCA BST | O(h) | O(h) recursion |
| Course Schedule | O(V + E) | O(V + E) |
| Merge K Lists | O(n log k) | O(k) heap |

## Review Protocol

After reading the user's file:
1. Verify each problem against acceptance criteria.
2. For Problem 3, explicitly walk through the cycle detection state machine if they used a different approach.
3. For Problem 4, compare their approach (merge 2-at-a-time vs heap) and discuss the complexity difference.
4. Ask: "Which of the four problems connected the most dots for you? Which concept from the curriculum do you want to revisit?"
5. Save to memory: "Full curriculum complete — [date]. Note any areas for further practice."

## Completion

When the capstone is done, say:

> "You've completed the full learn-dsa curriculum — Big-O through graphs, linear structures through trees, and everything in between. What you've built: the mental models and code patterns for the 20-30% of problems that cover the vast majority of real interviews and codebases.
>
> Where to go next:
> - **Interview prep:** LeetCode Blind 75 — you now have the foundations to tackle all of them.
> - **Deeper DSA:** Dynamic programming, tries, union-find, Dijkstra's algorithm.
> - **In practice:** Recognize these patterns in real code you read and write daily.
>
> Use `/learn-dsa status` to review what you covered, or `/learn-dsa stop` to end the session."
