# Curriculum: Building Portable Agent Skills

## Module 1: Portability Patterns

**Goal:** Understand how to write skills that work across multiple coding agent platforms.

### Lessons

1.1 **What "Portable" Means**
- Separating intent from platform syntax
- The universal core: every agent reads instructions and has tools
- Why portability matters even if you only use one agent today

1.2 **The Agent Interface Landscape**
- Common interfaces: system prompts, tool declarations, context injection, file-based rules
- Claude Code: SKILL.md + references/ + scripts/ + assets/
- Cursor: `.cursor/rules/*.mdc` (MDC format with frontmatter) or legacy `.cursorrules`
- Windsurf: `.windsurfrules` (plain markdown, always loaded)
- Copilot: `.github/copilot-instructions.md` (always loaded, no trigger matching)
- Aider: `CONVENTIONS.md` + files listed in `.aider.conf.yml`
- OpenCode: SKILL.md (same structure as Claude Code, different discovery paths)
- What they share vs. where they diverge

1.3 **Universal Core, Platform Wrapper**
- Pattern: write the "brain" once, wrap it per platform
- What belongs in the universal core (intent, logic, criteria, examples)
- What belongs in the wrapper (trigger syntax, file format, tool references, platform-specific features)
- Example: a code review skill expressed for 3 platforms

1.4 **Mapping Between Platforms**
- Translation table: Claude Code concepts → equivalents on each platform
- Handling capabilities that don't exist on all platforms (progressive disclosure, memory, trigger matching)
- Graceful degradation vs. platform-specific branches

1.5 **Anti-Patterns**
- Tight coupling to one agent's quirks
- Assuming specific tool names or invocation syntax
- Embedding platform paths in core logic
- Over-engineering portability for a single-platform skill

### Exercise
Take an existing Claude Code skill and extract its universal core. Write a 1-paragraph "portability brief" describing how it could adapt to Cursor.

---

## Module 2: Platform-Native Formats

**Goal:** Master the correct file format, structure, and capabilities for each platform.

### Lessons

2.1 **Claude Code: SKILL.md**
- Frontmatter: `name` and `description` only (no `globs`, `tags`, or other fields)
- Description drives trigger matching — write it as a discrimination signal
- Directory layout: SKILL.md + references/ + scripts/ + assets/
- Progressive disclosure: always-loaded (SKILL.md) → on-demand (references/) → copy-only (assets/)
- Memory system for state persistence across sessions
- Named tools (Read, Grep, Glob, Edit, Write, Bash)

2.2 **Cursor: MDC Rules**
- File location: `.cursor/rules/skill-name.mdc`
- Frontmatter: `description`, `globs` (file patterns for auto-attach), `alwaysApply`
- Context variables: `{{REPO_ROOT}}`, `{{CURRENT_FILE}}`, `{{SELECTION}}`
- Body structure: Activation Boundaries → Context & Objective → Workflow → Constraints
- Legacy format: `.cursorrules` (plain markdown, no frontmatter)

2.3 **Windsurf: .windsurfrules**
- Plain markdown, no frontmatter, no context variables
- Always loaded for every session — keep concise (<150 lines)
- Cascade hierarchy: global user rules → project rules → in-chat instructions
- Structure: Role → Stack → Workflow → Always/Never → Out of Scope

2.4 **Copilot: Instructions File**
- File: `.github/copilot-instructions.md`
- Always loaded, no activation boundaries, no trigger matching
- Suggestion-based, not agentic — no multi-step workflows
- Focus on conventions, patterns, and constraints
- Keep under 100 lines (competes with open files for context)

2.5 **Aider: Conventions**
- File: `CONVENTIONS.md` in project root, or files listed in `.aider.conf.yml`
- Plain markdown, no frontmatter, loaded every session
- Write for a developer scanning quickly, not an agent parsing steps
- Deep git integration — include commit conventions
- Keep under 200 lines

2.6 **OpenCode: SKILL.md**
- Nearly identical to Claude Code format (same directory structure)
- Extra optional frontmatter: `license`, `compatibility`, `metadata`
- Permission system: `allow`/`deny`/`ask` in `opencode.json`
- Use intent-based language (tool names differ from Claude Code)

2.7 **What's Truly Universal vs. Platform-Specific**
- Universal: name/identifier, description/purpose, workflow steps, constraints, boundaries
- Platform-specific: `globs` (Cursor), `alwaysApply` (Cursor), context variables (Cursor), memory system (Claude Code), progressive disclosure (Claude Code/OpenCode), permission system (OpenCode)
- When to use platform-specific features vs. when to stay portable

### Exercise
Create a skill for a platform you use. Then describe what would change to port it to a second platform.

---

## Module 3: Prompt Engineering for Skills

**Goal:** Write skill instructions that produce consistent, high-quality agent behavior.

### Lessons

3.1 **Imperative vs. Descriptive Instructions**
3.2 **Positive Framing — Why "Do X" Beats "Don't Y"**
3.3 **Examples as Specification (and the Anchoring Risk)**
3.4 **Handling Ambiguity and Edge Cases**
3.5 **Voice and Tone Calibration**

---

## Module 4: Tool & Resource Design

**Goal:** Know when and how to use scripts, references, assets, and progressive disclosure effectively.

### Lessons

4.1 **Scripts: Deterministic Reliability**
- When to use scripts vs. instructions
- Naming and location conventions

4.2 **References: On-Demand Knowledge**
- When to create references, naming conventions, progressive disclosure
- Structural archetypes: teaching, generator, utility
- Full reference: `references/anatomy.md`

4.3 **Assets: Templates and Boilerplate**
- When to use assets vs. references
- Template design for copy-and-modify workflows

4.4 **Context Budget Management**
- Platform size targets, SKILL.md vs. references allocation
- Decision framework for structural patterns (phases, modes, subcommands, state)
- Full reference: `references/decisions.md`

4.5 **Platform-Specific Features in Practice**
- Claude Code: progressive disclosure, memory, named tools
- Cursor: globs for auto-attach, context variables, alwaysApply
- When these features are worth using vs. when they harm portability

---

## Module 5: Skill Design Considerations

**Goal:** Recognize and prevent the failure modes that break skills in production.

### Lessons

5.1 **Attention Failures**
- Lost in the middle, over-specification, context bloat
- How to structure instructions for reliable attention

5.2 **Grounding Failures**
- Negation failure, state leakage, conversational drift, persona capture
- Building termination signals and scoped behavior

5.3 **Robustness and Composition**
- Trigger pollution, happy-path-only, platform assumptions
- Skill composition, scope creep, priority inversion

5.4 **Calibration and Interaction**
- Overconfidence, hallucination amplification, example anchoring
- Silent failure, mode opacity, feedback loops

5.5 **Adversarial Testing**
- Testing with missing input, wrong input type, out-of-scope requests
- Pre-ship checklist for skill quality

Full taxonomy: `../../skill-design-considerations/`
