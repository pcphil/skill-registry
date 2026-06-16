# P2-L3: Sorting — Merge Sort & Quick Sort

## Concept

Sorting is a foundational operation. Python's built-in `sorted()` and `.sort()` use Timsort (O(n log n)), but understanding *why* O(n log n) is the practical lower bound for comparison sorts — and how to implement two canonical algorithms — sharpens your divide-and-conquer thinking.

**Merge Sort — divide, sort, merge:**
1. Split array in half recursively until you have arrays of size 1 (already sorted).
2. Merge two sorted halves into one sorted array (O(n) per merge).
3. Recurrence: T(n) = 2T(n/2) + O(n) → O(n log n) always.
- Stable sort (preserves relative order of equal elements).
- O(n) extra space for the merge step.

**Quick Sort — partition around a pivot:**
1. Choose a pivot element.
2. Partition: move all elements smaller than pivot to the left, larger to the right.
3. Recursively sort left and right partitions.
4. Average: O(n log n). Worst case: O(n²) if the pivot is always the smallest/largest (sorted input + bad pivot choice).
- In-place: O(log n) stack space on average.
- Not stable.

| | Merge Sort | Quick Sort |
|--|-----------|------------|
| Time (avg) | O(n log n) | O(n log n) |
| Time (worst) | O(n log n) | O(n²) |
| Space | O(n) | O(log n) |
| Stable | Yes | No |

**When to use which:** Merge sort when stability matters or worst-case guarantees are required. Quick sort when memory is tight and input isn't adversarially sorted.

## Analogy

**Merge sort:** You have a pile of unsorted index cards. Split the pile in half, hand half to a friend. You each keep splitting until everyone has one card (trivially sorted). Then you merge pairs of sorted piles back together by interleaving in order. The merge is easy because both piles are already sorted — you just compare the top cards.

**Quick sort:** Pick one card as the "pivot." Slide every card smaller than it to the left pile, every card larger to the right pile. Now the pivot is in its final position. Repeat the same process on each pile independently, choosing a new pivot each time.

## Workshop

**File:** `sort_array.py`

**Problem:** Implement both sorting algorithms from scratch.

```
Input:  [5, 2, 3, 1]
Output: [1, 2, 3, 5]

Input:  [5, 1, 1, 2, 0, 0]
Output: [0, 0, 1, 1, 2, 5]
```

Implement in `sort_array.py`:

```python
def merge_sort(nums):
    # Return a new sorted list
    pass

def quick_sort(nums):
    # Return a new sorted list (simplest version: not in-place)
    pass

# Test both
arr = [5, 2, 3, 1, 8, 0, 4]
print(merge_sort(arr[:]))   # [0, 1, 2, 3, 4, 5, 8]
print(quick_sort(arr[:]))   # [0, 1, 2, 3, 4, 5, 8]
```

For quick sort, a clean functional approach is acceptable (not in-place): partition into `left`, `mid`, `right` lists around a pivot, then recurse and concatenate. Focus on understanding the algorithm, not optimizing memory.

## Acceptance Criteria / Edge Cases

- Empty list → `[]`.
- Single element → `[x]`.
- Already sorted → same output.
- Reverse sorted → correct output.
- Duplicates → stable for merge sort (equal elements maintain original order).
- Both functions must not modify the input array.

## Complexity Target

| Function | Time | Space |
|----------|------|-------|
| `merge_sort` | O(n log n) | O(n) |
| `quick_sort` (functional) | O(n log n) avg | O(n) partitions + O(log n) stack |

## Common Mistakes

- Merge sort: forgetting to handle the base case `len(nums) <= 1`.
- Merge sort: mutating the input instead of building a new list in the merge step.
- Merge sort: off-by-one in `mid = len(nums) // 2` — one side gets the extra element, that's fine.
- Quick sort: choosing the first element as pivot on sorted input causes O(n²) — choosing `nums[len(nums)//2]` is safer.
- Quick sort: including the pivot in both partitions creates an infinite loop on duplicates — isolate pivot as its own list.

## Interview vs Fundamentals Note

**Fundamentals:** The goal is to viscerally understand O(n log n) — it comes from doing O(n) work at each of O(log n) levels of recursion. Draw the recursion tree. Count the work at each level.

**Interview prep:** You'll rarely be asked to implement merge sort in an interview, but the merge step appears constantly (merge k sorted lists, merge intervals). Quick sort's partition logic underlies the "quick select" algorithm for finding the k-th largest element in O(n) average.

## Bridge

You can now sort arrays and understand why O(n log n) is efficient. Next: trees — a non-linear structure where divide-and-conquer thinking becomes the natural traversal pattern.
