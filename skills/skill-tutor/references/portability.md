# Module 1: Portability Patterns

## Lesson 1.1 — What "Portable" Means

### Concept

A portable skill is one whose core logic and intent can be expressed on any coding agent platform with minimal rewriting. Portability doesn't mean "write once, run everywhere" — it means **designing so the expensive part (the thinking) is reusable**, even when the packaging changes.

Every coding agent, regardless of platform, does three things:
1. Reads instructions (system prompt, rules file, skill body)
2. Has access to tools (file read/write, search, execute, web)
3. Operates within a context window (limited attention)

These three universals are your portability surface. A skill that's built around *what to think about* rather than *how to invoke a specific tool* will translate across platforms.

**Why this matters even if you only use Claude Code today:**
- You might switch tools. Your skill investment shouldn't be lost.
- Skills designed for portability tend to be cleaner — they force you to separate intent from mechanism.
- The agent landscape is moving fast. Today's platform may merge features from others.

### Example

**Non-portable instruction:**
```
When the user invokes /review, use the Grep tool to find all TODO comments,
then use the Read tool to load each file, and output findings using markdown.
```

**Portable instruction:**
```
When reviewing code, find all TODO comments across the project, read the
surrounding context for each, and present a summary grouped by priority.
```

The second version expresses *intent*. Any agent can figure out how to search and read files. The first version is Claude Code-specific (tool names, invocation pattern).

### Exercise

Look at this instruction and rewrite it to be portable:
> "Use the Bash tool to run `npm test`, capture the output, then use Edit to fix any failing assertions."

What's the intent? What's platform-specific?

---

## Lesson 1.2 — The Agent Interface Landscape

### Concept

Understanding what each platform offers helps you identify the universal core.

| Platform | Instruction Format | Trigger Mechanism | Tool Access | Context Model |
|----------|-------------------|-------------------|-------------|---------------|
| Claude Code | SKILL.md (markdown + frontmatter) | Description matching + slash commands | Named tools (Read, Edit, Bash, etc.) | Progressive disclosure (3 levels) |
| Cursor | .cursorrules (markdown) | Always loaded or @-referenced | Built-in (file ops, terminal) | Single file, always in context |
| Windsurf | .windsurfrules (markdown) | Always loaded | Built-in (Cascade tools) | Single file, always in context |
| Copilot | .github/copilot-instructions.md | Always loaded + custom agents | Limited (code generation focus) | Varies by mode |
| Custom SDK | System prompt (string) | Programmatic | Developer-defined | Developer-controlled |

**Key differences:**
- **Trigger**: Claude Code has sophisticated trigger matching; others are mostly "always on"
- **Progressive disclosure**: Only Claude Code has the 3-level loading system
- **Tool naming**: Every platform names its tools differently
- **Scope**: Cursor/Windsurf rules are project-wide; Claude Code skills can be cross-project

**Key similarities:**
- All read markdown instructions
- All can search, read, and modify files
- All operate on a single project at a time
- All benefit from clear, concise instructions with examples

### Exercise

Pick two platforms from the table. List three things they share and three things that would need adaptation when porting a skill between them.

---

## Lesson 1.3 — Universal Core, Platform Wrapper

### Concept

The pattern: **Write the brain once, wrap it per platform.**

Your skill has two layers:

```
┌─────────────────────────────┐
│     Platform Wrapper         │  ← Trigger syntax, tool names, file structure
├─────────────────────────────┤
│     Universal Core           │  ← Intent, logic, examples, quality criteria
└─────────────────────────────┘
```

**Universal core contains:**
- What the skill does (role, purpose)
- When it should activate (situations, not syntax)
- How to think about the problem (criteria, principles)
- What good output looks like (examples)
- Quality checks and edge cases

**Platform wrapper contains:**
- File format and frontmatter
- Trigger/matching configuration
- Tool-specific instructions (if needed for reliability)
- File path conventions
- Platform-specific features (progressive disclosure, hooks)

### Example: Code Review Skill

**Universal core** (works anywhere):
```markdown
# Code Review

## Role
You are a code reviewer focused on correctness, security, and maintainability.

## When to Activate
When the user asks for a review, submits a PR, or requests feedback on code changes.

## Review Criteria
1. Correctness: Does it do what it claims?
2. Security: OWASP top 10, input validation, auth checks
3. Maintainability: Clear names, reasonable complexity, tests exist
4. Performance: No obvious N+1, unnecessary allocations, or blocking calls

## Output Format
- Summary (1-2 sentences)
- Issues (severity + location + suggestion)
- Strengths (what's done well)
```

**Claude Code wrapper** (SKILL.md additions):
```yaml
---
name: code-review
description: Reviews code for correctness, security, and maintainability. Triggers on /review or when user asks for code feedback.
---
```
Plus: references/ for detailed checklists, progressive disclosure.

**Cursor wrapper** (.cursorrules addition):
```markdown
## Code Review Mode
When I ask you to review code, follow these criteria: [paste universal core]
```

Same brain, different packaging.

---

## Lesson 1.4 — Mapping Between Platforms

### Concept

Here's a translation table for porting skills:

| Claude Code | Cursor | Windsurf | Copilot | Universal Term |
|-------------|--------|----------|---------|----------------|
| SKILL.md | .cursorrules | .windsurfrules | copilot-instructions.md | Instruction file |
| `name` frontmatter | (N/A — always loaded) | (N/A) | Agent name | Identity |
| `description` frontmatter | (N/A) | (N/A) | Agent description | Trigger text |
| references/ | @-file references | (inline) | (inline) | Extended knowledge |
| scripts/ | (terminal commands) | (terminal) | (limited) | Deterministic actions |
| Progressive disclosure | (not available) | (not available) | (not available) | Context management |
| Memory system | (not available) | (not available) | (not available) | State persistence |

**Handling missing capabilities:**

When porting to a platform that lacks a feature:
- **No progressive disclosure** → Keep instructions concise; inline the most critical references
- **No trigger matching** → The skill is always active; add "When to activate" section so the agent self-filters
- **No memory** → Rely on file-based state or accept statelessness
- **Limited tools** → Express intent and let the agent use what it has

---

## Lesson 1.5 — Anti-Patterns

### Hard-Coded Tool Names
```
BAD:  "Use the Grep tool to search for..."
GOOD: "Search the codebase for..."
```
The agent knows how to search. Tell it *what* to find, not *which tool to use* — unless a specific tool is critical for correctness.

### Platform Path Assumptions
```
BAD:  "Read ~/.claude/memory/progress.md to check status"
GOOD: "Check learning progress from your persistent state"
```

### Over-Specified Invocation
```
BAD:  "When the user types /review followed by a file path..."
GOOD: "When the user requests a code review..."
```
Slash commands are a Claude Code convention. The universal intent is "user wants a review."

### Portability Theater
Don't abstract for portability if:
- You genuinely only use one platform and don't plan to change
- The skill relies heavily on platform-specific features (hooks, MCP servers)
- The overhead of abstraction exceeds the skill's complexity

Portability is a design principle, not a religion. Apply it where it earns its keep.
