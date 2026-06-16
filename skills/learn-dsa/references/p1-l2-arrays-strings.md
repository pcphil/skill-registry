# P1-L2: Arrays & Strings + Two-Pointer Technique

## Concept

A Python list is a dynamic array — a contiguous block of memory that holds references to objects. Key operations and their costs:

| Operation | Big-O | Why |
|-----------|-------|-----|
| Index access `a[i]` | O(1) | Direct memory offset |
| Append `a.append(x)` | O(1) amortized | Doubles capacity when full |
| Insert at middle `a.insert(i, x)` | O(n) | Shifts all elements right |
| Delete at middle `del a[i]` | O(n) | Shifts all elements left |
| Search `x in a` | O(n) | Must scan every element |
| Slice `a[i:j]` | O(k) | Copies k elements |

Strings in Python are **immutable** — every `+` concatenation allocates a new string. Use `"".join(parts)` when building strings in a loop.

**Two-pointer technique:** Place one pointer at the start and one at the end (or both at the start moving at different speeds). Move them toward each other based on a condition. Turns many O(n²) brute-force problems into O(n).

## Analogy

Picture a row of lockers numbered 1–100. You can open any locker instantly because you know its number — that's O(1) access. But if you need to insert a new locker in the middle, every locker to the right has to shuffle one position — that's O(n).

For the two-pointer: imagine two people walking toward each other on a bridge. They don't need to compare every possible pair of positions — they just keep walking and meet in the middle. One pass, O(n).

## Workshop

**File:** `two_sum.py`

**Problem:** Given a list of integers `nums` and a target integer `target`, return the indices of the two numbers that add up to `target`. You may assume exactly one solution exists and you may not use the same element twice.

```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]   # nums[0] + nums[1] = 2 + 7 = 9

Input:  nums = [3, 2, 4], target = 6
Output: [1, 2]

Input:  nums = [3, 3], target = 6
Output: [0, 1]
```

**Constraints:**
- 2 ≤ len(nums) ≤ 10⁴
- -10⁹ ≤ nums[i] ≤ 10⁹
- Exactly one valid answer exists

Implement `two_sum(nums, target)` in `two_sum.py`. Start with the brute-force approach first, then see if you can improve it.

## Acceptance Criteria / Edge Cases

- Returns a list of exactly two indices `[i, j]` where `i != j`.
- Works when the answer is at the front, back, or middle of the list.
- Works with negative numbers.
- Works when both indices are adjacent (`[3, 3], target=6`).
- Brute force: O(n²) — nested loop checking every pair.
- Optimal: O(n) using a hash map (preview of next lesson — if they find this, celebrate it).

## Complexity Target

- Brute force: O(n²) time, O(1) space — acceptable first pass.
- Optimal: O(n) time, O(n) space — using a complement map.

## Common Mistakes

- Returning values instead of indices.
- Using the same index twice: `nums[i] + nums[i]` when `target == 2 * nums[i]`.
- Off-by-one errors in nested loop bounds (`range(len(nums))` vs `range(len(nums)-1)`).
- String concatenation in a loop: `result = result + str(n)` — this is O(n²). Teach `"".join()`.

## Interview vs Fundamentals Note

**Fundamentals:** Two Sum teaches you to think past the obvious nested loop. The interesting question is: what information from previous iterations can I *remember* to avoid re-scanning?

**Interview prep:** Two Sum is the gateway problem for hash-map patterns. Interviewers expect you to: (1) state the brute-force and its complexity, (2) identify the bottleneck, (3) propose the hash-map optimization. Practice narrating this transition.

## Bridge

You solved Two Sum with a nested loop — but the optimal solution uses a hash map. Next lesson: hash maps and sets, the most powerful constant-time lookup structure in your toolkit.
