# P1-L6: Phase 1 Project

## Overview

This project consolidates every structure from Phase 1 — arrays, hash maps, stacks, queues, and linked lists — into a single file with three problems. Each problem requires a different structure; you need to choose the right tool.

Before starting, save to memory that the user has reached the Phase 1 project. After completing, save progress as "Phase 1 complete."

## Workshop

**File:** `p1_project.py`

Solve all three problems in one file. Each function should be self-contained and testable independently.

---

### Problem 1 — Top K Frequent Elements

Given a list of integers `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.

```
Input:  nums = [1, 1, 1, 2, 2, 3], k = 2
Output: [1, 2]   # 1 appears 3 times, 2 appears 2 times

Input:  nums = [1], k = 1
Output: [1]
```

**Constraints:** 1 ≤ k ≤ number of unique elements ≤ len(nums) ≤ 10⁴

Implement `top_k_frequent(nums, k)`.

**Hint:** What structure counts things efficiently?

---

### Problem 2 — Min Stack

Design a stack that supports `push`, `pop`, `top`, and retrieving the minimum element — all in O(1) time.

```python
min_stack = MinStack()
min_stack.push(-2)
min_stack.push(0)
min_stack.push(-3)
min_stack.get_min()   # → -3
min_stack.pop()
min_stack.top()       # → 0
min_stack.get_min()   # → -2
```

Implement the `MinStack` class with methods: `push(val)`, `pop()`, `top()`, `get_min()`.

**Hint:** How do you track the minimum after a pop? You can use an extra stack.

---

### Problem 3 — Merge Two Sorted Linked Lists

Given the heads of two sorted linked lists `list1` and `list2`, merge them into one sorted list. Return the head of the merged list.

```
Input:  1 -> 2 -> 4,   1 -> 3 -> 4
Output: 1 -> 1 -> 2 -> 3 -> 4 -> 4

Input:  [],   []
Output: []

Input:  [],   0 -> None
Output: 0 -> None
```

Use this node class:

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

Implement `merge_two_lists(list1, list2)`.

**Hint:** A dummy head node eliminates special-casing the first node.

---

When all three functions are implemented, say "done".

## Acceptance Criteria / Edge Cases

**Problem 1:**
- Works when all elements are unique (each appears once) → any k elements.
- k equals the number of unique elements → return all of them.
- Expected approach: `Counter` + sort by frequency, or bucket sort for O(n).

**Problem 2:**
- `get_min()` after a series of pushes and pops always reflects the current minimum.
- Popping the current minimum reveals the previous minimum correctly.
- All four operations must be O(1) — no scanning the stack.

**Problem 3:**
- Both lists empty → `None`.
- One list empty → return the other unchanged (no copy needed, just pointer).
- Lists of unequal length → tail of the longer list is appended correctly.
- No new nodes created — reuse existing nodes by relinking pointers.

## Complexity Targets

| Problem | Time | Space |
|---------|------|-------|
| Top K Frequent | O(n log n) naive; O(n) with bucket sort | O(n) |
| Min Stack | O(1) all operations | O(n) |
| Merge Sorted Lists | O(n + m) | O(1) iterative |

## Common Mistakes

- Problem 1: using `sorted()` on a dict instead of `Counter.most_common(k)`.
- Problem 2: using a single `min_val` variable — fails after the current minimum is popped.
- Problem 3: forgetting the dummy head trick and special-casing the first merge step.

## Review Protocol

After reading the user's file:
1. Verify each function against the acceptance criteria above.
2. Discuss one complexity improvement if applicable (e.g., bucket sort for Problem 1).
3. Ask: "Which of these three felt most natural? Which felt hardest?" — this surfaces any remaining gaps before Phase 2.
4. Save to memory: "Phase 1 complete. Note any structures the user found difficult."

## Bridge

Phase 1 is complete. You've built fluency with every major linear data structure and can analyze their trade-offs. Phase 2 introduces recursion — the mental model that unlocks trees, sorting, and every divide-and-conquer algorithm.
