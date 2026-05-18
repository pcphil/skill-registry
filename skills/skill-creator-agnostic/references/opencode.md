# OpenCode Skill Format

## File Location

Same structure as Claude Code:

```
skill-name/
├── SKILL.md          # Required. Entry point.
├── references/       # On-demand detail
├── scripts/          # Deterministic executables
└── assets/           # Templates/boilerplate — not loaded into context
```

See OpenCode docs: https://opencode.ai/docs/skills/

## Frontmatter

```yaml
---
name: kebab-case-name
description: >
  One or two sentences rich in trigger keywords.
---
```

Same frontmatter fields as Claude Code. `name` and `description` only.

## Key Differences from Claude Code

- **Tool names differ** — OpenCode has its own tool set. Do not reference Claude Code-specific tool names (`Read`, `Grep`, `Glob`, `Edit`, `Write`, `AskUserQuestion`). Use intent-based language instead: "read the file", "search the codebase", "ask the user".
- **Memory system** — verify whether OpenCode supports persistent memory across sessions before relying on it. If unsupported, use stateless instructions only.
- **No emojis, no globs, no `{{vars}}`** — same constraints as Claude Code.

## Body Format

Plain prose markdown. Same structure as Claude Code:

1. **On Invoke** — what to do first
2. **Core workflow** — step-by-step behavior
3. **Rules** — positive constraints
4. **Boundaries** — explicit out-of-scope statements

## Portability Note

A well-written OpenCode skill and a well-written Claude Code skill should look nearly identical. If they don't, the skill is probably too platform-specific. Aim for intent-based language ("search the codebase for X") over tool-specific calls ("use the Grep tool").

## Template

See `assets/opencode-template.md`
