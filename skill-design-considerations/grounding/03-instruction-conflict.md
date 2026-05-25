# Instruction Conflict

## What it is

Instruction conflict occurs when a skill's instructions contradict instructions from another source — the system prompt, CLAUDE.md, another loaded skill, or the user's direct message. The model receives two valid-seeming directives that cannot both be satisfied, and must choose one. The choice is not deterministic and often not the one the skill author intended.

Conflicts range from obvious (skill says "always ask before generating"; user says "just generate it") to subtle (skill says "use formal language"; system prompt says "be concise and direct" — formal and direct can conflict in tone).

## Why it happens

Modern agent setups layer instructions from multiple sources:
- System prompt (set by the platform or deployment)
- User-level config (CLAUDE.md, settings files)
- Project-level config (project CLAUDE.md)
- Loaded skills (one or more)
- User's live message

All of these land in the context window simultaneously. The model has no explicit conflict resolution protocol — it uses attention and recency as implicit tiebreakers. Generally:
- More recent instructions tend to win over earlier instructions at the same level (recency bias)
- System prompt instructions generally outweigh user messages by design, but strong user-turn phrasing can sometimes displace skill-level or CLAUDE.md instructions
- Stronger language ("always", "never", "you must") can override weaker language at the same precedence level

But this is not reliable. The model may try to satisfy both instructions partially, producing output that fully satisfies neither.

## Analogy

Two managers simultaneously text contradictory instructions to the same employee — one says "approve the request immediately," the other says "escalate for review first." The employee has to pick one. They might pick wrong, or try to satisfy both and fully satisfy neither. A model facing conflicting instructions does exactly this — and unlike the employee, it won't tell you it received two messages. It just produces output that looks subtly wrong.

## Symptoms

- Skill behavior changes depending on what else is in the system prompt
- Skill works in isolation but breaks when deployed with other skills or in a custom agent
- Model seems to "half-follow" the skill — satisfying some constraints but not others
- User's direct instruction ("just do it") overrides skill's workflow ("confirm before doing")
- Two loaded skills give contradictory instructions and model alternates between them unpredictably
- Skill formatted output gets reformatted by a higher-priority system-level style instruction

## Fix

**Narrow the skill's domain:**

The smaller and more specific the skill's domain, the less likely it collides with other instructions. A skill that says "when creating SKILL.md files, use this format" is much less likely to conflict than one that says "always structure output this way."

```markdown
## Scope
This skill governs only SKILL.md file creation and platform rule generation. It does not modify behavior for any other task type.
```

**Acknowledge the hierarchy:**

Some conflicts are resolvable if the skill explicitly acknowledges the priority order:

```markdown
## On Conflict
If the user gives a direct instruction that contradicts this workflow (e.g., "skip the confirmation step"), follow the user's instruction. The workflow is a default, not a hard override.
```

This prevents the model from trying to satisfy both and failing at both.

**Avoid style/tone instructions:**

Style instructions (tone, verbosity, formatting) are the most likely to conflict with system-level instructions. Keep skills focused on behavioral workflow, not presentation style. Let the platform's style instructions win on style.

**Test in context:**

A skill that works in isolation must be tested in its actual deployment context — with the full system prompt and any other active skills. Conflicts that don't appear in isolation will appear in deployment.

**Skill isolation pattern:**

For skills that must enforce strong constraints, scope them explicitly:

```markdown
## Domain
This skill is active only during skill-creation tasks. Outside that scope, this skill's instructions do not apply and should not influence behavior.
```

**Resolve known conflicts explicitly:**

If you know a conflict exists (e.g., your CLAUDE.md says "be terse" but the skill needs detailed structured output), resolve it in the skill body:

```markdown
## Output Format
Skill output is structured and detailed by design. The general terse-response preference does not apply to skill file generation — skill files must be complete to be usable.
```

## Example

**Conflict scenario:**

CLAUDE.md: "Keep all responses concise. One paragraph max unless asked for more."

Skill body: "Generate complete SKILL.md files including frontmatter, On Invoke, Core Workflow, Rules, and Boundaries sections."

These conflict. The model may generate a truncated skill file trying to satisfy both.

**Resolution in skill body:**

```markdown
## Output Format
Generated skill files must be complete regardless of general response-length preferences. A truncated skill file is not functional. Length constraints from other instructions do not apply to skill file content.
```

**Conflict from user message:**

User: "Just create the skill, skip all the questions."
Skill: "Ask for platform, negative triggers, and workflow before generating."

**Resolution in skill body:**

```markdown
## On User Shortcut
If the user asks to skip the question phase, proceed with stated assumptions and list them at the top of the output: "Assumed: Claude Code format, no existing skill detected, using provided description as-is." Generate immediately after stating assumptions.
```

The conflict becomes a defined edge case with a clear resolution path.
