# Claude Code Skill Format

## File Location
```
skill-name/
├── SKILL.md          # Required. Entry point.
├── references/       # On-demand detail — load when needed
├── scripts/          # Deterministic executables
└── assets/           # Templates/boilerplate — not loaded into context
```

Install: symlink `skill-name/` into `~/.agents/skills/skill-name`

## Frontmatter

```yaml
---
name: kebab-case-name
description: >
  One or two sentences. Dense with trigger keywords — this drives skill matching.
  Include the slash command if one exists (e.g., "invokes /skill-name").
---
```

**Only `name` and `description` are standard fields.** Do not add `globs`, `tags`, or platform-specific fields.

## Body Format

Plain prose markdown. No emojis. No emoji section headers.

Structure:
1. **On Invoke** — what to do first (check memory, detect state, ask questions)
2. **Core workflow** — step-by-step behavior
3. **Rules** — constraints, written as positive instructions where possible
4. **Boundaries** — explicit out-of-scope statements

## Tool References

Name tools explicitly — Claude Code executes these directly:

- `Read` — read a file
- `Grep` — search codebase
- `Glob` — find files by pattern
- `Edit` / `Write` — modify/create files
- `Bash` / `PowerShell` — run commands
- `AskUserQuestion` — ask user structured questions with options
- Memory system — persist state across sessions

## Negative Triggers

Claude Code doesn't have a dedicated negative trigger field. Embed in description or body:

```markdown
## Boundaries
- Only activate for X. For Y: say "out of scope, focus on X."
- Skip if user is asking a conceptual question without code modification.
```

## State & Memory

Track progress across sessions using Claude Code memory (type: `project`):

```markdown
Save to memory: current step, what's been built, user background.
On resume: read memory → summarize where they left off → ask continue or restart.
```

## Size Constraint

Keep SKILL.md under 500 lines. Move heavy content to `references/`. Reference it explicitly:

```markdown
Full spec: `references/detail.md`
```

## Template

See `assets/claude-code-template.md`
