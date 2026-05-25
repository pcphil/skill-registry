# Termination Ambiguity

## What it is

A skill with no explicit completion signal leaves the model uncertain about when its task is done. Without a clear termination condition, the model stays partially in skill mode — continuing to apply the skill's workflow, constraints, and framing to subsequent requests that have nothing to do with the original task. The skill never truly ends; it fades.

This is distinct from state leakage (grounding/02), which covers specific behaviors that persist after a skill ends. Termination ambiguity is upstream: the skill never defined what "done" looks like, so the model never knows when to stop applying it.

## Why it happens

Skill authors focus on the happy path: what the skill does when it's working. The ending is assumed — "the task will eventually finish." But the model has no automatic boundary. It will continue applying active instructions until something explicit overrides them or the context resets.

When a skill's last instruction is a workflow step ("deliver the output"), the model treats task delivery as a pause, not a stop. The next user message arrives and the model asks: is this still part of the skill's task? Without a clear termination signal, it often answers yes.

## Analogy

A meeting with no agenda item for "adjourn." The team works through the items, presents conclusions — and then everyone sits there. Is the meeting over? Someone mentions something tangentially related and discussion resumes. Nobody declared the meeting closed, so it never was. A good facilitator says "we're done here, next steps are X" and the room clears. Skills need the same closing statement.

## Symptoms

- After skill completes its main output, subsequent user messages get processed through the skill's workflow instead of as new requests
- Model asks skill-specific clarifying questions for requests unrelated to the skill
- Skill's format constraints apply to output produced after the skill's task was nominally complete
- Multi-step skill loses track of whether step N has ended or step N+1 has started
- User has to explicitly say "okay, we're done with that" to reset behavior

## Fix

**Define an explicit completion signal:**

Every skill should have an `## On Complete` section that:
1. States what signals the task is done
2. Describes what the model returns to afterward

```markdown
## On Complete
Task is complete when: generated output has been confirmed by the user
or the user signals they're done (says "done", "thanks", "looks good",
closes the workflow with a dismissal).

On completion: return to default assistant behavior.
This skill's workflow, format rules, and clarifying questions
do not apply to subsequent requests.
```

**Give the model a completion checklist:**

For multi-step skills, make completion explicit per step and for the whole workflow:

```markdown
## Workflow
1. Gather requirements — complete when user confirms scope
2. Generate draft — complete when draft is delivered
3. Revise — complete when user approves or dismisses
4. **Task complete.** Return to default behavior.
```

**Name the terminal state:**

State what "done" looks like in concrete terms, not just "the task finishes":

```markdown
# Vague (bad)
Deliver the output when ready.

# Concrete (good)
Deliver the output. After delivery, wait for one of:
- User confirms ("looks good", "ship it", "done")
- User requests revision (re-enter step 3)
- User changes topic (treat as task complete, exit skill)
```

**Handle topic change as an exit signal:**

Explicitly tell the model that a topic change terminates the skill:

```markdown
If the user's next message is unambiguously outside this skill's domain,
treat the skill's task as complete and respond normally.
```

## Example

**Bad — no termination signal:**

```markdown
## Workflow
1. Analyze the requirements
2. Generate the skill body
3. Format and deliver

## Rules
- Ask for platform before generating
- Keep output under 150 lines
- Use YAML frontmatter
```

The skill ends at "Format and deliver" — but what does "deliver" mean? The model doesn't know if the next message is a revision request (still in skill), a clarifying question (still in skill), or something else entirely. Rules stay active indefinitely.

**Good — explicit termination:**

```markdown
## Workflow
1. Analyze requirements — confirm scope before proceeding
2. Generate skill body — deliver as a single code block
3. Confirm — wait for user approval or revision request
4. **Done.** On approval or topic change, exit skill and return to default behavior.

## On Complete
Skill task ends when the user confirms the output or shifts to a new topic.
After completion, none of this skill's rules apply to subsequent responses.
```

Same workflow. Clear exit. The model knows when it's finished.
