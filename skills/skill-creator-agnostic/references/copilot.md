# GitHub Copilot Instructions Format

## File Location

**Workspace instructions:** `.github/copilot-instructions.md`

Copilot loads this file automatically for all chat interactions in the workspace. No activation config needed — it always applies.

## Format

Plain markdown. No frontmatter. No special variables. No globs.

Copilot treats this file as persistent workspace context. Write in direct, imperative prose — Copilot follows instruction-style text more reliably than descriptive prose.

## What Copilot Instructions CAN Do

- Set coding style and conventions
- Specify preferred libraries, patterns, idioms
- Define naming conventions and file structure
- Set language/framework version constraints
- Define what to avoid (anti-patterns, deprecated APIs)

## What They CANNOT Do

- Control when Copilot activates (it's always on)
- Reference files dynamically (no `{{vars}}`)
- Define multi-step workflows (Copilot is suggestion-based, not agentic)
- Persist state across sessions (no memory system)

## Recommended Structure

```markdown
# Copilot Instructions

## Stack
- Language: [TypeScript 5.x / Python 3.12 / etc.]
- Framework: [Next.js 15 / FastAPI / etc.]
- Test framework: [Vitest / pytest / etc.]

## Code Style
- [Naming convention — e.g., "Use camelCase for variables, PascalCase for components"]
- [Import style — e.g., "Named imports only, no default imports from libraries"]
- [Comment style — e.g., "No inline comments unless behavior is non-obvious"]

## Preferred Patterns
- [Pattern 1 — e.g., "Use `zod` for all runtime validation"]
- [Pattern 2 — e.g., "Prefer `const` arrow functions over `function` declarations"]

## Patterns to Avoid
- [Anti-pattern 1]
- [Anti-pattern 2]

## Testing
- [Test location, naming, coverage expectations]
```

## Negative Triggers

Copilot has no activation boundary system — instructions always apply. Use "Patterns to Avoid" and scope-limiting language:

```markdown
## Scope
These instructions apply to the `src/` directory only. Do not apply them to files in `scripts/` or `infra/`.
```

## Size

GitHub recommends keeping this file concise. Under 100 lines is ideal — Copilot's context window competes with open files and chat history. Prioritize the highest-impact conventions at the top.

## Template

See `assets/copilot-template.md`
