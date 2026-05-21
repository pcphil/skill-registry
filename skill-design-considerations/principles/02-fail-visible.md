# Fail Visible

## What it is

When a skill can't proceed — because information is missing, input is ambiguous, a tool is unavailable, or a condition isn't met — it should surface the failure clearly and specifically, not guess, fill in silently, or produce output that looks correct but isn't. A visible failure gives the user something to act on. A silent or hidden failure gives them nothing.

This is the positive version of silent-failure (interaction/01): where that document explains what goes wrong, this principle explains the standard to design toward.

## Why it matters

Users can recover from visible failures. They cannot recover from hidden ones. A skill that says "I couldn't find the target platform in your message — which one are you targeting?" gives the user a specific, answerable question. A skill that silently assumes "Claude Code" and generates platform-specific output for the wrong platform wastes the user's time and produces output they'll have to redo.

Models are biased toward producing *something* rather than stopping. Fail visible is a deliberate counterweight to that tendency: it teaches the model that a well-articulated stop is better than a confident wrong answer.

## How to apply

**Define failure states as part of the workflow, not as an afterthought:**

For each step, ask: what can go wrong here? Define an explicit output for each failure case:

```markdown
## Workflow
1. Load skill file
   → Success: proceed to step 2
   → File not found: "No skill file at [path]. Please provide a valid path."
   → File empty: "The file at [path] is empty. Nothing to analyze."
```

**Name the failure before asking for resolution:**

State what failed, then ask. Don't just ask — that leaves the user guessing why:

```markdown
# Opaque (bad)
What platform is this for?

# Visible (good)
Target platform is missing — I need it to generate platform-specific output.
Which platform: Claude Code, Cursor, Windsurf, or other?
```

**Treat partial completion as a reportable state:**

If the skill completes some steps but is blocked on others, report both:

```markdown
Completed: requirements gathered, draft generated.
Blocked on: platform capability for [feature X] — needs verification before I can complete the constraints section.
To continue: [specific question or action needed].
```

**Surface uncertainty rather than resolve it silently:**

When the model is uncertain (ambiguous input, competing interpretations), say so — don't pick one silently:

```markdown
# Silent resolution (bad)
[Model interprets ambiguous input as X and proceeds]

# Visible uncertainty (good)
Your message could mean X or Y. I'll proceed as X — let me know if you meant Y.
```

**Make "no findings" explicit:**

A null result should be as visible as a finding. "No issues found" is a result. Silence is not:

```markdown
If analysis produces no findings, output:
"No issues detected in this skill."
Do not output nothing.
```

## Example

**Before — silent failure mode:**

```markdown
## Workflow
1. Read the user's request
2. Generate output based on what they described
3. Deliver the result
```

When the request is ambiguous, required information is missing, or the skill can't execute a step — nothing is said. The model generates something. It may not be what the user needed.

**After — visible failure standard:**

```markdown
## Workflow
1. Read the user's request
   → If required information is missing: list what's missing and ask — do not proceed
   → If request is ambiguous: state both interpretations and ask which to proceed with
2. Generate output
   → If generation is blocked by an unresolvable uncertainty: stop and name the blocker
3. Deliver result
   → If result is empty/null: output "No output generated — [reason]."

## Failure Standard
Every failure state has a user-facing message. Every message:
- Names what failed (not just asks a question)
- Explains why it matters
- States exactly what's needed to continue
```

Visible failures. Users always know what happened and what to do next.
