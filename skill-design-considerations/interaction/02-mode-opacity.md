# Mode Opacity

## What it is

Skills with multiple modes, phases, or states don't always tell the user which mode is currently active or what the skill expects next. The user interacts with a skill that behaves differently depending on where it is in its own workflow — but with no visible indicator of which state they're in. They don't know whether the skill is gathering requirements, generating output, waiting for confirmation, or doing something else entirely.

## Why it happens

Skill authors know their own state machine. When writing a multi-phase workflow, the author understands the distinction between "gathering requirements" and "generating output" — but doesn't think to make that distinction visible to the user, because it seems obvious from the conversation flow.

In practice, conversations branch, users skip steps, and the model advances or retreats through the skill's phases in ways the user doesn't track. Without explicit state signals, the user ends up sending inputs that don't match what the skill currently expects.

## Analogy

A phone menu system that starts playing music when it's on hold, plays a different tune when it's transferring you, and stays silent when it's processing — but doesn't say "please hold while we transfer you" or "processing your request." The caller has no idea whether the call is working, failed, waiting for input, or ringing. Every silence or sound requires guessing what state the system is in.

## Symptoms

- User provides detailed input when the skill is in confirmation mode (expects only yes/no)
- User answers a question the skill already gathered in a previous step — because they lost track
- User asks "are you done?" because there's no indication the skill finished or is still running
- Model doesn't recognize user input as relevant because it doesn't match the expected input for the current phase
- Skill feels unpredictable — behavior changes between turns with no visible reason

## Fix

**Signal mode transitions explicitly:**

When the skill moves between phases, say so:

```markdown
**[Gathering requirements]** I need a few details before generating...

**[Generating]** Working on the skill file now...

**[Review]** Here's the draft. Let me know if you want changes or say "looks good" to finalize.
```

**Open every response with current state when it's non-obvious:**

```markdown
## Output Format
Begin each response with a one-line state indicator when the user may not know what the skill expects:
[Phase: Requirements] / [Phase: Generating] / [Phase: Awaiting Confirmation]
```

**State what the skill expects from the user:**

Don't just output content — tell the user what to do next:

```markdown
# Bad — delivers output with no next-step signal
Here's the generated skill file.

# Good — delivers output and states expected response
Here's the generated skill file.
**Next:** Review it and say "ship it" to finalize, or describe any changes you want.
```

**Make mode transitions part of the workflow definition:**

```markdown
## Workflow
1. **[Requirements mode]** Ask for: platform, skill name, trigger description
   → Transitions to Generate when all three are confirmed

2. **[Generate mode]** Produce the skill file
   → Transitions to Review when file is delivered

3. **[Review mode]** Wait for: approval ("looks good", "ship it") or revision request
   → Transitions to Generate on revision
   → Completes on approval
```

**Define what "done" looks like from the user's perspective:**

Users should never have to guess whether the skill is finished. The terminal state should be explicit:

```markdown
On completion: output "**[Done]** Skill file finalized." — then return to default behavior.
```

## Example

**Bad — phases implicit, no state signals:**

```markdown
## Workflow
1. Ask for requirements
2. Generate the skill
3. Iterate until approved
4. Deliver final version
```

The model knows where it is. The user doesn't. After step 2, the user might ask a question (model re-enters step 1), paste new requirements (model re-generates), or say "looks good" (model finalizes). The model has to guess intent from each message because there's no state signal.

**Good — explicit mode signals in workflow and output:**

```markdown
## Workflow
1. **[Requirements]** Gather: platform, skill name, trigger description, negative triggers
   - Output format: numbered list of what's been confirmed, inline ask for what's missing
   - Transition signal: "Requirements confirmed — generating now."

2. **[Generating]** Produce skill file
   - Output: skill file in a code block, followed by:
     "**[Review]** Confirm to finalize or describe changes."

3. **[Review]** Await approval or revision
   - On approval: output "**[Done]** Skill saved." and exit
   - On revision: output "**[Revising]** [what's changing]..." and re-enter step 2

## State Indicator Rule
Prefix each response with the current phase in brackets when transitioning:
[Requirements] / [Generating] / [Review] / [Done]
```

State is always visible. User always knows what the skill expects next.
