---
name: skill-name
description: >
  One or two sentences rich in trigger keywords. Include the slash command if one exists (e.g., "invokes /skill-name").
---

[One sentence persona. E.g., "You are an expert in X."]

## On Invoke

1. Check memory for existing progress.
   - If progress exists: summarize, ask resume or restart.
   - If no progress: run [Assessment/Init flow].

## [Core Workflow]

[Step-by-step behavior. One concept/action per step.]

1. **[Step name]** — [what to do]
2. **[Step name]** — [what to do]
3. **[Step name]** — [what to do]

## Rules

- [Positive constraint — "Always do X" not "Never forget X"]
- [Positive constraint]
- [Positive constraint]

## Boundaries

- [What this skill does NOT handle] — say "[redirect message]" instead.
- "/skill-name stop" or "[end phrase]": save progress to memory, summarize coverage.
