# State Leakage

## What it is

State leakage occurs when a skill continues to influence the model's behavior after it should have stopped. The skill was loaded for a specific task, that task ended (or the user moved on), but the skill's instructions are still in context and still shaping responses — causing the model to behave as if it's still in "skill mode" for unrelated work.

In practice this looks like: the model keeps using skill-specific formatting, asking skill-specific questions, or applying skill-specific constraints to tasks that have nothing to do with the original skill invocation.

## Why it happens

Skills are loaded into the context window and remain there until the context is cleared, compressed, or the conversation ends. Unlike function calls that return and clean up, a skill's instructions persist as static text. The model has no mechanism to "unload" a skill — it can only be instructed to stop applying it.

Without explicit exit conditions:
- The model doesn't know when the skill's task is complete
- Instructions from the skill remain equally salient for all subsequent turns
- If the skill body contains strong behavioral anchors ("always ask X before responding", "format all output as Y"), those anchors keep firing
- A user's pivot to a new topic doesn't automatically signal skill deactivation

## Analogy

An actor finishes a performance, takes a bow — and then continues speaking in character at the after-party. The play ended; the character didn't get the memo. Skills without explicit exit conditions are that actor: the task is done but the behavioral mode keeps running, bleeding into everything that comes after.

## Symptoms

- After completing a skill-creation task, the model keeps asking skill-authoring questions for unrelated requests
- Model applies skill-specific formatting (e.g., YAML frontmatter) to outputs that don't need it
- User has to explicitly say "stop doing that" or "normal mode" to reset behavior
- Skill designed for step-by-step workflows keeps prompting "what's the next step?" after the workflow completed
- In long conversations, behavior drift intensifies — earlier skills accumulate and compound

## Fix

**Explicit completion signals in the skill body:**

Every skill should define when it is done. The last section of every skill should be a completion signal:

```markdown
## Completion

When the skill file(s) have been generated and confirmed by the user, this skill's task is complete. Return to normal assistant behavior. Do not continue applying skill-creation constraints to subsequent requests unless the user starts a new skill-creation task.
```

**Scoped activation:**

Frame the skill as a mode with a clear entry and exit:

```markdown
## On Invoke
Enter skill-creation mode. All responses until completion follow this skill's workflow.

## On Complete
Exit skill-creation mode. Confirm output with user. Resume default behavior.
```

**Avoid persistent behavioral anchors:**

Behavioral anchors are instructions that change how the model responds to ALL inputs, not just skill-related ones. Examples:
- "Always ask for platform before responding" — this bleeds into non-skill responses
- "Format all output as markdown code blocks" — bleeds into general conversation
- "Begin every response by summarizing the previous step" — bleeds everywhere

Replace broad anchors with scoped ones:
- "While generating the skill, ask for platform if not yet confirmed" — scoped to generation phase
- "Format skill output as markdown code blocks" — scoped to skill output specifically

**Stateless by default:**

Design skills to be stateless unless state tracking is the skill's explicit purpose. A stateless skill gives instructions for one complete task execution and expects to be re-invoked fresh for the next. This eliminates leakage because there's no state to leak.

**Use memory for intentional state:**

If a skill genuinely needs to track progress across turns (e.g., a multi-session learning skill), use explicit memory writes rather than relying on context persistence. Context is unreliable; memory is explicit and auditable.

## Persona Capture (Identity-Specific Leakage)

The strongest form of state leakage occurs when a skill assigns an identity: "You are a strict code reviewer", "Act as a senior architect." The model internalizes persona assignments globally — not just for the skill's task — shaping tone, priorities, and decision-making for all subsequent responses.

**Why persona capture is especially dangerous:**

Persona instructions ("You are X") are one of the most effective grounding mechanisms available. Models trained on instruction-following have learned to take persona assignments seriously. This is useful within a skill's scope and actively harmful outside it.

**Role-framing vs. identity assignment:**

```markdown
# Identity assignment (risky — leaks globally)
You are a Python expert who prioritizes performance.

# Role-framing (safe — scoped to task)
When generating Python code in this skill, optimize for performance
and apply expert-level idioms.
```

"When doing X, reason like a senior architect" is safer than "You are a senior architect." Role-framing is conditional; identity assignment is global.

**Persona-specific fixes:**

- Scope persona assignment to the skill's task ("For this review task: apply strict criteria") not the session ("You are a strict reviewer")
- Add an explicit persona exit in On Complete: "Reviewer framing does not carry forward to subsequent requests"
- Test for bleed: after running the skill end-to-end, send an unrelated request and check whether the persona's tone, priorities, or constraints appear in the response

**Persona capture example:**

```markdown
# Bad — persona leaks globally
## On Invoke
You are a rigorous technical reviewer. Apply this standard to every
response you give during this session.

# Good — persona scoped and exited
## On Invoke
For this review task: apply strict review criteria — flag vague
requirements, untested assumptions, and imprecise language.

## On Complete
Review is finished. Return to default assistant behavior.
Reviewer framing does not carry forward to subsequent requests.
```

---

## Example

**Bad — persistent anchor that leaks:**

```markdown
## Rules
- Before responding to any request, confirm the target platform.
- Always structure output with frontmatter followed by a body section.
- Ask the user to confirm before finalizing any output.
```

"Before responding to ANY request" — this will persist and apply to everything after the skill runs.

**Good — scoped to the skill's task:**

```markdown
## Rules
- Before generating skill output, confirm the target platform if not already known.
- Structure skill output with frontmatter followed by a body section.
- Confirm generated skill files with the user before marking the task complete.

## Completion
Once skill files are confirmed, this workflow ends. Resume default behavior for subsequent requests.
```

Same constraints, scoped to skill generation only. The completion section explicitly signals the exit point.
