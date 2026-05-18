# Skill Composition Blindness

## What it is

Skill composition blindness occurs when a skill is designed as if it will always be the only active skill in the agent's context. In real deployments, multiple skills are often loaded simultaneously — a user might have a skill for code review, one for documentation, and one for skill creation all active at once. When skills don't account for each other's existence, their instructions collide, their domains overlap, and their behavioral anchors compound in unpredictable ways.

This is related to instruction conflict (which covers any two conflicting instructions) but is caused specifically at design time: the skill author never considered that other skills would be present.

## Why it happens

Skills are authored, tested, and published in isolation. The author loads one skill, confirms it works, and ships it. The test environment is fundamentally different from the production environment where 3–5 skills may be active simultaneously.

There's no standard mechanism for skill authors to declare what other skills they're compatible with, or to define behavior when conflicts arise with unknown co-loaded skills. Each skill implicitly assumes full control.

When multiple skills each assume full control, the model must reconcile conflicting assumptions — and it has no principled way to do so.

## Analogy

Three different GPS apps giving you directions simultaneously through separate speakers. Each was designed to be the only voice in the car. One says "turn left," another says "continue straight," the third is recalculating. You're the driver — you have to pick one and hope it's right. The apps aren't broken individually; they're broken compositionally.

## Symptoms

- Skill behaves correctly in isolation but inconsistently in user's actual environment
- Two loaded skills produce conflicting format instructions; output alternates between styles
- A skill's workflow gets interrupted by another skill's trigger firing mid-task
- Behavioral anchors from multiple skills stack — model asks three sets of questions before generating anything
- User has to disable other skills to make one skill work correctly
- Skill's completion signal doesn't fire because another skill's instructions keep it "active"

## Fix

**Declare domain ownership explicitly:**

Every skill should state what domain it owns and explicitly disclaim others. This gives the model a basis for resolving conflicts when multiple skills are present:

```markdown
## Domain
This skill governs SKILL.md creation and platform rule generation only.
It does not govern: code review, documentation, testing, or general coding tasks.
If another loaded skill handles those domains, defer to it for those requests.
```

**Scope all behavioral anchors tightly:**

Behavioral anchors (instructions that change how the model responds to ALL inputs) are the primary source of composition conflicts. Scope every anchor to the skill's domain:

```markdown
# Bad — global anchor, will conflict with other skills
Before responding to any request, ask for the target platform.

# Good — scoped anchor
Before generating skill output, ask for the target platform if not already known.
```

**Define yield behavior:**

Specify what the skill should do when it detects that another skill is handling the current request:

```markdown
## On Conflict
If another loaded skill appears to be actively handling the current request, yield to it.
Only activate when the request is unambiguously within this skill's domain (SKILL.md creation).
```

**Avoid format universalism:**

Skills that declare global output format preferences conflict with every other skill. Keep format instructions scoped to the skill's own output:

```markdown
# Bad
Always format output with YAML frontmatter followed by a body section.

# Good
Format generated skill files with YAML frontmatter followed by a body section.
```

**Test with realistic skill loads:**

Before publishing, test the skill with at least 2–3 other commonly co-loaded skills active simultaneously. Identify conflicts and resolve them with scoping or yield behavior.

## Example

**Bad — assumes sole control:**

```markdown
## Rules
- Before responding to any request, confirm the target platform
- Always structure output with frontmatter first
- Ask the user to confirm before finalizing any output
- Format all code as markdown code blocks
```

Every rule is global. Loaded alongside a code-review skill, this produces a mess: the model asks for platform confirmation during code review, formats review comments with frontmatter, and demands confirmation before every code suggestion.

**Good — scoped and compositionally aware:**

```markdown
## Domain
Governs skill file creation only. Does not apply to code review, debugging, or general assistance.

## Rules
- Before generating a skill file, confirm the target platform
- Format generated skill files with frontmatter followed by a body section
- Confirm generated skill files with the user before marking creation complete

## On Conflict
If the current request is not a skill creation task, this skill's rules do not apply.
Defer to whichever skill or default behavior governs the actual request.
```

Same intent. No global anchors. Explicitly yields outside its domain.
