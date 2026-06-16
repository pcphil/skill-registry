# P2-L4: Trees & Traversals

## Concept

A tree is a hierarchical structure of nodes where each node has a value and zero or more **children**. A **binary tree** restricts each node to at most two children (left and right).

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

**Key vocabulary:**
- **Root** — the top node (no parent).
- **Leaf** — a node with no children.
- **Height** — longest path from root to a leaf.
- **Depth** — distance from root to a node.
- A tree with n nodes has exactly n-1 edges.

**Traversals — four ways to visit every node:**

| Traversal | Order | Use case |
|-----------|-------|----------|
| Inorder (L, Root, R) | left → node → right | BST: produces sorted output |
| Preorder (Root, L, R) | node → left → right | Copy/serialize a tree |
| Postorder (L, R, Root) | left → right → node | Delete a tree, evaluate expressions |
| Level-order (BFS) | level by level, left to right | Shortest path, level-based problems |

DFS traversals (in/pre/post) use the **call stack** (recursive) or an explicit **stack** (iterative).
Level-order uses a **queue** (`collections.deque`).

**Complexity for all traversals:** O(n) time (visit every node once), O(h) space for DFS (h = height, O(n) worst case for skewed tree, O(log n) for balanced), O(w) space for BFS (w = max width).

## Analogy

A company org chart is a tree. The CEO is the root. VPs are children of the CEO. Directors are children of VPs, and so on. Employees with no direct reports are leaves.

**Inorder traversal** on an org chart: go as deep left as possible, report, come back up. It's like reading the org chart column by column, left to right.

**Level-order traversal**: read the org chart row by row — CEO first, then all VPs, then all Directors. A queue is natural: process one level, enqueue its children, repeat.

**Postorder**: evaluate from the bottom up — you need all employees' work done before a manager can summarize it.

## Workshop

**File:** `tree_traversal.py`

**Problem:** Given the root of a binary tree, return the nodes' values in all four traversal orders.

```
Tree:
        1
       / \
      2   3
     / \
    4   5

Inorder:    [4, 2, 5, 1, 3]
Preorder:   [1, 2, 4, 5, 3]
Postorder:  [4, 5, 2, 3, 1]
Level-order: [[1], [2, 3], [4, 5]]   # grouped by level
```

Use this node class and tree builder:

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

Implement four functions:

```python
def inorder(root):    # returns list
def preorder(root):   # returns list
def postorder(root):  # returns list
def level_order(root):  # returns list of lists, one per level
```

Test with the tree above (build it manually with `TreeNode`).

## Acceptance Criteria / Edge Cases

- Empty tree (`root = None`) → each function returns `[]`.
- Single node → inorder/preorder/postorder return `[val]`; level_order returns `[[val]]`.
- Left-skewed tree (each node has only a left child) — all traversals work.
- Right-skewed tree — all traversals work.
- Level-order returns a **list of lists**, not a flat list.

## Complexity Target

- All four traversals: O(n) time.
- DFS (in/pre/post): O(h) space — O(log n) balanced, O(n) worst case.
- Level-order: O(w) space — O(n) worst case (last level can have n/2 nodes).

## Common Mistakes

- Inorder: writing `root → left → right` (that's preorder) instead of `left → root → right`.
- Level-order: appending all nodes to one flat list instead of grouping by level. Fix: snapshot `len(queue)` at the start of each level loop.
- Not handling `None` children before recursing: `if root.left: inorder(root.left)` — cleaner to guard at the top: `if not root: return []`.
- Confusing tree height O(log n) for balanced vs O(n) for skewed — both are valid trees.

## Interview vs Fundamentals Note

**Fundamentals:** Trees are the gateway to thinking recursively about hierarchical data. Every tree function follows the same shape: handle the base case (`root is None`), recurse left, recurse right, combine. Internalize this pattern.

**Interview prep:** Level-order traversal (BFS on a tree) is extremely common. Know it cold. Inorder is essential for BST problems (next lesson). Preorder is used to serialize trees. The queue-based level-order template is reused for graph BFS.

## Bridge

You can now traverse any binary tree. Next: Binary Search Trees — trees where the left/right ordering property enables O(log n) search, insert, and delete.
