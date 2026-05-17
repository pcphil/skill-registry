# Skills

A **skill** is a markdown prompt loaded into a coding agent to give it specialised behaviour — a tutor, a code reviewer, a scaffolder, etc.

## Structure

```
skill-name/
├── SKILL.md          # Required. Frontmatter + instructions.
├── references/       # Heavy docs loaded on demand.
├── scripts/          # Deterministic helper scripts.
└── assets/           # Templates and boilerplate.
```

**SKILL.md** is the entry point. It uses YAML frontmatter for metadata and markdown for instructions:

```markdown
---
name: skill-name
description: One or two sentences — drives trigger matching and search.
---
# Instructions...
```

## Activation

Copy or symlink a skill directory into `~/.agents/skills/` (or `.claude/skills/` for project-scoped skills) and reload plugins. The `description` field controls when the agent auto-activates the skill.

## Best Practices

- **Keep SKILL.md short** — under 500 lines. Move heavy content to `references/` and load it on demand.
- **Write the description carefully** — it is used for semantic search and trigger matching; keyword-rich and specific beats vague.
- **One concept per skill** — a skill that does one thing well is easier to trigger correctly and easier to maintain.
- **Express intent, not mechanism** — write "search the codebase for X" not "use the Grep tool". This keeps skills portable across agents.
- **Define clear boundaries** — state explicitly when the skill should *not* activate to avoid wasting context on irrelevant tasks.
- **Prefer flat structure** — avoid deep nesting inside a skill directory; it adds complexity without benefit.
