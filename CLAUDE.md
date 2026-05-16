# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a skill registry — a collection of reusable agent skills designed primarily for Claude Code, with portability to other coding agents (Cursor, Windsurf, Copilot) as a design goal.

## Skill Structure

Each skill lives in its own top-level directory following this layout:

```
skill-name/
├── SKILL.md          # Required. Frontmatter (name, description) + markdown instructions.
├── references/       # On-demand detailed docs, loaded by Claude when needed.
├── scripts/          # Deterministic executables (Python/Bash).
└── assets/           # Templates, boilerplate — not loaded into context.
```

### Key constraints
- SKILL.md should stay under 500 lines — move heavy content to references/
- The `description` field in frontmatter drives trigger matching; write it carefully
- Keep directory structure flat (no deep nesting)

## Installing Skills

Symlink a skill directory into `~/.agents/skills/` to make it available in Claude Code:

```bash
ln -s "$(pwd)/skill-name" ~/.agents/skills/skill-name
```

## Design Principles

- **Portability first**: Express intent over mechanism. Say "search the codebase for X" not "use the Grep tool."
- **Progressive disclosure**: Metadata always loaded → SKILL.md on trigger → references on demand.
- **Universal core / platform wrapper**: Write the logic once, wrap per platform.
- Learning state and progress tracking use Claude Code memory (not committed to repo).
