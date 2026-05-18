# Trigger Pollution (False Positives)

## What it is

Trigger pollution occurs when a skill's `description` field is too vague, too broad, or uses generic keywords that match unrelated user requests. The skill activates when it shouldn't, consuming tokens, derailing the agent's actual task, and eroding user trust. In multi-skill setups, a poorly written description can cause the wrong skill to fire every time, shadowing the skill that should have activated.

The inverse — a description so narrow the skill never fires when it should — is also a failure mode, but false positives are more damaging because they actively break unrelated tasks.

## Why it happens

The `description` field is the primary signal used by the agent (or the skill-matching system) to decide whether a skill is relevant to the current task. Agents use semantic similarity, keyword matching, or a combination. If the description contains:

- High-frequency generic words ("help", "create", "generate", "code", "write")
- Domain words that apply to many tasks ("skill", "file", "project", "workflow")
- No specificity about WHAT the skill does differently from default behavior

...then it will match a wide range of unrelated requests.

Additionally, skill descriptions are often written for human readers ("Creates agent skills for coding platforms") rather than as discrimination signals for an agent making a binary activate/don't-activate decision.

## Analogy

A smoke alarm set to maximum sensitivity fires every time you make toast. It's technically doing its job — detecting heat — but in completely the wrong context. Everyone ignores it because it cries wolf constantly. A skill description full of generic keywords is that alarm: it fires on everything, helps no one, and trains the user to route around it.

## Symptoms

- Skill activates when user asks an unrelated question in the same domain
- Multiple skills compete for the same trigger; the wrong one wins
- User notices the agent "switches modes" unexpectedly mid-conversation
- Agent loads skill and then immediately determines it's not relevant — wasted tokens
- Skill designed for platform X fires when user is working on platform Y

## Fix

**Write descriptions as discrimination signals, not marketing copy:**

The description should answer: "Under exactly what conditions should this skill activate, and under what conditions should it NOT?" Include both.

**Density over length:**
- Use specific trigger keywords: exact actions ("creates", "converts", "audits"), exact domain terms ("SKILL.md", "frontmatter", "negative triggers"), exact contexts ("Claude Code skill", "Cursor rule")
- Avoid generic verbs: "helps", "assists", "handles", "manages", "works with"

**Include implicit negative triggers in the description:**
- "Activates for skill creation and editing. Does NOT activate for general coding questions or skill usage questions."
- This costs ~15 tokens and prevents most false positives

**Test the description:**
- Read your description and ask: "Could this describe 5 other things?" If yes, it's too vague.
- Ask: "Would someone unfamiliar with this skill know exactly what triggers it?" If no, add specificity.

**Use the Boundaries section as a backstop:**
- Even with a good description, some false positives will slip through. The `## Boundaries` section in the skill body handles these at runtime: "If the user is asking how to USE a skill rather than CREATE one, say 'out of scope' and stop."

## Example

**Bad — vague, triggers everywhere:**

```yaml
---
name: skill-creator
description: Creates and manages agent skills for coding projects.
---
```

"Creates and manages agent skills" matches: any question about skills, any question about agents, any creation task in a coding project. Too broad.

**Good — specific, discriminating:**

```yaml
---
name: skill-creator
description: >
  Generates new SKILL.md files and platform-specific rule files (Claude Code,
  Cursor, Windsurf, Copilot, Aider, OpenCode). Triggers when user requests a
  new skill, rule, or agent behavior definition. Does not activate for general
  coding help, skill usage questions, or questions about what a skill does.
---
```

The good version names exact artifacts, exact platforms, exact action, and states explicit non-triggers. Discrimination is tight.

**Negative trigger in body as backstop:**

```markdown
## Boundaries

- Activate only when the user is requesting creation or modification of a SKILL.md or platform rule file.
- If the user is asking how to use an existing skill: answer the question directly, do not enter skill-creation mode.
- If the user is asking a general coding question unrelated to skill authoring: answer directly, do not activate.
```
