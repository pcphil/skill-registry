# P1-L4: Stacks & Queues

## Concept

Stacks and queues are **access-restricted** sequences — you can only insert or remove from specific ends. This constraint is the point: it models real ordering problems.

**Stack — Last In, First Out (LIFO):**

| Operation | Python | Big-O |
|-----------|--------|-------|
| Push | `stack.append(x)` | O(1) |
| Pop | `stack.pop()` | O(1) |
| Peek | `stack[-1]` | O(1) |
| Is empty | `len(stack) == 0` | O(1) |

Use a plain Python `list` as a stack. Append to the right, pop from the right.

**Queue — First In, First Out (FIFO):**

| Operation | Python | Big-O |
|-----------|--------|-------|
| Enqueue | `q.append(x)` | O(1) |
| Dequeue | `q.popleft()` | O(1) |
| Peek | `q[0]` | O(1) |
| Is empty | `len(q) == 0` | O(1) |

Use `collections.deque` for queues. `list.pop(0)` is O(n) — never use it as a queue.

**When to reach for a stack:** Problems involving matching pairs, "undo" history, tracking state that must be unwound in reverse order (parsing, DFS).

**When to reach for a queue:** Problems involving processing in arrival order, level-by-level traversal, BFS.

## Analogy

**Stack:** A stack of plates in a cafeteria. You always take from the top (last placed), and you always add to the top. You can't grab the plate from the bottom without removing everything above it.

**Queue:** A line at a coffee shop. First person in line gets served first. You join at the back, you leave from the front. Perfectly fair, strictly ordered.

The power of these structures is the *constraint*. By limiting how you access data, you create predictable ordering guarantees that solve a whole category of problems cleanly.

## Workshop

**File:** `valid_parentheses.py`

**Problem:** Given a string `s` containing only the characters `(`, `)`, `{`, `}`, `[`, `]`, return `True` if the input string is valid. A string is valid if:
1. Open brackets are closed by the same type of bracket.
2. Open brackets are closed in the correct order.
3. Every close bracket has a corresponding open bracket.

```
Input:  s = "()"
Output: True

Input:  s = "()[]{}"
Output: True

Input:  s = "(]"
Output: False

Input:  s = "([)]"
Output: False

Input:  s = "{[]}"
Output: True
```

**Constraints:**
- 1 ≤ len(s) ≤ 10⁴
- `s` consists of parentheses characters only

Implement `is_valid(s)` in `valid_parentheses.py`.

## Acceptance Criteria / Edge Cases

- Empty string → `True` (no unmatched brackets).
- Single character like `"("` → `False` (unclosed).
- String that closes before it opens: `")("` → `False`.
- Deeply nested but valid: `"({[]})"` → `True`.
- Stack must be empty at the end — leftover open brackets are invalid.

## Complexity Target

- O(n) time: one pass through the string.
- O(n) space: stack can hold up to n/2 open brackets.

## Common Mistakes

- Checking only character counts (same number of `(` and `)`) — fails for `")("`  and `"([)]"`.
- Forgetting to check that the stack is empty after the full string is processed.
- Popping from an empty stack when encountering a close bracket — handle this explicitly.
- Using a list and popping from index 0 (O(n)) instead of index -1 (O(1)).

## Interview vs Fundamentals Note

**Fundamentals:** Valid Parentheses is the canonical stack problem because the stack naturally models "I need to remember what I opened, in order, so I can match it when I close." The moment you see "matching pairs in order," reach for a stack.

**Interview prep:** This exact problem appears frequently. Know the solution cold. More importantly, be able to generalize: "I use a stack whenever I need to track state that must be resolved in reverse order." Extend this to: decode strings, asteroid collision, daily temperatures.

## Bridge

Stacks and queues constrain access to create ordering guarantees. Next: linked lists — a foundational structure where understanding *pointers* unlocks a whole class of manipulation problems.
