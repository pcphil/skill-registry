# Negation Failure

## What it is

LLMs follow instructions phrased as prohibitions ("don't do X", "never do Y", "avoid Z") significantly less reliably than instructions phrased as positive actions ("do A instead", "always do B", "use C"). When a skill relies heavily on negative instructions to constrain behavior, the model tends to violate those constraints — especially under ambiguous conditions or when the instruction is far from the point of action.

## Why it happens

Language models are trained primarily on text that describes what things ARE and what actions TO take, not on text that describes what NOT to do. Negation requires holding a concept in mind and then suppressing a response to it — a more complex cognitive operation that training does not reinforce as strongly.

Additionally:
- Negative instructions require the model to first generate (or consider) the prohibited action before suppressing it. Under pressure to complete a task, the suppression step gets skipped.
- "Don't do X" leaves the correct action undefined. The model fills the gap with its default behavior, which may be exactly X.
- In long contexts, "don't do X" stated once early is forgotten by the time the model reaches the decision point. A positive instruction ("do Y") at the decision point is more effective.

## Analogy

Tell yourself "don't think about a pink elephant." You just thought about one. Now try "picture a blue square" — that works immediately. The brain latches onto the concrete concept in the instruction. Negative instructions hand the model a vivid image of the forbidden action right before asking it not to do it. Positive instructions hand it the action to take instead.

## Symptoms

- Skill includes "don't generate code without asking first" — model generates code without asking
- Skill says "never activate for conceptual questions" — model activates for conceptual questions
- "Don't blend platform formats" — model blends formats anyway when user's request is ambiguous
- Model follows positive rules in a skill reliably but violates the negative ones
- Adding "NEVER" or "ABSOLUTELY DO NOT" in caps temporarily fixes the issue but fails again as context grows

## Fix

**Reframe every negative as a positive:**

| Negative (unreliable) | Positive (reliable) |
|-----------------------|---------------------|
| Don't generate without confirmation | Ask for confirmation before generating |
| Never blend platform formats | Generate one file per platform, clearly labeled |
| Avoid activating for conceptual questions | Activate only when code modification is requested |
| Don't add rules the user didn't ask for | Add only rules explicitly requested by the user |
| Never skip negative triggers | Define negative triggers before writing the description |

**Structural fixes:**
- Audit every instruction in your skill for "don't", "never", "avoid", "no", "without". Rewrite each one as what to do instead.
- If you can't rewrite a negative as a positive, the constraint is probably unclear. Clarify what the desired behavior actually is.
- When a boundary truly must be stated negatively (out-of-scope declarations), keep it in a dedicated `## Boundaries` section and follow each negative with a redirect: "For X, say 'out of scope' and suggest Y instead."

**At decision points:**
- Place the positive instruction immediately before the action it governs, not only at the top of the file.
- Use conditional positive framing: "If the user asks about X, do Y" rather than "If the user asks about X, don't do Z."

## Example

**Bad — negation-heavy:**

```markdown
## Rules
- Don't generate without knowing the target platform
- Never use Claude Code tool names in a Cursor skill
- Don't activate if the user is just asking a question
- Never produce output longer than 500 lines
- Don't ask more than 2 clarifying questions
```

**Good — positive reframe:**

```markdown
## Rules
- Confirm target platform before generating any output
- Use intent-based language ("search the codebase") — never platform tool names
- Activate only when the user is requesting skill creation or modification
- Keep output under 500 lines; move excess to references/
- Ask at most 2 clarifying questions, then generate with stated assumptions
```

Same constraints. The positive version gives the model a clear action to take at each decision point.
