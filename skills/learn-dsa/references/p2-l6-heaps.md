# P2-L6: Heaps / Priority Queues

## Concept

A **heap** is a complete binary tree with the heap property:
- **Min-heap:** every parent's value ≤ its children's values. Root is always the minimum.
- **Max-heap:** every parent's value ≥ its children's values. Root is always the maximum.

A heap does **not** maintain full sorted order — only the top element is guaranteed to be the min or max. This is sufficient for many problems and enables highly efficient operations.

**Key operations:**

| Operation | Big-O | Why |
|-----------|-------|-----|
| Push (insert) | O(log n) | Bubble up from leaf |
| Pop min/max | O(log n) | Sink down from root |
| Peek min/max | O(1) | Root is always min/max |
| Build heap from list | O(n) | Heapify is amortized linear |

**Python's `heapq` module** implements a **min-heap** using a regular list:

```python
import heapq

h = []
heapq.heappush(h, 3)
heapq.heappush(h, 1)
heapq.heappush(h, 2)
print(heapq.heappop(h))  # 1 (minimum)

# Build from existing list
nums = [3, 1, 4, 1, 5]
heapq.heapify(nums)       # O(n), in-place

# Max-heap trick: negate values
heapq.heappush(h, -val)   # push negated
max_val = -heapq.heappop(h)  # negate when popping
```

**When to reach for a heap:**
- You need repeated access to the current minimum or maximum as the set changes.
- Finding the k-th largest/smallest element.
- Merging k sorted lists.
- Scheduling tasks by priority.

## Analogy

A hospital emergency room uses a priority queue. Patients don't wait in arrival order — they wait by severity. The most critical patient is always seen next, regardless of when they arrived.

When a new patient arrives, staff assess and place them in the correct priority slot (O(log n) — like bubbling up in a heap). When the next patient is called, the most critical one is retrieved instantly (O(1) peek) and removed (O(log n) to restore heap order).

The ER doesn't keep a fully sorted list of all patients — that would be expensive to maintain. It only guarantees that the *top priority* patient is always known. That's the heap guarantee.

## Workshop

**File:** `kth_largest.py`

**Problem:** Given an integer array `nums` and an integer `k`, return the k-th largest element in the array. Note: the k-th largest means the k-th largest in sorted order, not the k-th distinct element.

```
Input:  nums = [3, 2, 1, 5, 6, 4], k = 2
Output: 5

Input:  nums = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4
Output: 4
```

**Constraints:**
- 1 ≤ k ≤ len(nums) ≤ 10⁴
- -10⁴ ≤ nums[i] ≤ 10⁴

Implement `find_kth_largest(nums, k)` in `kth_largest.py`.

**Hint:** A min-heap of size k is more efficient than sorting the entire array. Think about what invariant you want to maintain as you process each element.

**Bonus (optional):** Also implement `top_k_elements(nums, k)` that returns the k largest elements (in any order) using a heap.

## Acceptance Criteria / Edge Cases

- k = 1 → return the maximum.
- k = len(nums) → return the minimum.
- Duplicate values handled correctly: `[3, 2, 3, 1, 2, 4, 5, 5, 6], k=4` → `4` (the 4th largest is 4, not 5).
- Approach using heap of size k: maintain a min-heap; if heap exceeds size k, pop the minimum. At the end, the root of the heap is the k-th largest.

## Complexity Target

| Approach | Time | Space |
|----------|------|-------|
| Sort | O(n log n) | O(1) |
| Max-heap, pop k times | O(n + k log n) | O(n) |
| Min-heap of size k | O(n log k) | O(k) |

The min-heap of size k is optimal when k << n. Discuss all three with the user after reviewing.

## Common Mistakes

- Confusing k-th largest with k-th smallest: `[1,2,3,4,5], k=2` → k-th largest is `4`, not `2`.
- Using a max-heap (negated values) when a min-heap suffices — and forgetting to negate on push and pop.
- Not importing `heapq` or using `heapq.heappush` correctly (the heap is a list, not a class).
- Maintaining heap size > k instead of popping when size exceeds k.

## Interview vs Fundamentals Note

**Fundamentals:** The heap's value is in what it *doesn't* guarantee — full sorting — while still answering "what's the current min/max?" in O(1). This is the right trade-off when you don't need everything sorted, just the top element.

**Interview prep:** "Find k-th largest" and "top k elements" are classic heap interview problems. The min-heap-of-size-k pattern is a reusable template: maintain a window of k elements, always evict the weakest (min) when over capacity. This same pattern applies to "k closest points to origin," "k most frequent elements," and sliding window maximums.

## Bridge

Heaps efficiently track extremes in a dynamic set. Next: the Phase 2 project, which combines recursion, binary search, trees, and heaps into a mixed problem set.
