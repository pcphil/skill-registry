# Silent Failure

## What it is

When a skill can't proceed — because required input is missing, a tool call failed, a file wasn't found, or an ambiguous request doesn't match any defined path — it produces one of two bad outcomes: it exits quietly with no output, or it generates something that looks like output but isn't what was needed. The user has no way to know the skill failed, what it failed on, or what to provide to fix it.

Skills that handle only the success path treat every other outcome as invisible. The model stops, hedges, or fills in — and the user sees a result that gives them no useful signal.

## Why it happens

Skill authors design for the happy path: user provides the right input, tools work, output is generated. Error conditions require explicitly anticipating what can go wrong, which requires thinking about failure at design time — something authors skip when they're focused on making the success path work.

Models also have a natural tendency to produce *something* rather than stop. When the happy path fails, the model often finds an adjacent path and follows it, generating plausible-looking output that isn't what the skill was supposed to produce. The failure is hidden inside a response that looks successful.

## Analogy

A vending machine that, when your selection is out of stock, silently gives you nothing and keeps your money. Compare to one that says "item C4 is out of stock — select another or press refund." Both vending machines failed to deliver item C4. Only one told you. The second one gives you something to act on. The first wastes your time and leaves you confused.

## Symptoms

- Skill produces empty output, off-topic output, or a generic response with no explanation
- User retries with the same input and gets the same result — because they don't know what to change
- Skill output looks plausible but addresses a slightly different task than was requested
- Tool errors in the background produce no user-visible message
- User discovers the skill didn't work only when they try to use the output

## Fix

**Define failure states explicitly:**

For each step in the workflow, define what a failure looks like and what the model should output when it occurs:

```markdown
## Workflow
1. Load the target skill file
   - If file not found: "Could not find skill file at [path]. Please provide the correct path."
   - If file is empty: "The skill file at [path] appears to be empty. Nothing to review."
2. Analyze the skill...
```

**Give every blocking condition a user-facing message:**

```markdown
## Blocking Conditions
These stop the workflow. Output the associated message when hit:

- Missing target platform → "Which platform is this skill for? (Claude Code / Cursor / Windsurf / other)"
- No SKILL.md found in provided path → "No SKILL.md found at [path]. Check the path and try again."
- Skill file exceeds context limit → "This skill file is too large to process at once. Which section should I start with?"
```

**Name the failure before asking for resolution:**

Don't just ask a question — tell the user what failed first:

```markdown
# Bad — question without context
What's the target platform?

# Good — failure named, then question
I need the target platform to generate platform-specific output — it wasn't specified.
Which platform is this skill for?
```

**Treat partial completion as a success state to be reported:**

If the skill completes some steps but not all, report what was done and what wasn't — don't silently deliver a partial result:

```markdown
Completed: requirements gathered, draft generated.
Blocked: could not confirm platform capability for [feature] — needs verification.
Next: resolve [question] to finish the remaining section.
```

## Example

**Bad — no failure handling:**

```markdown
## Workflow
1. Read the skill file provided by the user
2. Analyze it for failure modes from the skill-design-considerations taxonomy
3. Deliver a review with findings and recommendations
```

If the user provides a path that doesn't exist, or pastes something that isn't a skill file, the model either errors silently or reviews the wrong thing. The user has no signal.

**Good — failure states defined:**

```markdown
## Workflow
1. Read the skill file
   - If path not found or no file provided: stop and ask — "Please provide the skill file contents or a valid path."
   - If provided content doesn't look like a SKILL.md: name what was received and ask — "This looks like [what it is], not a skill file. Should I review it anyway, or did you mean to paste something else?"
2. Analyze — if analysis produces no findings, say so explicitly: "No failure modes detected in this skill."
3. Deliver findings

## On Empty Result
If no issues found, output "No issues detected" — not silence.
A null result should be as explicit as a finding.
```

Failure states are named. The user always knows what happened and what to do next.
