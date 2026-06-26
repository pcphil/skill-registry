# Quiz Mode Reference

Reference for SKILL.md. Load this when running a lesson in Quiz mode.

---

## Question Types

Use a mix of question types per lesson. Don't ask all the same type — variety prevents pattern-matching answers.

### Type 1: Recall
Test whether the user retained the core mental model.
- "In your own words, what is [concept]?"
- "What problem does [concept] solve?"
- "What does [analogy element] correspond to in [concept]?"

Use for Lesson 1 (What it is). Expect: 1–3 sentence answer that captures the essence without quoting the explanation verbatim.

### Type 2: Trace / Walk-through
Test whether the user understands the mechanics.
- "Walk me through what happens when [scenario] occurs."
- "What are the steps in [process], in order?"
- "If [input], what does [concept] produce?"

Use for Lesson 2 (How it works). Expect: numbered steps or a clear sequential description.

### Type 3: Predict / Reason
Test whether the user can apply the concept to a novel scenario.
- "What would happen if [constraint was violated]?"
- "If [edge condition], does [concept] still work? Why or why not?"
- "Between [option A] and [option B], which would you use here, and why?"

Use for Lesson 3 (Edge cases / gotchas). Expect: a reasoned answer that shows the user is thinking through consequences, not just recalling facts.

### Type 4: Contrast
Test whether the user can distinguish the concept from related ideas.
- "How is [concept] different from [similar concept]?"
- "When would you choose [concept] over [alternative]?"
- "What does [concept] guarantee that [alternative] doesn't?"

Use for Lesson 4 (Variants / relatives). Expect: a comparison that highlights the key differentiating property.

### Type 5: Synthesis
Test whether the user can situate the concept in a real-world decision.
- "Name a situation where [concept] would be the wrong choice."
- "What's the tradeoff you accept when using [concept]?"
- "How would you explain [concept] to someone with no technical background?"

Use for Lesson 5 (When to use it / tradeoffs). Expect: a practical, grounded answer — not just a definition.

---

## Per-Lesson Question Count

- Lesson 1: 2 questions (recall + one predict)
- Lesson 2: 2–3 questions (trace/walk-through dominant)
- Lesson 3: 2 questions (predict/reason, edge-case focused)
- Lesson 4: 2 questions (contrast focused)
- Lesson 5: 2 questions (synthesis focused)

Don't exceed 3 questions per lesson. Depth over breadth.

---

## Evaluation Rubric

### Correct
User answer captures the essential idea, even if phrased differently. Minor imprecision (wrong word, slightly off example) is fine as long as the core understanding is there.

Action: Brief affirmation ("Exactly." / "Right." / "Yes —") then move to next question or advance lesson.

### Partial
User has part of the answer but is missing a key piece (a step, a constraint, a counterexample).

Action:
1. Acknowledge what they got right: "You've got the [X] part right."
2. Name the gap precisely: "What you're missing is [Y]."
3. Ask a targeted follow-up: "Can you add that to your answer?"

Do NOT re-deliver the full explanation. One targeted sentence pointing at the gap.

### Wrong
User answer reflects a misconception or misses the point entirely.

Action:
1. Don't say "wrong" — say "Let me reframe this."
2. Re-explain the specific sub-point with a different angle or a new analogy element.
3. Ask the same question again (not a new question).
4. If wrong a second time: give a direct, scaffolded hint ("Think about it this way: [near-answer]"), then ask once more.

### Lesson Advance Condition
All questions answered correctly or partially-correctly with the gap closed. A user who gets partial → corrects → moves on has demonstrated understanding.

---

## Follow-up Question Templates

When an answer is close but needs precision, use these follow-up patterns:

- "You said [X] — what makes that true in this case?"
- "That's the right direction. What specifically causes [effect]?"
- "Good. Now what happens if [constraint is removed or reversed]?"
- "Correct. Can you connect that back to the analogy I gave earlier?"

Avoid open-ended "can you say more?" — be specific about what's missing.

---

## What Not to Do in Quiz Mode

- Don't ask leading questions that give away the answer ("Isn't it true that...?")
- Don't accept vague answers ("kind of" or "it's like a thing that does stuff") — probe until precise
- Don't ask more than 3 questions per lesson — it becomes an interrogation, not a check
- Don't skip to the next lesson after one correct answer — make sure the concept sticks with at least 2 questions
