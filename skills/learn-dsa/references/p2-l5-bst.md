# P2-L5: Binary Search Trees (BST)

## Concept

A Binary Search Tree is a binary tree with one critical ordering property: for every node N,
- All values in N's **left** subtree are **less than** N's value.
- All values in N's **right** subtree are **greater than** N's value.

This property holds recursively for every node in the tree.

**Operations and their complexity:**

| Operation | Average | Worst Case |
|-----------|---------|-----------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |

Worst case O(n) occurs when the tree is **unbalanced** — inserting sorted values produces a linked list. Balanced BSTs (AVL, Red-Black) guarantee O(log n) always, but implementing them is beyond this curriculum.

**Search algorithm:** Start at root. If target < current: go left. If target > current: go right. If equal: found. If you reach `None`: not in tree.

**Insert algorithm:** Same as search, but when you reach `None`, that's where the new node belongs.

**Inorder traversal of a BST produces a sorted sequence** — a fundamental property used in many problems.

**Delete algorithm (three cases):**
1. Node has no children → remove it (set parent's pointer to `None`).
2. Node has one child → replace node with its child.
3. Node has two children → replace node's value with its **inorder successor** (smallest value in right subtree), then delete the inorder successor.

## Analogy

A BST is a well-organized library. Each shelf (node) has books to its left that come *before* it alphabetically and books to the right that come *after*. To find "Moby Dick," you start at the center shelf. If "M" comes before the center, you go left. You keep narrowing until you find it or reach an empty shelf.

Because of this ordering guarantee, you never need to search every shelf — each comparison eliminates half the remaining shelves. This is why a balanced BST gives O(log n) search: the same guarantee as binary search, but in a dynamic structure that supports fast insert and delete.

## Workshop

**File:** `bst_insert_search.py`

**Problem:** Implement insert and search for a BST, then use them to validate a BST.

Use this node class:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

**Part 1 — Insert:**
Insert a value into a BST. Return the root of the modified tree.

```
Insert 5 into:   4          Result:  4
                / \                  / \
               2   7                2   7
                                   /
                                  (5 should go left of 7? No — 5 < 7, so left of 7)
```

Actually: `Insert 5 into [4, 2, 7]` → 5 > 4 → go right → 5 < 7 → go left → empty → place here.

Implement `insert(root, val)`.

**Part 2 — Search:**
Return `True` if `val` exists in the BST, `False` otherwise.

Implement `search(root, val)`.

**Part 3 — Validate BST:**
Given a binary tree root, determine if it is a valid BST.

```
Valid:       2          Invalid:   5
            / \                   / \
           1   3                 1   4
                                    / \
                                   3   6
# Invalid because 4 is in the right subtree of 5, but 4 < 5.
```

Implement `is_valid_bst(root)`.

**Hint for Part 3:** Checking only that `left.val < node.val < right.val` at each node is insufficient. You need to track valid value ranges as you recurse.

## Acceptance Criteria / Edge Cases

**Insert:**
- Insert into empty tree (`root = None`) → new node becomes root.
- Insert duplicate value → acceptable to insert to the right (or ignore; pick one consistently).

**Search:**
- Search empty tree → `False`.
- Search for root value → `True`.
- Value not in tree → `False`.

**Validate BST:**
- Single node → `True`.
- Left child equal to parent → `False` (strict inequality required).
- The "range narrowing" approach: pass `(min_val, max_val)` bounds recursively.
  - Root: `(-inf, +inf)`.
  - Go left: `(min_val, node.val)`.
  - Go right: `(node.val, max_val)`.

## Complexity Target

- Insert and Search: O(h) time — O(log n) balanced, O(n) worst case. O(h) stack space.
- Validate: O(n) time (must check every node), O(h) space.

## Common Mistakes

- Validate BST: checking only immediate children, not propagating bounds down the tree. The classic trick case: a node deep in the right subtree with a value smaller than the root.
- Insert: forgetting to return the root when recursing — `root.left = insert(root.left, val)`.
- Search: using `==` on float nodes without care; generally only integer values in these problems.

## Interview vs Fundamentals Note

**Fundamentals:** BST is where the tree ordering property becomes a superpower. The inorder traversal producing sorted output is a useful fact — it means you can solve "find k-th smallest element in BST" with a simple inorder traversal.

**Interview prep:** Validate BST (Part 3) is a very common interview question specifically because the naive approach (check only immediate children) fails the tricky case. Interviewers use it to test whether you understand the *global* BST property, not just the local one.

## Bridge

BSTs give O(log n) operations on dynamic ordered data. Next: heaps — a different tree-based structure that efficiently tracks the minimum or maximum element as the set changes.
