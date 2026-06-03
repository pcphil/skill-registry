# Reference Files — Pattern Guide

Reference files live in `references/` and are loaded on demand, not at skill startup.
Keep them out of SKILL.md when content exceeds ~50 lines or is only needed in specific situations.

## When to create a reference file

- Curriculum content (lesson objectives, examples, exercises, acceptance criteria)
- Platform-specific format guides (claude-code, cursor, aider, etc.)
- Large lookup tables or decision trees
- Anything the agent only needs once per session, not every turn

## How to wire it up in SKILL.md

Instruct the agent to load it at the right moment:

```markdown
## Core Workflow

1. Load the lesson content: read `references/curriculum.md` section for lesson [N].
2. Present the concept...
```

Or conditionally:

```markdown
If the user's platform is Cursor, read `references/cursor.md` before generating output.
```

## Naming conventions

| Content | Suggested name |
|---------|---------------|
| Single curriculum file | `curriculum.md` |
| Per-lesson granular files | `p1-l1-setup.md`, `p1-l2-variables.md` |
| Per-platform guides | `claude-code.md`, `cursor.md`, `aider.md` |
| Project specs | `projects.md` |
| API / external docs | `api-reference.md` |

## What NOT to put here

- Logic or decision trees that run every turn → keep in SKILL.md
- Files under ~20 lines → inline them in SKILL.md directly
- Generated output or user data → use memory, not reference files

---

Delete this file and replace with your actual reference content.
