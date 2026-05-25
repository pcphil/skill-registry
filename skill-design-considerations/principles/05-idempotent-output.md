# Idempotent Output

## What it is

A skill that generates artifacts — skill files, configurations, plans, structured documents — should produce structurally consistent output when given the same input. Field ordering, section structure, formatting decisions, and constraint application should be stable across runs. The exact wording may vary (models are stochastic), but the shape of the output should not.

Idempotent output means: if you run the skill twice with the same requirements, you get two outputs that are structurally interchangeable — not two outputs that differ in format, field order, or which sections are included.

## Why it matters

Output instability has compounding costs:

- **Downstream consumers break.** Scripts, parsers, or workflows that consume skill output depend on consistent structure. If field ordering changes between runs, `grep`-based extraction fails.
- **User trust erodes.** When the same request produces differently-structured output, users stop trusting the skill and start manually editing everything.
- **Revision becomes expensive.** If the skill regenerates with a different structure, the user has to re-review the entire output rather than just the changed section (see feedback-loop-absence, interaction/04).
- **Comparison is impossible.** Diffing two outputs to find meaningful changes requires structural consistency. Format variation creates noise that obscures real differences.

## How to apply

**Define output schema explicitly:**

Don't leave structural decisions to the model's preference. Specify the exact sections, their order, and which are required vs. optional:

```markdown
## Output Structure (in this order)
1. YAML frontmatter: name, description (required)
2. ## On Invoke (required)
3. ## Workflow (required, numbered steps)
4. ## Rules (required, max 5)
5. ## Boundaries (optional — include only if negative triggers were defined)
6. ## Completion (required)
```

**Specify field ordering in structured output:**

For YAML, JSON, or other structured formats, name the field order:

```markdown
## Frontmatter Fields (in this order)
name: <value>
description: <value>
triggers: <list>
```

"In this order" eliminates a common source of output variation.

**Use templates from assets/ for structural consistency:**

Templates enforce structure by example. Place them in `assets/` (not loaded into context) and instruct the model to copy the structure:

```markdown
Copy the structure from `assets/skill-template.md`.
Fill in the sections with the user's requirements.
Do not add, remove, or reorder sections.
```

**Constrain optional content with clear inclusion criteria:**

Sections that appear sometimes but not others are a source of variation. Define when each optional section is included:

```markdown
## Optional Sections
- ## Boundaries: include only when negative triggers are defined
- ## References: include only when content exceeds 150 lines and must be split
- ## Fallbacks: include only when the skill targets multiple platforms

If the condition is not met: omit the section entirely (no empty placeholder).
```

**Test for consistency:**

Run the skill twice with identical input. Diff the outputs. Structural differences (section order, field order, which sections appear) are bugs. Wording differences are expected.

## Example

**Before — structure varies between runs:**

```markdown
## Workflow
1. Gather requirements
2. Generate the skill file
3. Deliver output
```

Run 1 produces: frontmatter → On Invoke → Workflow → Rules → Boundaries.
Run 2 produces: frontmatter → Workflow → Rules → On Invoke (no Boundaries).
Same input. Different structure. User can't rely on the output format.

**After — structure pinned:**

```markdown
## Output Structure (required, in this order)
1. YAML frontmatter: `name`, `description` (always present)
2. `## On Invoke` — one-line trigger summary
3. `## Workflow` — numbered steps
4. `## Rules` — 3–5 constraints, bulleted
5. `## Boundaries` — include if negative triggers were defined; omit otherwise
6. `## Completion` — always present

Do not add sections beyond this list.
Do not reorder sections.
Copy structure from `assets/skill-template.md` if available.
```

Same input → same structure. Wording varies; shape doesn't.
