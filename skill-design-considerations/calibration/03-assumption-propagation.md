# Assumption Propagation

## What it is

When a user states a premise — "my skill is triggering too often", "this approach doesn't scale", "Claude can't handle long contexts" — a skill that accepts that framing and proceeds builds its entire output on a foundation it never verified. If the premise is wrong, the output is wrong. The skill has propagated a false assumption through the entire workflow and produced a confident, well-structured answer to the wrong question.

## Why it happens

Skills are written to be helpful: take the user's request, process it, produce output. This flow implicitly treats the user's framing as accurate. Instruction-following models do the same — they optimize for responding to what was said, not for auditing whether what was said is correct.

Users are not always right about their own problems. A developer who says "the bug is in the authentication module" may be wrong. A skill author who says "my skill triggers too often because the description is too broad" may have misdiagnosed the cause. The model is capable of noticing these things — but only if the skill gives it permission to challenge the premise rather than just acting on it.

## Analogy

A doctor who prescribes the medication the patient asks for without diagnosing whether the patient's self-diagnosis is correct. The patient says "I have a sinus infection, I need antibiotics." The doctor writes the prescription. Efficient — but if it's a viral infection, the antibiotic does nothing and the patient doesn't get the right treatment. A good doctor asks questions before prescribing, even when the patient is confident.

## Symptoms

- Skill produces technically correct output that solves the wrong problem
- User follows the skill's advice and the underlying issue persists or worsens
- Model generates an explanation of why the user's situation has a problem it wasn't asked to question
- Skill never asks clarifying questions that challenge the user's framing, only questions that refine it
- User returns with "that didn't work" — because the original premise was wrong

## Fix

**Add a premise-check step before the core workflow:**

```markdown
## Workflow
1. Read the user's request and stated problem
2. Identify any premises or assumptions in the request that affect the diagnosis
3. If a premise seems potentially incorrect, flag it and ask — before proceeding
4. Once premises are confirmed, proceed with the core workflow
```

**Give the model explicit permission to push back:**

Without permission, the model defaults to agreeing with the user. Grant it explicitly:

```markdown
If the user's stated problem appears to have an incorrect premise,
name the assumption and ask whether it's accurate before proceeding.
Being helpful means solving the right problem, not just the stated one.
```

**Separate symptom from cause in the workflow:**

```markdown
## On Invoke
1. Identify the symptom (what the user observed)
2. Identify the cause the user has attributed to it
3. Assess whether the attributed cause is the likely actual cause
4. If the attribution seems wrong or uncertain: surface it, then proceed
```

**Define challenge-and-confirm behavior for diagnostic skills:**

Skills that diagnose problems (debugging, skill review, performance analysis) should always include a verification step before prescribing a fix:

```markdown
Before recommending a fix:
- State the root cause you're diagnosing
- Explain why you believe it's the cause, not just a symptom
- Ask the user to confirm the diagnosis before you proceed with the fix
```

## Example

**Bad — propagates the user's framing without challenge:**

```markdown
## On Invoke
The user has identified an issue with their skill. Understand the issue
they've described and generate a solution that addresses it.

## Workflow
1. Read the skill file
2. Apply the fix the user described
3. Deliver the corrected version
```

If the user's diagnosis is wrong, this workflow produces a well-executed fix to the wrong problem.

**Good — premise check before fix:**

```markdown
## On Invoke
The user has described a problem with their skill. Before generating a fix:
verify that the described problem is actually the root cause.

## Workflow
1. Read the skill file
2. Read the user's problem description
3. Assess:
   - Is the described symptom real? (confirm you can see it in the file)
   - Is the user's attributed cause the likely root cause?
   - Are there other causes that better explain the symptom?
4. If the diagnosis seems off: name the discrepancy and ask before proceeding
5. Once diagnosis is confirmed: generate the fix
6. Explain why this fix addresses the root cause, not just the symptom

## Premise Challenge Format
"You've described [symptom] and attributed it to [cause]. Looking at the skill,
I think [actual cause] is more likely because [reason]. Should I fix [actual cause]
instead, or do you want to proceed with the original approach?"
```

Same helpfulness. Checks the premise first. Produces solutions to real problems.
