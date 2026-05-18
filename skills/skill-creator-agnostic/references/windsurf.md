# Windsurf Rule Format

## File Location

**Global rules:** `.windsurfrules` in project root
**Workspace rules:** Configured via Windsurf settings UI

Windsurf loads `.windsurfrules` automatically for every session in the project.

## Format

Plain markdown. No frontmatter. No special context variables (unlike Cursor).

Windsurf's Cascade model reads rules as persistent system-level context. Write instructions in second person, present tense — "You are...", "Always...", "Never...".

## Cascade Context

Windsurf's Cascade applies rules hierarchically:
- Global user rules (settings) → applied first
- Project `.windsurfrules` → layered on top
- In-chat instructions → override for that session only

Write `.windsurfrules` assuming global user rules may already set baseline behavior. Don't repeat universal instructions (e.g., "write clean code") — focus on project-specific constraints.

## Recommended Structure

```markdown
# [Project Name] Rules

## Role & Objective
You are [persona]. Your primary goal is [objective].

## Stack
- Language: [e.g., TypeScript 5.x]
- Framework: [e.g., Next.js 15 App Router]
- Key dependencies: [list pinned versions]

## Workflow
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Always
- [Positive constraint 1]
- [Positive constraint 2]

## Never
- [Hard prohibition 1]
- [Hard prohibition 2]

## Out of Scope
[What this rule does NOT cover — prevents drift]
```

## Negative Triggers

No auto-attachment by file type (no globs). Windsurf applies `.windsurfrules` to all sessions. Use "Out of Scope" section to bound behavior:

```markdown
## Out of Scope
- Do not generate backend code — this project is frontend only.
- Do not modify files in `src/generated/` — auto-generated, do not edit.
```

## Size

Windsurf loads full file every session. Keep under 150 lines. Shorter = more reliable instruction-following.

## Template

See `assets/windsurf-template.md`
