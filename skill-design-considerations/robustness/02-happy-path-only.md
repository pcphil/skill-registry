# Happy-Path-Only Design

## What it is

Happy-path-only design occurs when a skill defines thorough instructions for what to do when everything goes right, but provides zero guidance for when it doesn't. No handling for incomplete user input, ambiguous requests, failed detection, conflicting requirements, or unexpected responses. When the model hits an edge case, it improvises — and improvisation without guidance usually produces inconsistent, low-quality results.

Most skills are written this way because authors mentally simulate the ideal interaction. The user asks exactly what the skill expects, provides all required information, and accepts the first output. Real usage is messier.

## Why it happens

Skill authors are optimistic. They design for the user they wish they had — one who provides a complete, unambiguous request that maps cleanly onto the skill's workflow. Edge cases feel like rare exceptions not worth specifying.

They're not rare. In practice:
- Users give partial information and expect the skill to ask for the rest
- Detection heuristics misfire (no CLAUDE.md present, ambiguous platform signals)
- Requirements conflict ("make it short but include all the details")
- User changes their mind mid-workflow
- The skill's workflow doesn't apply cleanly to an unusual variant of the request

Without explicit guidance, the model defaults to its training-time behavior at each branch point — which may be completely inconsistent with the skill's intent.

## Analogy

A recipe that only tells you what to do when every ingredient is available and nothing burns. It's a great recipe — for the 30% of cooks who have everything on hand and a perfect oven. The other 70% are standing in the kitchen wondering what to substitute for buttermilk and whether the smoke means it's done. A recipe without substitutions and troubleshooting notes isn't finished; it's just optimistic.

## Symptoms

- Skill works perfectly in demos, inconsistently in production
- Model asks no clarifying questions when input is clearly ambiguous — just guesses
- Skill fails silently when detection logic finds no match (e.g., no platform signal found)
- User provides half the required info; model either halts or invents the rest
- Edge cases produce outputs that are plausible but wrong — no error signal, just drift
- Adding more rules to the happy path doesn't fix edge-case behavior

## Fix

**Define at least one fallback for each decision point:**

Every branch in the workflow needs a "what if this fails" path. It doesn't need to be exhaustive — just enough to give the model a defined action rather than a guess.

```markdown
## Platform Detection
Detect platform from context (see signals table).
If no signal found: ask the user directly before proceeding.
If signals conflict: list detected signals and ask user to confirm.
```

**Handle the three most common failure modes explicitly:**

1. **Incomplete input** — what to ask, in what order, with what limit (e.g., "ask at most 2 clarifying questions, then proceed with stated assumptions")
2. **Ambiguous request** — how to resolve (ask vs. pick most likely and state assumption)
3. **Conflicting requirements** — which constraint wins, or how to surface the conflict to the user

**Use assumption statements instead of halting:**

When the model lacks required info and asking would be disruptive, define what assumption to make and how to communicate it:

```markdown
If platform is unknown and asking is not appropriate, assume Claude Code format.
State the assumption at the top of output: "Assumed: Claude Code — specify a different platform to regenerate."
```

**Define a recovery path for workflow interruption:**

If the user abandons the workflow mid-step and returns later, or pivots to a different request, what should the model do?

```markdown
## On Interruption
If the user asks an off-topic question during skill generation, answer it briefly, then offer to resume: "Want to continue the skill we were building?"
```

## Example

**Bad — happy path only:**

```markdown
## Workflow
1. Extract objective from user description
2. Detect target platform
3. Load platform reference
4. Generate skill output
5. Confirm with user
```

What happens if step 2 fails? What if step 1 gives ambiguous output? Undefined. The model guesses.

**Good — edge paths defined:**

```markdown
## Workflow
1. Extract objective from user description
   - If objective is unclear: ask one clarifying question before continuing
2. Detect target platform from context signals
   - If no signal: ask user which platform before loading reference
   - If multiple signals conflict: list them, ask user to confirm
3. Load platform reference from `references/<platform>.md`
   - If reference not found: tell user, list available platforms
4. Generate skill output per platform spec
5. Confirm with user
   - If user requests changes: apply and re-confirm
   - If user abandons: save progress note, exit cleanly
```

Same 5 steps. Each has a defined failure path. The model never needs to improvise.
