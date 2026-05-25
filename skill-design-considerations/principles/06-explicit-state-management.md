# Explicit State Management

## What it is

Every decision, requirement, and intermediate result in a skill's workflow should be visible in the conversation — stated in the model's responses, not carried implicitly in context. If a decision was made in turn 3, it should be restated when it's used in turn 15. If the skill is in phase 2, the response should say so. Nothing about the skill's current state should require reading the full conversation history to reconstruct.

This is the positive-design version of context compaction fragility (robustness/05): where that document explains what breaks when state is implicit, this principle explains how to keep state explicit.

## Why it matters

Implicit state is fragile:

- **Compaction erases it.** Platforms summarize earlier turns; details established in turn 3 may not survive to turn 30. Explicit state in recent responses survives compaction because recent turns are preserved.
- **Users can't see it.** When state is implicit, the user doesn't know what the model "remembers." They can't verify whether the model is working from the right assumptions. Explicit state is auditable.
- **Sessions can't be resumed.** A new session starts with no conversation history. If state was implicit, it's gone. If it was stated explicitly in the model's last response, a user can paste that summary to resume.
- **Debugging is impossible.** When output is wrong, tracing the cause requires knowing what state the model was working from. Implicit state leaves no trail.

## How to apply

**Restate decisions at the point of use:**

Don't rely on a decision surviving from when it was made. Restate it when it affects output:

```markdown
## Workflow
1. Confirm platform → state in response: "Platform confirmed: [X]"
2. Generate output → begin with: "Generating for [X] with requirements: [list]"
```

**Include a state summary in responses at phase transitions:**

When the skill moves between phases, output the current state:

```markdown
## On Phase Transition
Summarize in each transition response:
- Current phase
- Decisions made so far
- What's needed for the next phase

Example: "Moving to generation. Confirmed: Claude Code platform, skill name 'data-fetcher',
3 triggers defined, no negative triggers specified. Generating now."
```

**Use structured state blocks for complex workflows:**

For skills with many state variables, embed a state block in responses:

```markdown
## State Block Format (include in responses when state is complex)
**State:**
- Platform: Cursor
- Skill name: code-reviewer
- Phase: Generation (step 3 of 5)
- Requirements: [list]
- Open items: negative triggers not yet defined
```

**Write to memory for cross-session persistence:**

Conversation state dies with the session. If the skill needs state to persist across sessions, use memory:

```markdown
## State Persistence
After confirming requirements, save to memory:
- Platform, skill name, core requirements
- Current phase and progress

On session resume: check memory for saved state before asking the user to re-provide.
```

**Make each response interpretable in isolation:**

A reader should understand the model's current response without reading the 20 turns before it. This doesn't mean repeating everything — it means including enough context that the response makes sense standalone:

```markdown
# Requires full history to understand
Here's the updated version with those changes applied.

# Self-contained
Here's the updated skill file (v3 for Claude Code, 'data-fetcher').
Changed: description (shortened per feedback). Everything else unchanged from v2.
```

**Design for the observer who just walked in:**

The user may resume mid-conversation after a break, or a different team member may take over. State visibility ensures continuity:

```markdown
## Response Standard
Every response during active workflow should answer, at minimum:
- What phase is this? (Requirements / Generating / Review / Done)
- What key decisions are we working from?
- What is this response delivering or asking for?
```

## Example

**Before — implicit state:**

```markdown
## Workflow
1. Ask for platform
2. Ask for requirements
3. Generate output
4. Iterate until done
```

By step 4, the platform choice and requirements are 15+ turns back. If compacted, they're gone. If the user returns after a break, they can't tell what the model is working from.

**After — explicit state throughout:**

```markdown
## Workflow
1. **Requirements** — gather platform, name, triggers, negative triggers
   → Response includes: "Confirmed: [platform], [name], [triggers]. Missing: [if any]."

2. **Generate** — before generating, state inputs:
   "Generating [name] for [platform]. Requirements: [summary]."
   → If memory is available, save confirmed state

3. **Review** — present output with state header:
   "[name] | [platform] | Draft v[N] | Awaiting review"

4. **Revise** — on each revision:
   "Changed: [what]. Unchanged: [everything else]. Now at v[N+1]."
   → Re-verify state is still accurate before applying changes

## State Rule
No response during active workflow should require reading prior turns
to understand what platform, requirements, or phase are in play.
```

State is visible in every response. Survives compaction, session breaks, and handoffs.
