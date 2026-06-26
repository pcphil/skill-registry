# Build Mode Reference

Reference for SKILL.md. Load this when running a lesson in Build mode.

---

## Task Type Selection

Choose the task type based on the concept and lesson:

| Concept type | Lesson 1–2 | Lesson 3 | Lesson 4–5 |
|---|---|---|---|
| Algorithmic / code | Code task | Code task (edge case input) | Code task or comparison write-up |
| Protocol / systems | Pseudocode or trace task | Trace with failure scenario | Comparison write-up |
| Mathematical | Worked example by hand | Counterexample task | Tradeoff write-up |
| Non-technical | Write-in-own-words task | Counterexample task | Scenario apply task |

---

## Task Templates

### Code Task (algorithmic / code concepts)

Structure:
1. State the problem in 2–3 sentences
2. Give 1–2 worked examples with input → output
3. State constraints (time/space complexity target if applicable)
4. Give the exact filename: `{concept_slug}_{lesson_n}.py` (e.g. `memoization_l1.py`)
5. State acceptance criteria (what correct output looks like)
6. Say: "Write your solution and say 'done' when ready."

Example (memoization, lesson 2):
> **Task:** Write a function `fib(n)` that returns the nth Fibonacci number using memoization.
> - `fib(5)` → `5`, `fib(10)` → `55`
> - Target: O(n) time, O(n) space
> - File: `memoization_l2.py`
> - Acceptance: Returns correct values for n=0 through n=20. Uses a cache (dict or `@lru_cache`) — not plain recursion.

### Pseudocode / Trace Task (protocol / systems concepts)

Structure:
1. State the scenario (e.g. "A client is connecting to a server")
2. Ask the user to write out the steps in order, in plain English or pseudocode
3. Give the exact filename if written: `{concept_slug}_l{n}_trace.txt` or `.md`
4. State acceptance criteria (which steps must appear, in what order)
5. Say: "Write your trace and say 'done' when ready."

Example (TCP handshake, lesson 2):
> **Task:** Write out the steps of a TCP three-way handshake. Include: who sends what, what information is in each message, and what state each side is in after each step.
> - File: `tcp_handshake_l2.md`
> - Acceptance: All three steps present (SYN, SYN-ACK, ACK), correct sender for each, connection state described at end.

### Write-in-Own-Words Task (non-technical concepts)

Structure:
1. Give a scenario or prompt: "Imagine you're explaining [concept] to a friend who has never heard of it."
2. Ask the user to write 3–5 sentences that capture the core idea
3. No filename needed — ask them to paste it directly
4. State acceptance criteria (what the explanation must include)

Example (opportunity cost, lesson 1):
> **Task:** In 3–5 sentences, explain opportunity cost to someone who has never studied economics. Use a real example from everyday life — not a textbook definition.
> - Acceptance: Explanation mentions what was given up (not just what was chosen), and the example makes clear that opportunity cost isn't the monetary price paid.

### Counterexample Task (edge cases / gotchas)

Structure:
1. Give a claim or common assumption about the concept
2. Ask the user to find or construct a case where it breaks
3. Can be code (write a test that exposes the failure) or text (describe the scenario)
4. State acceptance criteria (what the counterexample must show)

Example (memoization, lesson 3):
> **Task:** Here's a common assumption: "memoization always makes a function faster." Find a case where this is false or harmful.
> - You can write a Python example that demonstrates it, or describe the scenario in 2–3 sentences.
> - File (if code): `memoization_l3_edge.py`
> - Acceptance: Identifies a real case — e.g. functions with large argument spaces filling memory, or mutable arguments causing incorrect cache hits.

### Scenario Apply Task (tradeoffs / when to use)

Structure:
1. Present a realistic scenario with two or more options
2. Ask which option to pick and why
3. Paste/paste accepted — no file needed
4. Acceptance criteria: answer names the right choice and states the key tradeoff

Example (TCP vs UDP, lesson 5):
> **Task:** You're building a video game that sends player position updates 30 times per second. Should you use TCP or UDP? Explain your choice in 2–3 sentences.
> - Acceptance: Chooses UDP, explains that position updates are latency-sensitive and occasional loss is acceptable (a stale frame is less harmful than a delayed one).

---

## Acceptance Criteria Standards

Always state these explicitly before the user starts:

- **For code**: exact function name, required inputs/outputs, complexity target (if applicable), at least 1 edge case that must pass
- **For traces / write-ups**: what must be present, what order matters (if any), minimum length
- **For counterexamples**: what the example must demonstrate (not just "a case where it's slow" — be specific)

Don't make criteria vague. "Shows understanding" is not a criterion. "Returns correct output for n=0, n=1, and n=20" is.

---

## Review Standards

### For code (Read the file first — always)

1. Read the file using the Read tool. Never review blind.
2. Check:
   - Correctness: does it produce right outputs for the stated examples?
   - Edge cases: does it handle n=0, empty input, etc.?
   - Complexity: does it meet the stated target?
   - Approach: does it reflect understanding of the concept (not a workaround that bypasses it)?
3. Cite exact lines in feedback: "Line 7: this recursion without a cache is O(2^n), not O(n) — that's plain recursion, not memoization."
4. Positive + specific gap: "The base case is right. The issue is on line 12 — [specific problem]. Here's a hint: [targeted direction]."

### For text tasks (paste from user)

1. Read what they wrote carefully before responding.
2. Check against acceptance criteria — each criterion explicitly.
3. Identify the first gap (not all gaps at once — fix one thing per round).
4. Quote their words when correcting: "You said '[X]' — that's close, but it misses [Y]."

### Advance condition

Task passes acceptance criteria. Partial credit (most criteria met, minor gap) → point out the gap, ask for a small fix, then advance after. Don't require perfection; require demonstrated understanding.

---

## What Not to Do in Build Mode

- Don't review without reading — blind feedback is worse than no feedback
- Don't give the answer in the task description — the task must require them to work it out
- Don't set acceptance criteria so vague that any answer passes
- Don't require more than one task per lesson — one task, one concept
- Don't give multi-paragraph feedback — cite the specific line/sentence and the specific issue
