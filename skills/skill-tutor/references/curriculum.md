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
- Claude Code: SKILL.md + references + scripts
- Cursor: .cursorrules, context files
- Windsurf: .windsurfrules, workflows
- Copilot: instructions files, custom agents
- What they share vs. where they diverge

1.3 **Universal Core, Platform Wrapper**
- Pattern: write the "brain" once, wrap it per platform
- What belongs in the universal core (intent, logic, examples)
- What belongs in the wrapper (trigger syntax, tool names, file paths)
- Example: a code review skill expressed for 3 platforms

1.4 **Mapping Between Platforms**
- Translation table: Claude Code concepts → equivalents elsewhere
- Handling capabilities that don't exist on all platforms
- Graceful degradation vs. platform-specific branches

1.5 **Anti-Patterns**
- Tight coupling to one agent's quirks
- Assuming specific tool names or invocation syntax
- Embedding platform paths in core logic
- Over-engineering portability for a single-platform skill

### Exercise
Take an existing Claude Code skill and extract its universal core. Write a 1-paragraph "portability brief" describing how it could adapt to Cursor.

---

## Module 2: Skill Anatomy

**Goal:** Master the structure and metadata that make a skill discoverable, loadable, and effective.

### Lessons

2.1 **The SKILL.md Contract**
- Frontmatter: name, description, and why description is critical
- Body: role, instructions, examples
- Length budget: why 500 lines matters (context window cost)

2.2 **Progressive Disclosure**
- Level 1: metadata (always loaded, ~100 words)
- Level 2: SKILL.md body (loaded on trigger)
- Level 3: references, scripts, assets (on-demand)
- Deciding what goes where

2.3 **Trigger Design**
- Writing descriptions that trigger correctly
- Avoiding false positives and false negatives
- Explicit invocation vs. contextual detection

2.4 **Directory Layout**
- When to use references/ vs. scripts/ vs. assets/
- Naming conventions
- Keeping it flat

---

## Module 3: Prompt Engineering for Skills

**Goal:** Write skill instructions that produce consistent, high-quality agent behavior.

### Lessons

3.1 **Imperative vs. Descriptive Instructions**
3.2 **Scoping Behavior — What Not to Do**
3.3 **Examples as Specification**
3.4 **Handling Ambiguity and Edge Cases**
3.5 **Voice and Tone Calibration**

---

## Module 4: Tool & Resource Design

**Goal:** Know when and how to use scripts, references, and assets effectively.

### Lessons

4.1 **Scripts: Deterministic Reliability**
4.2 **References: On-Demand Knowledge**
4.3 **Assets: Templates and Boilerplate**
4.4 **Context Budget Management**

---

## Module 5: Testing & Iteration

**Goal:** Validate that skills work as intended and improve over time.

### Lessons

5.1 **Manual Testing Strategies**
5.2 **Edge Case Discovery**
5.3 **Iteration Loops: Feedback → Revision**
5.4 **Versioning and Breaking Changes**
