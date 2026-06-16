# P2-L7: Phase 2 Project

## Overview

This project consolidates Phase 2: recursion, binary search, sorting, tree traversals, BSTs, and heaps. Three problems, each requiring a different Phase 2 concept. Choose the right tool for each.

Before starting, save to memory that the user has reached the Phase 2 project. After completing, save progress as "Phase 2 complete."

## Workshop

**File:** `p2_project.py`

Solve all three problems in one file. Include any required class definitions.

---

### Problem 1 — Maximum Depth of Binary Tree

Given the root of a binary tree, return its maximum depth. The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf.

```
Input:
        3
       / \
      9  20
         / \
        15   7

Output: 3

Input:  root = [1, None, 2]
Output: 2

Input:  root = None
Output: 0
```

Use the standard `TreeNode` class. Implement `max_depth(root)`.

**Hint:** Think recursively. The depth of a tree is 1 + the depth of its deeper subtree.

---

### Problem 2 — Search a 2D Matrix

Write an efficient algorithm to search for a target value in an m × n matrix where:
- Integers in each row are sorted left to right.
- The first integer of each row is greater than the last integer of the previous row.

```
Input:
matrix = [
  [1,  3,  5,  7],
  [10, 11, 16, 20],
  [23, 30, 34, 60]
]
target = 3
Output: True

target = 13
Output: False
```

Implement `search_matrix(matrix, target)`.

**Hint:** The matrix can be treated as a single sorted array of m*n elements. Use binary search on this virtual array. Map a flat index `mid` to row/column with `divmod(mid, n)`.

---

### Problem 3 — Kth Smallest Element in a BST

Given the root of a BST and an integer k, return the k-th smallest value (1-indexed) in the tree.

```
Input:
    3
   / \
  1   4
   \
    2
k = 1
Output: 1

Input:
    5
   / \
  3   6
 / \
2   4
/
1
k = 3
Output: 3
```

Implement `kth_smallest(root, k)`.

**Hint:** What traversal of a BST produces values in sorted order?

---

When all three functions pass their test cases, say "done".

## Acceptance Criteria / Edge Cases

**Problem 1:**
- Empty tree → `0`.
- Single node → `1`.
- Left-skewed tree of depth 5 → `5`.
- Recursive solution preferred; brief mention of iterative BFS alternative.

**Problem 2:**
- Target in first cell, last cell, or exact middle → all return `True`.
- Target not in matrix → `False`.
- 1×1 matrix → works.
- Avoid O(m*n) linear scan — binary search must be O(log(m*n)).

**Problem 3:**
- k = 1 → smallest element (leftmost node in BST).
- k = total nodes → largest element.
- Pure inorder traversal O(n) is acceptable; early-exit inorder O(k) is better — discuss the difference.

## Complexity Targets

| Problem | Time | Space |
|---------|------|-------|
| Max Depth | O(n) | O(h) |
| Search 2D Matrix | O(log(m*n)) | O(1) |
| Kth Smallest BST | O(n) naive / O(k) early exit | O(h) |

## Common Mistakes

- Problem 1: returning `max(left, right)` without adding 1 for the current node.
- Problem 2: doing two nested binary searches (one for row, one for column) instead of treating the whole matrix as a flat sorted array.
- Problem 3: flattening the BST into a sorted list first — valid but O(n) space. Push toward the inorder traversal with a counter approach.

## Review Protocol

After reading the user's file:
1. Verify each function against acceptance criteria above.
2. Discuss the binary search 2D matrix insight explicitly — it's the most non-obvious connection.
3. Ask: "Which Phase 2 concept clicked most? Which felt shakiest?" — surface gaps before Phase 3.
4. Save to memory: "Phase 2 complete. Note any concepts the user found difficult."

## Bridge

Phase 2 is complete. You can now think recursively, search efficiently, sort from first principles, and traverse trees in any order. Phase 3: graphs — the most general structure, where trees are a special case and the problems mirror real-world systems like maps, networks, and social graphs.
