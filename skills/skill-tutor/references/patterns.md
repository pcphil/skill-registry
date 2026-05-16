# Pattern Library

A living reference of skill design patterns. Each pattern addresses a recurring challenge in skill authoring.

**Format:** Present each pattern as: Name → Problem → Solution → Example → Portability rating.

---

## Pattern: Universal Core / Platform Wrapper

**Problem:** You want a skill that works across multiple agent platforms without rewriting the logic for each one.

**Solution:** Separate your skill into two layers: a universal core (intent, logic, criteria, examples) and a thin platform wrapper (file format, trigger config, tool-specific syntax). Write the core first, then wrap it for each target platform.

**Example:** A code review skill with shared criteria (correctness, security, maintainability) wrapped in SKILL.md for Claude Code and .cursorrules for Cursor.

**Portability:** This IS the portability pattern — it's the foundation for all others.

---

## Pattern: Intent Over Mechanism

**Problem:** Skills that name specific tools or commands break when moved to a different agent.

**Solution:** Express what you want accomplished, not how to accomplish it. Say "search the codebase for X" not "use the Grep tool to find X." The agent will map intent to its available tools.

**Example:**
- Mechanism: "Run `git diff --cached` using Bash, then Read each changed file"
- Intent: "Review all staged changes in the current commit"

**Portability:** High — every agent can interpret intent. Only add mechanism when a specific approach is critical for correctness.

---

## Pattern: Progressive Disclosure

**Problem:** Large skill instructions consume context window, reducing the agent's working memory for the actual task.

**Solution:** Layer information by urgency:
- Level 1 (always loaded): Name + description (~100 words)
- Level 2 (on trigger): Core instructions (<500 lines)
- Level 3 (on demand): Detailed references, schemas, examples

**Example:** A database skill with core SQL principles in SKILL.md, detailed schema docs in references/schema.md loaded only when the agent needs them.

**Portability:** Medium — Claude Code supports this natively. On other platforms, approximate by keeping instructions concise and linking to files the agent can read.

---

## Pattern: Self-Filtering Activation

**Problem:** On platforms without trigger matching (Cursor, Windsurf), a skill is always in context. It needs to know when to activate vs. stay quiet.

**Solution:** Include a "When to activate" section that describes the situations (not commands) where the skill applies. The agent uses this to self-filter.

**Example:**
```markdown
## When to Activate
- User is writing or modifying test files
- User asks about testing strategy
- User's code changes lack corresponding tests

## When to Stay Quiet
- User is exploring or reading code
- User is working on documentation
- Another specialized mode is already active
```

**Portability:** High — works on every platform. On Claude Code, this supplements the description-based trigger.

---

## Pattern: Minimal Tool Assumptions

**Problem:** Different agents expose different tools with different names and capabilities.

**Solution:** Assume only the universal capabilities: read files, write/edit files, search content, execute commands. Don't assume named tools exist. When a specific tool IS required, document it as a dependency.

**Example:**
```markdown
## Dependencies
This skill requires:
- File search capability (any form)
- File read/write capability
- Command execution (for running tests)

Optional (enhances but not required):
- Web search (for documentation lookup)
- Memory/state persistence (for progress tracking)
```

**Portability:** High — explicitly declaring dependencies makes porting straightforward.
