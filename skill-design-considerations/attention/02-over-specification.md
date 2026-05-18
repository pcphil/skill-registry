# Over-Specification

## What it is

Over-specification occurs when a skill contains more rules, constraints, or instructions than the model can reliably follow simultaneously. Every rule added to a skill competes with every other rule for the model's attention during generation. Beyond a threshold — roughly 5–7 active constraints — compliance degrades nonlinearly. The model satisfies the rules it noticed (usually the first few and the last one) and ignores the rest.

Over-specified skills feel thorough to their authors but produce inconsistent results in practice. The author sees all 15 rules as important; the model treats them as a suggestion menu.

## Why it happens

Models do not process a list of instructions as a checklist they consciously verify before producing output. Instead, all instructions influence the probability distribution over the next token simultaneously. When many constraints exist:

- High-frequency, salient constraints dominate (the ones using strong language or placed at the edges — see primacy/recency bias and lost in the middle)
- Low-salience constraints (passive voice, buried position, similar to other rules) are effectively ignored
- Conflicting constraints cancel each other out, leaving the model to default to training-time behavior
- The model cannot "fail gracefully" — it does not tell you which rules it dropped; it just drops them silently

Additionally, over-specified skills are harder to maintain. When behavior is wrong, it's unclear which rule is being violated or which rule is causing the violation.

## Analogy

A manager hands a new employee a laminated card with 20 rules on their first day. By lunchtime the employee remembers three — not because they're careless, but because human working memory has a hard ceiling. Models have the same ceiling, and it's lower than most skill authors assume. Handing the model 15 rules is the same as handing that employee 20: you'll get 3 followed reliably, and you won't know which 3 until it goes wrong.

## Symptoms

- Skill has 10+ rules in the `## Rules` section
- Some rules are followed consistently; others are violated consistently; the pattern feels random
- Adding a new rule breaks compliance with an existing rule
- The skill "mostly works" but has persistent edge cases that no amount of rule-adding fixes
- User and author keep appending rules to patch behavior without removing old ones

## Fix

**Ruthless prioritization:**
- Identify the 3–5 rules that, if violated, break the skill's core value. Those are your constraints.
- Everything else is either implied by those constraints or is a nice-to-have. Cut it.
- Ask for each rule: "If the model violates this, does the output become wrong or just imperfect?" Imperfect → cut.

**Compress rules into principles:**
Instead of 5 rules about output format, write 1 principle: "Output must be immediately pasteable into the target platform with no edits."

Instead of 4 rules about when to ask questions:
- Don't ask more than 2 questions
- Don't ask about things you can infer
- Don't ask if user has already answered
- Ask before generating, not after

Compress to: "Ask at most 2 clarifying questions before generating. Infer everything else from context."

**Move detail out of rules:**
Rules should state constraints, not procedures. Procedures belong in the workflow section or in `references/`. If a rule requires 3 sentences to explain, it's a procedure masquerading as a rule.

**Separate must-have from nice-to-have:**
```markdown
## Rules (required)
1. Confirm platform before generating
2. Include negative triggers in output
3. One file per platform

## Guidelines (best effort)
- Prefer intent-based language over tool-specific calls
- Keep output under 500 lines
```

The model will reliably follow "Rules" because there are only 3. "Guidelines" are soft hints.

**Set a hard limit:**
5 rules max in `## Rules`. If you need more, split into two separate skills with narrower scopes.

## Example

**Bad — 12 rules, compliance degraded:**

```markdown
## Rules
1. Always confirm the target platform before generating
2. Never blend platform formats
3. Include negative triggers in every skill
4. Use intent-based language, not tool names
5. Keep SKILL.md under 500 lines
6. Move heavy content to references/
7. Use kebab-case for all file names
8. Include a Boundaries section
9. Ask at most 2 clarifying questions
10. Don't generate without negative triggers defined
11. Name output files correctly per platform conventions
12. Always include a portability note
```

Rules 5–12 will be inconsistently followed. Rules 9 and 10 are redundant. Rules 7 and 11 are implied by platform format rules.

**Good — 4 rules, core constraints only:**

```markdown
## Rules
1. Confirm target platform before generating any output
2. Include negative triggers in every skill generated
3. Generate one file per platform; never blend formats
4. Use intent-based language throughout ("search the codebase", not "use the Grep tool")

Full format specs and file naming: see `references/<platform>.md`
```

Everything else moves to references or is dropped as implied.
