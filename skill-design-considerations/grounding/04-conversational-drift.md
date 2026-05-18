# Conversational Drift

## What it is

Conversational drift occurs when the model's behavior gradually shifts away from a skill's defined workflow due to the accumulating influence of recent conversation. The skill was loaded correctly, its instructions are in context, but as the conversation grows — user messages, model responses, casual phrasing, topic pivots — the recent turns carry more weight than the original skill instructions. The model starts optimizing for what the conversation has been recently, not what the skill says to do.

Drift is different from instruction conflict (a specific clash between two instructions) — it's a slow, directional slide caused by the cumulative weight of conversational context overwhelming static skill instructions.

## Why it happens

Recency bias means the most recent tokens in context have disproportionate influence on generation (see `07-primacy-recency-bias.md`). In a long conversation:

- The skill's instructions were loaded at turn 1 and are now far from the generation point
- The last 5 user messages shape the immediate context far more strongly than a skill loaded 20 turns ago
- User phrasing gradually calibrates the model's register ("just be quick", "keep it casual", "don't worry about that")
- Each model response is trained to be coherent with the immediately preceding turn — which may have already drifted

The drift compounds: each slightly-drifted response becomes the "recent context" that the next response optimizes for. Drift accelerates as conversations grow.

## Analogy

Directions given at the start of a road trip: "Take the highway, stay in the right lane, exit at junction 14." Two hours in, your passenger has been casually suggesting shortcuts, commenting on traffic, saying "this lane looks faster." You've drifted two lanes left and missed the exit — not because you decided to ignore the original directions, but because the accumulated weight of small in-the-moment suggestions nudged you there incrementally. No single comment was the cause. The drift was systemic.

## Symptoms

- Skill workflow is followed at the start of a conversation but degrades over 10+ turns
- Model stops asking required confirmation questions after the user says "just go ahead" once
- Skill's structured output format gives way to casual prose as conversation tone shifts
- Model starts abbreviating or skipping workflow steps in longer conversations
- User's casual phrasing ("whatever works", "just pick one") permanently changes model behavior for the rest of the session
- Skill works correctly when tested in a fresh conversation, fails in long working sessions
- Re-reading the skill instructions mid-conversation temporarily fixes behavior — confirming drift, not a skill bug

## Fix

**Reinforce critical constraints at decision points, not just at load time:**

The further a constraint is from the decision point (in token distance), the weaker its influence. Move the constraint closer:

```markdown
## Step 3: Generate Output
Before generating, confirm: platform selected, negative triggers defined, requirements clear.
If any are missing, ask before proceeding — do not generate with assumptions at this step.
```

The constraint is restated immediately before the action it governs, not just at the top of the file.

**Use explicit re-anchoring phrases:**

Build re-anchoring into the workflow itself. At key transitions, the skill instructs the model to restate its current operating mode:

```markdown
## On Each Major Step
Before starting each step, briefly state which step you're on and what you're about to do.
This keeps the workflow explicit in the conversation and resists drift.
```

**Make the workflow visible in responses:**

Drift is harder when the structured workflow is visible. Skills that produce structured output ("Step 2 of 4: Platform Detection") maintain coherence longer than skills whose workflow is entirely internal:

```markdown
## Output Format
Begin each response with the current step: "**Step [N]: [Step Name]**"
This makes the workflow position explicit and makes drift immediately visible.
```

**Define a recovery path for detected drift:**

If the model detects it has drifted (user asks why it stopped following the workflow), give it a defined recovery action:

```markdown
## On Detected Drift
If the workflow has been interrupted or bypassed, offer to restart from the last confirmed step:
"We've moved away from the skill-creation workflow. Want to pick up from [last step] or start fresh?"
```

**Keep conversations focused:**

Drift is amplified by long, wide-ranging conversations. Skills designed for multi-step workflows benefit from short, focused sessions. State this in the skill:

```markdown
## Session Guidance
For best results, use this skill in a focused session. If the conversation has covered many other topics,
consider starting a fresh conversation to reduce conversational drift.
```

## Example

**Bad — constraint stated once at load time, drifts by turn 10:**

```markdown
## Rules
- Always confirm platform before generating
- Always include negative triggers
- Always confirm output with user before finalizing
```

By turn 15, the user has said "just generate it" twice, switched topics once, and come back. The model has stopped confirming and started generating directly — not because it decided to ignore the rules, but because the conversation's recent weight pushed it there.

**Good — constraints reinforced at decision points:**

```markdown
## Rules
- Confirm platform before generating (checked in Step 2)
- Include negative triggers in all output (verified in Step 3 checklist)
- Confirm output before finalizing (Step 5 is always a confirmation step — do not skip)

## Step 2: Platform
Confirm platform. Do not proceed to Step 3 until platform is confirmed, even if user says "just pick one."
If user insists: pick Claude Code, state the assumption, and note they can request a different format.

## Step 5: Confirm
This step is not optional. Present output and ask: "Does this look right, or do you want changes?"
Even in fast-mode sessions, confirmation is required before marking the task complete.
```

The same constraints appear at the load point AND embedded in the workflow steps where they're actually enforced. Drift has to fight both.
