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
- Aider: conventions files, repo maps
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

## Module 2: The Universal Poly-Agent Layout

**Goal:** Master the standard skill structure that works across all coding agents.

### Lessons

2.1 **Frontmatter: name, description, globs, tags**
- `name`: snake_case, machine-readable identifier
- `description`: 1-2 sentences rich in keywords for system parsers and semantic search
- `globs`: file patterns for IDE auto-indexing (e.g., `src/**/*.ts`)
- `tags`: categorical labels for discovery
- Why description is the most important line (drives trigger matching AND vector search)

2.2 **Activation Boundaries**
- Positive triggers: "Active when the user asks to...", "When modifying files matching..."
- Negative triggers: explicit "DO NOT activate when" rules
- Why negative triggers matter: saves tokens, prevents false activations
- The difference between trigger descriptions (metadata) and self-filtering (body)

2.3 **Context Variables**
- `{{REPO_ROOT}}` — absolute project path without hardcoding
- `{{CURRENT_FILE}}` — active file scope for analysis
- Why variables beat hardcoded paths (portability across machines AND agents)
- When to use vs. when to let the agent resolve paths itself

2.4 **Execution Goals & Persona**
- Define the high-level objective and professional standard
- One paragraph: who you are, what you do, what standard you maintain
- Scoping: what's in bounds vs. what this skill doesn't handle

2.5 **Step-by-Step Workflow (Validate → Execute → Verify)**
- Validation: what must the agent check before acting?
- Execution: concrete steps, preferred commands, design patterns
- Verification: how the agent tests its own output
- Why the verification step prevents drift and hallucination

2.6 **Strict Constraints & Anti-Patterns**
- The critical guardrail: the single most important rule
- Version locks, forbidden syntax, performance boundaries
- Architectural patterns to avoid
- How constraints differ from instructions (hard walls vs. preferences)

2.7 **Reference Boilerplate**
- Minimal code examples to anchor the agent's output format
- JSON schemas for deterministic structured output
- Why boilerplate prevents syntax hallucination
- When to inline vs. move to references/

### Exercise
Create a skill using the full Universal Poly-Agent Layout. Include all 7 sections. Subject: anything you're currently working on.

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

**Goal:** Know when and how to use scripts, references, assets, and context variables effectively.

### Lessons

4.1 **Scripts: Deterministic Reliability**
4.2 **References: On-Demand Knowledge**
4.3 **Assets: Templates and Boilerplate**
4.4 **Context Budget Management**
4.5 **Context Variables in Practice**
- Defining project-specific variables
- Platform-agnostic path resolution
- Combining variables with globs for targeted activation

---

## Module 5: Testing & Iteration

**Goal:** Validate that skills work as intended and improve over time.

### Lessons

5.1 **Manual Testing Strategies**
5.2 **Edge Case Discovery**
5.3 **The Self-Verification Pattern**
- Building verification into the skill's workflow
- What "the agent tests its own work" looks like in practice
- Choosing verification commands (test suites, linters, type checks)
5.4 **Iteration Loops: Feedback → Revision**
5.5 **Versioning and Breaking Changes**
