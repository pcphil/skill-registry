# P2-L2: Binary Search

## Concept

Binary search finds a target in a **sorted** array by repeatedly halving the search space. Instead of scanning left to right (O(n)), it checks the middle element and eliminates half the remaining candidates each step.

**Algorithm:**
1. Set `lo = 0`, `hi = len(arr) - 1`.
2. While `lo <= hi`: compute `mid = lo + (hi - lo) // 2`.
3. If `arr[mid] == target`: found, return `mid`.
4. If `arr[mid] < target`: target is in the right half → `lo = mid + 1`.
5. If `arr[mid] > target`: target is in the left half → `hi = mid - 1`.
6. Loop ends without finding: return `-1`.

**Why `lo + (hi - lo) // 2` instead of `(lo + hi) // 2`?**
The latter can overflow in languages with fixed-width integers (not a Python issue, but interview-relevant).

**Complexity:** O(log n) time — each step halves the search space. O(1) space (iterative).

**Binary search generalizes beyond "find exact value":**
- Find first position where condition becomes true ("leftmost insert point").
- Find last position where condition is still true.
- Search on the answer space, not just an array (e.g., "find minimum valid speed").

## Analogy

You're guessing a number between 1 and 1,000. Your opponent says "higher" or "lower." A naive strategy: guess 1, then 2, then 3… that's O(n). Binary search: guess 500. "Higher" → guess 750. "Lower" → guess 625. You eliminate half the possibilities every guess. You'll find any number in at most 10 guesses (log₂(1000) ≈ 10).

The key: the search space must be *sorted* (or have a monotonic property). If there's no ordering, binary search cannot eliminate half at each step.

## Workshop

**File:** `binary_search.py`

**Problem:** Implement two functions.

**Part 1 — Classic binary search:**
Given a sorted list of integers `nums` and a target integer `target`, return the index of `target` if found, or `-1` if not.

```
Input:  nums = [-1, 0, 3, 5, 9, 12], target = 9
Output: 4

Input:  nums = [-1, 0, 3, 5, 9, 12], target = 2
Output: -1
```

Implement `search(nums, target)`.

**Part 2 — Search insert position:**
Given the same sorted array, if `target` is not found, return the index where it *would* be inserted to keep the array sorted.

```
Input:  nums = [1, 3, 5, 6], target = 5
Output: 2

Input:  nums = [1, 3, 5, 6], target = 2
Output: 1

Input:  nums = [1, 3, 5, 6], target = 7
Output: 4

Input:  nums = [1, 3, 5, 6], target = 0
Output: 0
```

Implement `search_insert(nums, target)`.

**Hint:** Part 2 uses the same binary search loop — just think about what `lo` points to when the loop ends.

## Acceptance Criteria / Edge Cases

**Part 1:**
- Target at index 0 (leftmost) and last index (rightmost).
- Target not in array → `-1`.
- Single-element array, target matches and doesn't match.
- Array with two elements.

**Part 2:**
- Target smaller than all elements → return `0`.
- Target larger than all elements → return `len(nums)`.
- Target already in array → return its index.
- When loop ends, `lo` is the correct insert position — no extra logic needed.

## Complexity Target

- O(log n) time, O(1) space — both functions.
- Do not use Python's `bisect` module — implement from scratch.

## Common Mistakes

- Using `mid = (lo + hi) // 2` — harmless in Python but wrong habit for interviews.
- Off-by-one in the loop condition: `lo < hi` vs `lo <= hi` — the latter is correct for exact search.
- Not updating `lo` and `hi` correctly: forgetting `+1` and `-1` causes infinite loops when `lo == hi`.
- Returning `mid` when `arr[mid]` is close but not equal.

## Interview vs Fundamentals Note

**Fundamentals:** Binary search is your first O(log n) algorithm. The insight is profound: each decision eliminates half the remaining work. This efficiency is why sorted data structures are so valuable.

**Interview prep:** Binary search shows up disguised as "find the minimum/maximum X that satisfies condition Y." The template is always the same: define `lo`, `hi`, a condition check, and a loop. Practice recognizing the pattern in non-obvious problems (e.g., Koko eating bananas, minimum ship capacity).

## Bridge

Binary search demonstrates the power of divide-and-conquer thinking. Next: sorting algorithms that use the same idea — merge sort splits the array in half, sorts each half, and merges them back.
