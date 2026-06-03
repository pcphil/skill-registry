# Scope Creep

## What it is

Scope creep occurs when a skill gradually accumulates responsibilities beyond its original purpose. It starts narrow ("generate SKILL.md files") and grows over time as the author adds handling for edge cases, related tasks, and user requests that are adjacent but not core. After enough additions, the skill does too many things: its `description` no longer matches its actual behavior, its trigger fires for the wrong requests, and its internal workflow is too long to follow reliably.

Scope creep is different from over-specification (too many rules for one task) — it's about too many tasks in one skill. The skill isn't just over-constrained; it's over-scoped. It has become a general-purpose assistant wrapped in a skill shell.

## Why it happens

Skills grow because adding is easier than splitting. When a user asks the skill to do something adjacent ("can you also validate the skill I just made?"), the author patches the skill body instead of creating a new skill. The patch works, gets committed, and sets a precedent. The next adjacent request gets patched in too.

There's also sunk-cost psychology: the skill has history, users, and known behavior. Creating a new skill feels like overhead. Patching feels like progress. Over time the patches accumulate and the skill's identity becomes blurry.

Additionally, skills are often not reviewed holistically after the initial authoring. The author sees each addition as small; they don't see the aggregate.

## Analogy

A Swiss Army knife is useful for casual outdoor tasks. A surgeon doesn't use one. The more functions you add to a single tool, the more it becomes adequate at everything and excellent at nothing. A skill that started as a scalpel and grew into a Swiss Army knife is doing the user a disservice — and the tools in the middle never get used correctly because nobody can find them.

## Symptoms

- SKILL.md is over 300 lines
- The `description` field says "creates skills" but the body also handles validation, conversion, installation, and user onboarding
- Skill triggers for requests it handles poorly because the description still matches the original narrow scope
- Author can't summarize what the skill does in one sentence without using "and"
- Internal workflow has 10+ steps covering multiple distinct use cases
- Users use the skill for tasks it was never designed for — and it half-works, creating support burden
- Adding a new edge case requires updating 4+ sections of the skill body

## Fix

**One skill, one responsibility:**

A skill should do one thing well. If you can't state the skill's purpose in a single sentence without "and", it has grown too broad. Split at the "and."

```
Before: "Creates SKILL.md files and validates existing skills and converts between platform formats"
After:
  - skill-creator: Creates SKILL.md files
  - skill-validator: Validates existing skills against best practices
  - skill-converter: Converts skills between platform formats
```

**Set a growth budget:**

Decide upfront how large the skill is allowed to get. A reasonable budget:
- SKILL.md: 150 lines max (the attention-quality target; Anthropic's platform hard limit is 500, but staying near 150 keeps the whole file in high-recall range)
- References: add one file per major sub-topic
- When the budget is hit: evaluate whether the new content belongs here or in a new skill

**Audit periodically:**

Every 3–6 months, re-read the skill's `description` and compare it to the actual body. If they've diverged, either update the description to reflect reality (and accept the trigger change) or refactor the body back to match the description.

**Create companion skills instead of patches:**

When an adjacent task comes in, resist the patch. Instead:
1. Determine if the task is genuinely part of this skill's core responsibility
2. If yes: add it properly (update description, integrate cleanly into workflow)
3. If no: create a new skill with a narrow scope

Companion skills can reference each other: "For validation, see `skill-validator`."

**Watch for these creep signals:**
- "While I'm in here, I'll also add..."
- "The user will probably also want..."
- "It's almost the same as what we already do..."

Each is a scope creep entry point.

## Example

**Bad — scope-crept skill:**

```markdown
---
name: skill-creator
description: Creates and manages agent skills for coding platforms.
---

## Workflow
1. Create new skills from user descriptions
2. Validate existing SKILL.md files against best practices
3. Convert Claude Code skills to Cursor format
4. Install skills by creating symlinks
5. List all installed skills
6. Update existing skills when requirements change
7. Archive deprecated skills
```

This is 7 distinct tools masquerading as one skill. The trigger fires for all 7, but the description only honestly covers #1. Steps 2–7 are scope creep.

**Good — narrow, focused, with companions:**

```markdown
---
name: skill-creator
description: >
  Generates new SKILL.md files and platform-specific rule files. Triggers when
  user requests a new skill or rule file. For validation, see skill-validator.
  For format conversion, see skill-converter.
---

## Workflow
1. Extract requirements from user description
2. Detect or ask for target platform
3. Generate skill file in correct platform format
4. Confirm output with user

## Boundaries
This skill handles creation only. For modifying existing skills, updating installed
skills, or validating skill quality: those are separate responsibilities handled
by companion skills.
```

Focused. Clear. Companion skills handle the rest.
