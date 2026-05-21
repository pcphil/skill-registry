# Persona Capture

## What it is

When a skill assigns a strong persona to the model ("You are a strict code reviewer", "Act as a senior architect"), the model internalizes that persona globally — not just for the skill's task. After the skill finishes, the persona persists across the session, shaping responses to unrelated requests. The model stays "in character" without realizing the skill's context has ended.

This is distinct from state leakage (grounding/02), which covers skill behavioral anchors that persist. Persona capture is specifically about identity assignment: the model adopts a self-concept that influences how it frames and delivers all subsequent responses, regardless of topic.

## Why it happens

Persona instructions ("You are X") are one of the most effective grounding mechanisms available. Models trained on instruction-following have learned to take persona assignments seriously — they update their tone, priorities, and decision-making to match the described identity. This is useful within a skill's scope and actively harmful outside it.

The model has no built-in mechanism to "exit" a persona when a skill ends. It follows the last persona instruction it received until something overrides it. If nothing does, the persona runs for the rest of the session.

## Analogy

An actor hired to play a strict detective in one scene doesn't stop playing the detective between takes. They stay in character in the green room, at lunch, during unrelated conversations — because "stay in character" was the last direction they received. The director didn't say "and when we cut, go back to being yourself." That's the missing instruction.

## Symptoms

- User asks an unrelated question after using a skill; model responds in an unexpected tone or with unexpected constraints
- A skill that uses "You are a senior architect" persona causes model to reject "simple" implementations long after the skill's task ended
- Model applies a skill's expertise framing to requests that don't require it ("As a strict reviewer, your variable name is acceptable but could be improved")
- User notices the model's behavior changed mid-session without an obvious cause
- Persona from one skill conflicts with persona from another loaded skill

## Fix

**Scope persona assignment to the skill's task:**

Replace unconditional identity assignment with task-scoped framing:

```markdown
# Bad — global persona
You are a strict code reviewer. Apply rigorous standards to all output.

# Good — task-scoped
When reviewing code as part of this skill: apply strict standards,
flag all violations, and prioritize correctness over brevity.
```

**Add an explicit persona exit:**

Define what the model returns to after the skill's task completes:

```markdown
## On Complete
Return to default assistant behavior. Do not carry reviewer framing
into subsequent responses unless this skill is explicitly re-invoked.
```

**Prefer role-framing over identity assignment:**

"When doing X, reason like a senior architect" is safer than "You are a senior architect." Role-framing is conditional; identity assignment is global.

```markdown
# Identity assignment (risky)
You are a Python expert who prioritizes performance.

# Role-framing (safe)
When generating Python code in this skill, optimize for performance
and apply expert-level idioms.
```

**Test for bleed:**

After running the skill end-to-end, send an unrelated request. Check whether the persona's tone, priorities, or constraints appear in the response. If they do, add a stronger exit instruction.

## Example

**Bad — persona leaks globally:**

```markdown
## On Invoke
You are a rigorous technical reviewer. You do not accept vague requirements,
untested assumptions, or imprecise language. Apply this standard to every
response you give during this session.

## Workflow
1. Read the code or document provided
2. Apply strict review criteria
...
```

"Every response you give during this session" guarantees bleed. After the review task, the model applies rigorous reviewer standards to simple questions.

**Good — persona scoped and exited:**

```markdown
## On Invoke
For this review task: apply strict review criteria — flag vague requirements,
untested assumptions, and imprecise language.

## Workflow
1. Read the code or document provided
2. Apply review criteria defined in references/critique.md
...

## On Complete
Review is finished. Return to default assistant behavior.
Reviewer framing does not carry forward to subsequent requests.
```

Same rigor, contained scope. The model knows when the persona ends.
