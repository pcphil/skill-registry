# P1-L3: Hash Maps & Sets

## Concept

A hash map (`dict` in Python) maps keys to values using a **hash function** — a function that converts a key into an array index. A hash set (`set`) is the same idea but stores only keys, no values.

Key operations and their costs (average case):

| Operation | dict / set | Big-O |
|-----------|------------|-------|
| Insert `d[k] = v` | O(1) | Hash computed, slot found |
| Lookup `d[k]` | O(1) | Same hash computation |
| Delete `del d[k]` | O(1) | Hash to slot, remove |
| Membership `k in d` | O(1) | Hash to slot, check |
| Iterate | O(n) | Must visit all slots |

**Worst case is O(n)** due to hash collisions, but Python's implementation makes this extremely rare in practice.

**When to reach for a hash map:** Any time you need O(1) lookup instead of O(n) scan. Common patterns:
- Count frequencies: `counts[x] = counts.get(x, 0) + 1`
- Check membership without caring about order: use a `set`
- Memoize seen values: `seen = set(); seen.add(x)`
- Store complements/pairs: the Two Sum optimal solution

## Analogy

A hash map is a coat check at a theater. You hand over your coat, get a numbered ticket. Later you hand the ticket back and instantly get your coat — O(1). The attendant doesn't search through every coat; the ticket number encodes exactly where it's stored.

A hash set is the same system, but you only care whether your coat was checked in — not what value is attached to it. "Has this coat been checked?" is answered in one lookup.

The risk: two people could theoretically get the same ticket number (a collision). The coat check has a system for that — Python's `dict` does too, transparently.

## Workshop

**File:** `contains_duplicate.py`

**Problem:** Given a list of integers `nums`, return `True` if any value appears at least twice, and `False` if every element is distinct.

```
Input:  nums = [1, 2, 3, 1]
Output: True

Input:  nums = [1, 2, 3, 4]
Output: False

Input:  nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
Output: True
```

**Constraints:**
- 1 ≤ len(nums) ≤ 10⁵
- -10⁹ ≤ nums[i] ≤ 10⁹

Implement `contains_duplicate(nums)` in `contains_duplicate.py`. There are at least two valid approaches — try to find the most efficient one.

## Acceptance Criteria / Edge Cases

- Returns `True` as soon as a duplicate is found (early exit is better).
- Works on a single-element list → `False`.
- Works on all-same elements → `True`.
- Works on negative numbers.
- Sorting approach: O(n log n) time, O(1) space — valid but not optimal.
- Hash set approach: O(n) time, O(n) space — optimal.

## Complexity Target

- O(n) time, O(n) space — using a `set` to track seen values.

## Common Mistakes

- Using `nums.count(x) > 1` inside a loop — that's O(n²): `count()` is O(n) and it's called n times.
- Forgetting that `list(set(nums))` loses order — fine here, but important to know.
- Returning the duplicate value instead of a boolean.
- Not short-circuiting: continuing to iterate after a duplicate is found.

## Interview vs Fundamentals Note

**Fundamentals:** The key insight is the space-time trade-off — you spend O(n) extra memory to buy O(n) time instead of O(n²). This trade-off recurs constantly in DSA.

**Interview prep:** "Sorting vs hash set" is a classic trade-off interviewers probe. Be ready to articulate: "Sorting is O(n log n) and O(1) space; hash set is O(n) and O(n) space. I'd choose hash set if memory isn't constrained because it's faster and gives early exit."

## Bridge

Hash maps give you O(1) lookup at the cost of some memory. Next: stacks and queues — structures that constrain *how* you access data, enabling a powerful class of problems.
