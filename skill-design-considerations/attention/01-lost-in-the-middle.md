# Lost in the Middle

## What it is

LLM attention is not uniform across a long context. Models pay the most attention to content at the **start** and **end** of their input. Content placed in the middle of a long prompt — even critical rules or constraints — receives significantly less attention and is more likely to be ignored or forgotten during generation.

This applies at multiple scales:
- Within a single SKILL.md file (rules buried on line 200 of 400)
- Within a list of instructions (item 6 of 10)
- Across the full context window (skill loaded in the middle of a long conversation)

## Why it happens

Transformer attention is theoretically global, but in practice trained models exhibit a U-shaped recall curve when tested on long inputs. The phenomenon was documented empirically in "Lost in the Middle: How Language Models Use Long Contexts" (Liu et al., 2023). The effect is stronger with longer inputs and intensifies as context window usage approaches its limit.

Likely causes:
- Training data rarely requires retrieving facts from the exact middle of long documents
- Positional encoding interacts with attention in ways that favor endpoints
- RLHF and instruction tuning reinforce following instructions in familiar positions (beginning of system prompt, beginning of user turn)

## Analogy

Think of a keynote speech. The audience remembers the speaker's opening joke and their closing call-to-action. The eight bullet points in the middle? Gone by the next morning. Your SKILL.md is that speech — the crowd (the model) was present for all of it, but only the edges survived. Write accordingly.

## Symptoms

- Model follows rules stated at the top of SKILL.md but ignores rules halfway down
- A constraint mentioned only once in the middle of a long skill body gets violated
- Skill works correctly on short conversations, breaks on long ones (middle content pushed further from edges as context grows)
- Model completes the wrong step in a multi-step workflow when the correct step was listed in the middle
- User corrects the model for ignoring something "clearly stated" — and it was in the middle of the file

## Fix

**Structural fixes:**
- Keep SKILL.md under 150 lines for the most critical path. Push detail to `references/`.
- State the single most important constraint in the first 5 lines of the skill body.
- Repeat critical constraints at the end of the file as a summary or checklist.
- Use progressive disclosure: load only what's needed for the current step.

**Ordering fixes:**
- Put the most important rule first in every list, not last.
- If you have 10 rules, cut to 5. The ones you cut were already lost in the middle.
- Never bury a negative trigger (when NOT to activate) in the middle — put it immediately after the description.

**Content fixes:**
- Use section headers to create visual anchors. Models attend to headers even in middle content.
- Bold critical constraints: `**Never generate output without user confirmation.**`
- For multi-step workflows, number steps and keep each step's instruction on one line.

## Example

**Bad — critical constraint buried mid-file:**

```markdown
## On Invoke
Check the user's goal.

## Workflow
1. Gather requirements
2. Detect platform
3. Generate skill body
4. Always define negative triggers before writing the description field — this is required.
5. Format output
6. Review

## Rules
...15 more rules...
```

Step 4's constraint is lost. It will be ignored.

**Good — critical constraint surfaced immediately:**

```markdown
**Required before generating:** negative triggers must be defined. Ask if missing.

## On Invoke
Check the user's goal. Confirm negative triggers exist before proceeding.

## Workflow
1. Gather requirements — confirm negative triggers defined
2. Detect platform
3. Generate skill body
4. Format output

## Rules
...5 rules max...

**Reminder:** do not generate without negative triggers confirmed.
```

Same constraint appears at top, embedded in the workflow step, and restated at the end.
