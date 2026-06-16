# P2-L1: Recursion Fundamentals

## Concept

Recursion is a function that calls itself to solve a smaller version of the same problem. Every recursive solution has two parts:

1. **Base case** — the simplest input where the answer is known directly (no recursive call). Without this, you get infinite recursion.
2. **Recursive case** — reduce the problem toward the base case and call the function on the smaller version.

**The call stack:** each recursive call is pushed onto the call stack. When a base case is reached, the stack unwinds — each frame returns its result to the frame below it. This is why recursion uses O(n) space for n levels of depth.

**Recurrence relations** describe the cost:
- `T(n) = T(n-1) + O(1)` → O(n) total (linear recursion, e.g. counting down)
- `T(n) = 2T(n/2) + O(n)` → O(n log n) (divide and conquer, e.g. merge sort)
- `T(n) = 2T(n-1) + O(1)` → O(2ⁿ) (exponential, e.g. naive Fibonacci)

**Memoization:** cache results of subproblems to avoid redundant work. Converts O(2ⁿ) naive Fibonacci to O(n).

## Analogy

Imagine you're in a movie theater and ask the person in front of you what row they're in. They don't know, so they ask the person in front of *them*. This continues until the person in row 1 says "row 1." Then the answer propagates back: "row 2," "row 3," until it reaches you.

That's recursion: delegate the question to a smaller version of itself, wait for the answer to bubble back up. The person in row 1 is the base case.

The call stack is the chain of people waiting for an answer. If the theater has 10,000 rows, 10,000 people are waiting — O(n) memory.

## Workshop

**File:** `fibonacci.py`

**Problem:** Implement three versions of Fibonacci and observe how they differ in performance.

Fibonacci: F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)

```
fib(0) = 0
fib(1) = 1
fib(6) = 8
fib(10) = 55
```

Implement all three functions in `fibonacci.py`:

```python
# Version 1: naive recursion
def fib_naive(n):
    pass

# Version 2: memoized recursion (use a dict or functools.lru_cache)
def fib_memo(n, memo={}):
    pass

# Version 3: iterative (bottom-up)
def fib_iter(n):
    pass
```

After implementing, add a timing test at the bottom:

```python
import time

for fn, label in [(fib_naive, "naive"), (fib_memo, "memo"), (fib_iter, "iter")]:
    start = time.time()
    result = fn(35)
    elapsed = time.time() - start
    print(f"{label}: fib(35) = {result}, time = {elapsed:.4f}s")
```

Say "done" when all three functions return correct results.

## Acceptance Criteria / Edge Cases

- `fib(0)` → 0, `fib(1)` → 1 — base cases handled.
- `fib_naive(35)` is noticeably slow (seconds); `fib_memo` and `fib_iter` are near-instant.
- All three return the same values.
- `fib_memo` must not recompute subproblems — verify by adding a print inside and observing it runs only once per unique n.

## Complexity Target

| Version | Time | Space |
|---------|------|-------|
| `fib_naive` | O(2ⁿ) | O(n) call stack |
| `fib_memo` | O(n) | O(n) memo dict + call stack |
| `fib_iter` | O(n) | O(1) |

## Common Mistakes

- Missing the base case or getting it wrong (`n == 0` vs `n <= 1`).
- Mutable default argument `memo={}` is shared across calls — fine here intentionally, but explain the footgun.
- Returning `fib(n-1) + fib(n-2)` without storing in memo first (memo check must come before the recursive call).
- Iterative version: starting loop at wrong index or not initializing `a, b = 0, 1` correctly.

## Interview vs Fundamentals Note

**Fundamentals:** Recursion is a mental model, not a trick. Practice tracing the call stack on paper for small inputs (n=4). Once you can visualize the tree of calls, you can reason about any recursive algorithm.

**Interview prep:** Memoization is the bridge to dynamic programming. Every DP problem starts as "naive recursion that's too slow" → add a cache → done. Fibonacci is the simplest example of this exact transformation.

## Bridge

You understand how functions call themselves and how to cache results. Next: binary search — a recursive algorithm that cuts the problem in half each step, achieving O(log n).
