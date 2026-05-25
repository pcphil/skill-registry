# Section Role Confusion

## What it is

Content placed in the wrong structural section of a SKILL.md. Rules written inside the workflow. Workflow steps disguised as rules. Assessment logic buried in On Invoke. Boundary declarations hidden in the description.

Each section has a distinct cognitive role for the model:

| Section | Role | Model treats content as... |
|---------|------|---------------------------|
| Frontmatter | Identity and trigger matching | Metadata — not behavioral |
| Opening line | Behavioral framing | Persistent posture for entire session |
| On Invoke | Initialization gate | One-time entry logic |
| Workflow | Sequential actions | Steps to execute in order, then move past |
| Rules | Hard constraints | Always-active invariants applied to every response |
| Boundaries | Scope limits | What to refuse or redirect |

When content lands in the wrong section, the model processes it through the wrong lens. A rule in the workflow section gets treated as a step to execute once and move past. A workflow step in the rules section gets treated as an always-active constraint applied to every response.

## Why it happens

Skill authors think in terms of *what to say*, not *where to say it*. The structural sections look like arbitrary groupings, so authors place content wherever it comes to mind during drafting. The workflow section is usually the longest, making it a natural dumping ground.

Additionally, some content is genuinely dual-purpose — a constraint that is both a rule (always true) AND a workflow gate (check at step 3). Authors place it in one section and assume the model carries it into the other. It doesn't.

## Analogy

A restaurant kitchen has stations: prep, grill, plating, expediting. If the grill cook finds a plating instruction taped to the grill hood, they read it while grilling — they don't suddenly switch to plating mode. The instruction gets processed through the wrong operational lens. Same words, wrong station, wrong behavior.

## Symptoms

- Model executes a "rule" once during the workflow step where it appears, then ignores it afterward
- Model treats a workflow step as a global constraint, applying it to every response even when irrelevant
- On Invoke section contains detailed assessment questions that should be in a Requirements phase
- Model asks boundary-related questions ("should I do X?") instead of refusing outright, because the boundary was stated as a soft preference in the description rather than a hard limit in the boundaries section
- Reordering sections changes model behavior in unexpected ways — a sign that content is section-dependent but placed in the wrong section

## Fix

**Diagnostic: the section swap test.** Move the suspicious content to its intended section. If behavior improves, the content was misplaced.

**Heuristic for placement:**
- Has a verb and an order ("do X then Y") → **Workflow**
- Is an always-true invariant ("all output must be...") → **Rules**
- Describes what the skill refuses → **Boundaries**
- Runs once at activation → **On Invoke**
- Sets behavioral posture for the whole session → **Opening line**

**For dual-purpose content** (both a rule and a workflow gate): state it in both places. Once in Rules as the invariant. Once in the relevant workflow step as a checkpoint. Repetition across sections is not redundancy — it's structural reinforcement.

**Audit pass:** After drafting, read each section in isolation and ask: "Does every item here belong to this section's role?" Flag anything that feels like it wandered in from another section.

## Example

**Bad — rule buried as workflow step:**

```markdown
## Workflow
1. Gather requirements from user
2. Detect target platform
3. All output must use positive constraint grammar — never use negation
4. Generate skill body
5. Format and present for review

## Rules
- Keep SKILL.md under 500 lines
```

Step 3 is a rule, not a workflow step. Model executes it at step 3 (maybe rephrases something), then moves to step 4 and forgets about positive grammar for the rest of generation.

**Good — rule in Rules, checkpoint in Workflow:**

```markdown
## Workflow
1. Gather requirements from user
2. Detect target platform
3. Generate skill body — verify positive constraint grammar before proceeding
4. Format and present for review

## Rules
- All constraints must use positive framing (actions to take, not things to avoid)
- Keep SKILL.md under 500 lines
```

The grammar constraint lives in Rules (always active). The workflow step references it as a verification checkpoint. The model applies it throughout generation AND explicitly checks at step 3.
