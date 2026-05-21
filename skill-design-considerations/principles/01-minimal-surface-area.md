# Minimal Surface Area

## What it is

A skill should define the smallest behavioral contract necessary to accomplish its purpose. Every rule, workflow step, format instruction, persona, and capability beyond the minimum is a surface area that can conflict with other skills, override user intent, break across model versions, or produce unexpected behavior in edge cases.

Minimal surface area means: if removing it doesn't break the skill's core function, remove it.

## Why it matters

Each additional instruction in a skill:
- Consumes attention budget (see over-specification, attention/02)
- Creates a potential conflict point with co-loaded skills (see skill-composition-blindness, composition/01)
- Adds a dependency that may break on model update (see version-assumption, robustness/04)
- Increases the chance the model applies it outside the skill's intended scope

Skills fail not just because they're missing something — they also fail because they have too much. A skill with 3 precise rules is more reliable than one with 12 rules, 3 of which contradict each other and 4 of which are never actually relevant.

## How to apply

**One skill, one responsibility:**

Before writing a rule, ask: is this rule about the skill's core function, or is it a nice-to-have addition? If it's the latter, leave it out.

```markdown
# Scope test: is this rule core or extra?
Core: "Confirm target platform before generating" (affects correctness of output)
Extra: "Use emoji in section headers for visual clarity" (nice-to-have, not core)
```

**Audit every constraint for necessity:**

For each rule in your skill's Rules or Constraints section, apply this test:
- What breaks if I remove this rule?
- If nothing breaks: remove it.
- If something breaks: it's core. Keep it.

**Minimize behavioral anchors:**

Behavioral anchors (instructions that change how the model responds to ALL inputs, not just the skill's task) are the highest-impact surface area. Audit all "always" and "before every" instructions and scope them tightly:

```markdown
# High surface area — global anchor
Always ask for platform confirmation before responding.

# Minimal surface area — scoped anchor
Before generating a skill file: confirm the target platform.
```

**Prefer narrow format rules over comprehensive style guides:**

A skill that specifies "output in YAML frontmatter with a body section" is smaller than one that specifies font, heading level, list style, emoji usage, and line length — and it's more portable.

**Keep skills focused; create a second skill if scope genuinely expands:**

If a skill is growing to cover two separate concerns, split it. Two focused skills with minimal surface area compose better than one large skill that tries to cover everything.

## Example

**Before — too much surface area:**

```markdown
## Rules
- Always confirm platform before any output
- Format all responses with YAML frontmatter
- Use emoji in section headers for clarity
- Keep output under 200 lines
- Ask at most 2 clarifying questions
- Never produce output without confirmation
- Always greet the user when activated
- Include a summary section at the end of every output
- Use numbered lists for workflow steps
- Reference the taxonomy in skill-design-considerations when giving advice
- Suggest reading skill-tutor after completing
- Bold all key terms on first mention
```

Most of these rules are nice-to-have. Many conflict with user preferences, compose badly with other skills, or will be applied outside the skill's scope.

**After — minimal surface area:**

```markdown
## Rules
- Confirm target platform before generating (correctness depends on it)
- Keep skill body under 150 lines; move detail to references/
- Ask at most 2 clarifying questions, then generate with stated assumptions
```

Three rules. All core. Each one survives the necessity test: removing any one of them would break the skill's core function.
