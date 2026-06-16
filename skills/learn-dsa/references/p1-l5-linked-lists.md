# P1-L5: Linked Lists

## Concept

A linked list is a sequence of **nodes**, where each node holds a value and a pointer to the next node. Unlike arrays, nodes are not stored contiguously in memory — each node knows only its own value and where to find the next one.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

Key operations and their costs:

| Operation | Big-O | Why |
|-----------|-------|-----|
| Access by index | O(n) | Must traverse from head |
| Insert at head | O(1) | Redirect one pointer |
| Insert at tail | O(n) | Must traverse to find tail |
| Delete a node (given node) | O(1) | Redirect predecessor's pointer |
| Delete a node (given value) | O(n) | Must find it first |
| Search | O(n) | Linear scan |

**Singly linked list:** each node has `val` and `next`.
**Doubly linked list:** each node has `val`, `next`, and `prev`. Enables O(1) deletion without needing the predecessor.

**Classic patterns:**
- **Two-pointer (fast/slow):** detect cycles, find middle node, find nth from end.
- **Dummy head node:** simplifies edge cases when the head itself may change.
- **Pointer reversal:** rebuild links in-place without extra memory.

## Analogy

A linked list is a treasure hunt. Each clue (node) tells you: "the value is X, and the next clue is hidden at location Y." You can only move forward by following clues — you can't jump to clue #5 directly without following the chain from clue #1.

This makes insertion easy: drop a new clue anywhere and update two neighbors' directions. But finding a specific clue? You walk from the beginning every time.

Compare to an array (lockers with numbers): you can open locker #5 immediately. But inserting a new locker in the middle means renumbering everything. Different trade-offs, different problems.

## Workshop

**File:** `reverse_linked_list.py`

**Problem:** Given the head of a singly linked list, reverse the list and return the new head.

```
Input:  1 -> 2 -> 3 -> 4 -> 5 -> None
Output: 5 -> 4 -> 3 -> 2 -> 1 -> None

Input:  1 -> 2 -> None
Output: 2 -> 1 -> None

Input:  1 -> None
Output: 1 -> None
```

The `ListNode` class is provided below. Define it in your file:

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

Implement `reverse_list(head)` that returns the new head node. Also include a helper to build and print lists so you can test manually:

```python
def build_list(values):
    dummy = ListNode(0)
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def print_list(head):
    vals = []
    while head:
        vals.append(str(head.val))
        head = head.next
    print(" -> ".join(vals))
```

## Acceptance Criteria / Edge Cases

- Empty list (`head = None`) → return `None`.
- Single node → return that node unchanged.
- Two nodes → swap correctly.
- After reversal, original head's `next` must be `None` (no cycle).
- Iterative approach: three pointers (`prev`, `curr`, `next_node`), O(1) space.
- Recursive approach: valid, but O(n) call stack space — mention the trade-off.

## Complexity Target

- O(n) time: single pass through all nodes.
- O(1) space (iterative): only a fixed number of pointers.

## Common Mistakes

- Losing the rest of the list by overwriting `curr.next` before saving `next_node`.
- Forgetting to set `prev = None` before the loop — the new tail must point to `None`.
- Off-by-one: returning `curr` instead of `prev` at the end (when the loop ends, `curr` is `None`).
- Confusing "reverse the values" (wrong — don't copy into an array and reverse) with "reverse the pointers" (correct).

## Interview vs Fundamentals Note

**Fundamentals:** Pointer reversal feels awkward at first. Draw it on paper: three boxes (`prev`, `curr`, `next`), advance one step at a time. The key insight is that you need `next_node = curr.next` *before* you sever the link.

**Interview prep:** Reversing a linked list is a building block, not the final boss. Interviewers use it to test pointer fluency. Expect follow-ups: "reverse only nodes k to k+m," "reverse in groups of k." The same three-pointer pattern applies everywhere.

## Bridge

You now have the full linear-structure toolkit: arrays, hash maps, stacks, queues, and linked lists. Next: a Phase 1 project that combines all five in a mixed problem set.
