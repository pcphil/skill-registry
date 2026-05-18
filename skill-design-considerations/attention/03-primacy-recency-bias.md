# Primacy / Recency Bias

## What it is

In any list of instructions, the first item and the last item are recalled most reliably. Items in the middle receive significantly less attention. This is a micro-scale version of the lost-in-the-middle problem, operating at the level of individual instruction lists rather than full documents.

**Primacy bias** — the first item in a list is processed when the model's attention is fully available and the context is least cluttered. It anchors how the rest of the list is interpreted.

**Recency bias** — the last item is closest to the point of generation. It's the most recently "seen" instruction and most likely to influence the immediately following output.

Items 2 through N-1 in a list compete with each other in the attention-poor middle zone.

## Why it happens

Both effects have roots in how sequence models process information:

- **Primacy**: Early tokens in a sequence influence all later tokens via the attention mechanism. The first instruction sets the frame for interpreting subsequent ones.
- **Recency**: Later tokens are closer to the generation step in the forward pass. Less time passes between "seeing" the instruction and acting on it, reducing the chance it's overridden by other signals.

These effects are amplified by training data patterns: instructions tend to state the most important thing first (human writing convention), so models learn to weight early items more heavily. Similarly, the last paragraph before "please do this" in human writing is usually the most proximate request.

## Analogy

Writing a grocery list throughout the day, you remember milk (the first thing you wrote, before the list got long) and eggs (just added five minutes ago). The six items in the middle? You're standing in the store trying to recall them. Instruction lists work the same way — first and last stick reliably; the middle is the graveyard. Design your lists knowing this, not hoping it won't apply.

## Symptoms

- Rule #1 and rule #8 in a list are followed; rules #3–#6 are frequently violated
- The last step in a workflow is executed correctly; middle steps are skipped or reordered
- Adding a rule at the end of a list temporarily "fixes" a compliance issue; adding it in the middle doesn't
- Multi-item instructions produce outputs that match the first and last items but miss middle requirements
- Skill has 8 workflow steps; model reliably executes steps 1 and 8, inconsistently executes 2–7

## Fix

**Structure lists with primacy and recency in mind:**

- Item 1: most critical constraint
- Items 2 to N-1: supporting details (accept that these get less reliable attention)
- Item N: second most critical constraint, or a summary/reminder of item 1

This is counterintuitive — most writers put conclusions last. For instruction lists, put the most important thing first AND last.

**Keep lists short:**

The longer the list, the larger the middle zone and the more items fall into it. 3-item lists have no middle zone. 5-item lists have a small one. 10-item lists have a large dead zone.

Target: 3–5 items per list. If you need more, split into separate sections with their own headers — each section's first and last items get full attention.

**Use structure to create multiple "edges":**

Section headers reset the primacy/recency dynamic. Each new section's first item gets primacy attention. Use this deliberately:

```markdown
## Step 1: Requirements
1. Extract objective (primacy — gets full attention)
2. Identify triggers
3. Confirm negative triggers (recency — gets good attention)

## Step 2: Platform
1. Detect from context (primacy)
2. Ask if ambiguous (recency)

## Step 3: Generate
1. Load platform reference (primacy)
2. Apply format exactly (recency)
```

6 instructions split across 3 sections, each with its own primacy/recency pair. Much more reliable than a flat list of 6.

**Repeat the most critical rule:**

State it first. Restate it last. Optionally embed it mid-workflow at the moment it's relevant.

```markdown
**Required: confirm platform before generating.**

## Workflow
1. Confirm platform
2. Load reference
3. Extract requirements
4. Generate output — platform must be confirmed before this step

**Reminder: do not generate without confirmed platform.**
```

## Example

**Bad — critical constraint in the middle:**

```markdown
## Rules
1. Use kebab-case for file names
2. Keep SKILL.md under 500 lines
3. Always include negative triggers — this is the most important rule
4. Use intent-based language
5. One file per platform
```

Rule 3 ("most important rule") is in position 3 of 5. It's in the middle zone. It will be violated more than rules 1 and 5.

**Good — critical constraint at edges:**

```markdown
## Rules
1. Always include negative triggers in every generated skill
2. Keep SKILL.md under 500 lines; move excess to references/
3. Use intent-based language ("search the codebase", not tool names)
4. One file per platform; use correct file names per platform conventions

**Required in all outputs: negative triggers must be defined.**
```

Most important rule is first. Restated as a bold reminder at the end. Middle rules 2–3 are important but survivable if occasionally missed. Rule 4 gets recency position because it's the last item.
