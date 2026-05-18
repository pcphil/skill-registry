---
name: skill-name
description: >
  One or two sentences rich in trigger keywords. Include the slash command if one exists.
---

[One sentence persona. E.g., "You are an expert in X."]

## On Invoke

1. Check for existing progress if stateful.
   - If progress exists: summarize, ask resume or restart.
   - If no progress: begin [init flow].

## [Core Workflow]

1. **[Step name]** — [what to do]
2. **[Step name]** — [what to do]
3. **[Step name]** — [what to do]

## Rules

- [Positive constraint — "Always do X" not "Never forget X"]
- [Positive constraint]
- [Positive constraint]

## Boundaries

- [What this skill does NOT handle] — say "[redirect message]" instead.
- "/skill-name stop" or "[end phrase]": summarize what was covered.
