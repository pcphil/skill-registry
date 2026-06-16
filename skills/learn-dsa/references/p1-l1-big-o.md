# P1-L1: Big-O & Complexity Analysis

## Concept

Big-O notation describes how an algorithm's runtime or memory usage *grows* as the input size `n` increases. It answers the question: "If I double the input, what happens to the cost?"

We ignore constants and lower-order terms because we care about the *shape* of growth, not the exact count. The most common classes, from fastest to slowest:

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | Array index lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Single loop over a list |
| O(n log n) | Linearithmic | Merge sort |
| O(n²) | Quadratic | Nested loops |
| O(2ⁿ) | Exponential | Recursive subsets |

**Space complexity** follows the same rules but counts memory allocated, not operations executed.

## Analogy

Imagine you're searching for a name in a phone book.

- **O(1)**: You already know the page number — flip straight to it.
- **O(log n)**: Open the middle, decide left or right, repeat — classic binary search through the alphabet.
- **O(n)**: Read every name from page 1 until you find it.
- **O(n²)**: For every name, compare it against every other name to find duplicates.

The phone book doesn't change — only your *strategy* determines whether it takes one second or an hour.

## Workshop

**File:** `big_o.py`

**Problem:** Classify the runtime of each of the following functions. For each, write a comment stating the Big-O time complexity and a one-line reason why.

```python
def func_a(n):
    return n * 2

def func_b(items):
    total = 0
    for item in items:
        total += item
    return total

def func_c(items):
    for i in items:
        for j in items:
            print(i, j)

def func_d(items):
    return items[0]

def func_e(n):
    if n <= 1:
        return n
    return func_e(n - 1) + func_e(n - 2)
```

Add your classifications as comments above each function, then say "done".

## Acceptance Criteria / Edge Cases

- `func_a` → O(1): single arithmetic operation, no loop.
- `func_b` → O(n): one loop iterating over all items.
- `func_c` → O(n²): nested loop, each runs n times.
- `func_d` → O(1): direct index access.
- `func_e` → O(2ⁿ): each call spawns two recursive calls; tree doubles each level.

Common mistake: calling `func_e` O(n) because it "counts down from n." Trace the call tree — two branches per call means exponential growth.

## Complexity Target

This is a classification exercise, not a coding problem. No runtime to optimize.

## Common Mistakes

- Confusing O(n + n) = O(2n) with O(n²): two *separate* loops is O(n), not O(n²). Nested loops are O(n²).
- Ignoring the recursive call tree: always draw it for recursive functions.
- Counting lines of code instead of how many times they execute.

## Interview vs Fundamentals Note

**Fundamentals:** Focus on understanding why each class exists and what it *feels* like at scale. Build the habit of asking "what happens if n = 1,000,000?" before writing a loop.

**Interview prep:** You'll be expected to state Big-O for every solution you write — time *and* space. Practice saying it out loud: "This runs in O(n) time and O(1) space because…"

## Bridge

You can now read code and reason about its cost. Next: arrays and strings — the most common data structure in every interview and codebase.
