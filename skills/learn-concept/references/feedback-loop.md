# Feedback Loop Reference

Reference for SKILL.md. Load this when adapting a lesson to the learner profile, or when running the post-lesson update.

---

## Learner Profile Schema

Stored in memory alongside progress (type: project, key: `learn-concept`):

```
learner_profile:
  pacing: fast | medium | slow
  analogy_styles_effective: []     # analogy category names from curriculum-guide.md
  recurring_gaps: []               # gap types seen 2+ times
  depth_preference: examples | theory | unknown
  lesson_history: []               # list of {lesson_n, attempt_count, gap_type, analogy_landed}
```

**Initial state** (set on first save, before lesson 1):
```
pacing: medium
analogy_styles_effective: []
recurring_gaps: []
depth_preference: unknown
lesson_history: []
```

---

## Signal Collection (after each lesson completes)

Collect these four signals silently — no user-facing prompt:

### 1. attempt_count
Count how many distinct attempts the user made before the lesson passed.
- 1 attempt = answered correctly or nearly correctly on first try
- 2 attempts = one re-explain or retry cycle
- 3+ attempts = struggled; multiple re-explains or retries

### 2. re_explain_needed
`true` if the user said "I don't get it", "can you explain again", "I'm confused", or required a full re-explanation of the concept (not just a follow-up hint).

### 3. analogy_landed
`true` if the user's response references or echoes the analogy (e.g. "oh so it's like the vending machine..."), or if they use the analogy's framing to explain back the concept. `false` if their answer is purely definitional with no trace of the analogy.

### 4. gap_type
The category of the first significant mistake made, if any:
- `recall` — couldn't remember what the concept is or what it's called
- `mechanics` — knew what it was but couldn't trace how it works step-by-step
- `edge_case` — missed a boundary condition, failure mode, or gotcha
- `application` — understood theory but struggled to apply to a task or new scenario
- `none` — no significant mistake; passed on first try

---

## Post-Lesson Update Protocol

Run this after a lesson is marked complete (regardless of how many attempts):

1. Record lesson result:
   ```
   lesson_history.append({
     lesson_n: <current lesson index>,
     attempt_count: <count>,
     gap_type: <type or none>,
     analogy_landed: <bool>
   })
   ```

2. Update `pacing` (rolling average):
   ```
   n = len(lesson_history)
   avg = sum(h.attempt_count for h in lesson_history) / n
   pacing = "fast" if avg < 1.5 else "slow" if avg >= 2.5 else "medium"
   ```

3. Update `recurring_gaps`:
   - Tally gap_type counts across lesson_history (excluding `none`)
   - Any gap_type with count >= 2: add to `recurring_gaps` if not already present

4. Update `analogy_styles_effective`:
   - If `analogy_landed = true` for this lesson: note the analogy category used (from curriculum-guide.md taxonomy) and add to `analogy_styles_effective` if not present

5. Update `depth_preference`:
   - If first-try pass (attempt_count = 1) happened after a definition-led explanation: lean `theory`
   - If first-try pass happened after an example-led explanation: lean `examples`
   - If mixed or unclear: leave as `unknown`
   - Rule: only update after 3+ lessons — not enough signal before that

6. Save updated profile to memory.

---

## Pre-Lesson Adaptation Rules

Read the learner profile at the start of each lesson. Apply these rules to adjust delivery:

### Pacing Adjustments

**pacing = slow**
- Analogy: 2–3 sentences (not one-liner). Use the most concrete, everyday example in the category.
- Explanation: add one extra worked example after the formal definition before asking questions or giving a task.
- Quiz mode: start with a simpler recall question before moving to trace/predict.
- Build mode: narrow the task scope (smaller input range, fewer edge cases to handle).

**pacing = fast**
- Analogy: one sentence is fine.
- Explanation: keep tight; skip restating things the user already showed they know.
- Quiz mode: skip trivial recall questions; open with trace or predict.
- Build mode: extend acceptance criteria to include one edge case they must handle.

**pacing = medium**
- Default delivery — no adjustment needed.

### Gap Adjustments

**recurring_gap = mechanics**
- Add one extra trace/walk-through step to the explanation ("let me walk through this step-by-step before you try").
- Quiz mode: ask a mechanics question even if the lesson is lesson 1 or 5 (not just lesson 2).

**recurring_gap = edge_case**
- Add an edge-case probe even outside lesson 3 ("before we move on — what would break this?").
- Build mode: acceptance criteria must include at least one edge case.

**recurring_gap = recall**
- Open each lesson with a one-line recap of the prior lesson's core idea ("Last time: [X]. Today builds on that.").
- This is a bridge, not a re-teach — one sentence only.

**recurring_gap = application**
- After explanation, add one "mini-apply" example before the actual task or quiz questions ("here's how this shows up in practice: [brief real scenario]").

### Analogy Style Adjustments

If `analogy_styles_effective` is non-empty:
- When picking an analogy for a new lesson, prefer categories listed in `analogy_styles_effective`.
- If the concept doesn't map well to an effective category, note this and use the closest fit.

If `analogy_styles_effective` is empty (early sessions):
- Default to the most concrete physical/everyday analogy for the concept type (see curriculum-guide.md patterns).

### Depth Preference Adjustments

**depth_preference = examples**
- Reorder the explanation: example first → then formal definition → then why it matters.
- In Build mode: show a small worked example inline before giving the task.

**depth_preference = theory**
- Standard order: formal definition → why it matters → example to confirm.
- In Quiz mode: ask the definition/recall question first.

**depth_preference = unknown**
- Use standard order. Observe this lesson's result to infer preference.

---

## Profile Summary for `/learn-concept status`

When the user runs `/learn-concept status`, include a one-line learner profile summary:

```
Learner profile: pacing=<value>, depth=<value>, recurring gaps=[<list or none>]
Analogies that landed: [<list or "still collecting">]
```

Keep it to two lines. Don't expose raw lesson_history — that's internal.
