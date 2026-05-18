# Cursor Skill Format

## File Location

**New format (MDC):** `.cursor/rules/skill-name.mdc`
**Legacy:** `.cursorrules` (root, plain markdown, no frontmatter)

Prefer MDC — it supports per-file scoping via `globs`.

## Frontmatter (MDC only)

```yaml
---
description: One sentence. Used by Cursor's agent mode to select rules.
globs: ["src/**/*.ts", "tests/**/*"]   # Files that auto-attach this rule
alwaysApply: false                      # true = always in context, false = on-demand
---
```

**`globs`** — Cursor auto-attaches rules matching open files. Omit if skill should only activate manually.
**`alwaysApply: true`** — loads into every chat. Use sparingly — burns context on every request.

## Context Variables

Available in rule body — Cursor resolves these at runtime:

| Variable | Value |
|----------|-------|
| `{{REPO_ROOT}}` | Absolute path to project root |
| `{{CURRENT_FILE}}` | Path of the currently active file |
| `{{SELECTION}}` | Currently selected text in editor |

## Body Format

Structured sections work well in Cursor — it renders markdown in the rule panel.
Emoji headers are optional but common in the Cursor ecosystem.

Recommended structure:

```markdown
## Activation Boundaries
**Active when:**
- User asks to [action]
- Editing files matching `[pattern]`

**Do NOT activate when:**
- User asks a theoretical/conceptual question
- Task targets a different stack (e.g., backend logic in a frontend rule)

## Context & Objective
[Persona + high-level goal. E.g., "You are an expert in Next.js 15 App Router..."]

## Workflow
1. **Validate** — check before writing code
2. **Execute** — concrete steps and preferred commands
3. **Verify** — how to test the output

## Constraints
- [Hard rule 1]
- [Hard rule 2]

## Reference Examples
[Minimal idiomatic code snippet to anchor correct output]
```

## Negative Triggers

Always include a "Do NOT activate when" section. This is the primary token-saving mechanism in Cursor — rules that fire when they shouldn't bloat every prompt.

## Template

See `assets/cursor-template.mdc`
