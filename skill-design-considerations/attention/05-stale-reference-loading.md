# Stale Reference Loading

## What it is

Skills that use progressive disclosure — splitting content into `references/` files loaded on demand — can load the wrong reference for the current step, or continue using a reference that was relevant earlier in the conversation but no longer applies. The model loaded `references/phase-1.md` at the start of the task and never re-evaluated; by step 4, the user is in phase 2 and the loaded content is stale.

Context bloat (attention/03) explains *why* to split content into references. This consideration addresses what goes wrong *after* splitting: the model has no signal for when to reload, invalidate, or switch references.

## Why it happens

Models don't have a built-in mechanism for reference lifecycle management. When a reference file is loaded into context, it stays there — equally salient — until the context is cleared or compressed. The model has no "this reference is no longer relevant" signal.

Causes:
- Reference was loaded at conversation start and never refreshed, even as the task progressed through phases
- Skill names references but doesn't specify which step each reference applies to
- Multiple references are loaded simultaneously; model uses content from the wrong one
- Conversation length pushes the reference load point far from the current step, reducing the model's association between "this reference is for this step"

## Analogy

A GPS that loaded the correct map tile when you started your trip but never updated as you drove. You're now three towns away, still seeing the original map. The GPS has the ability to load new tiles — but nothing told it the old one expired. You're navigating with stale data, and the GPS doesn't know it's wrong.

## Symptoms

- Multi-phase skill applies guidance from phase 1 while user is in phase 3
- Model references content from a lesson file that doesn't match the current lesson
- Skill with multiple platform references applies Claude Code conventions to a Cursor output
- User corrects the model; model briefly fixes behavior but reverts to the stale reference's guidance
- Skill works correctly in short sessions but degrades in long ones (more time for references to go stale)

## Fix

**Bind references to workflow steps explicitly:**

Don't just list available references — state which reference applies to which step:

```markdown0
## Workflow
1. Gather requirements — no reference needed
2. Detect platform → load `references/<detected-platform>.md`
3. Generate output using the loaded platform reference
4. Review — unload platform reference context; use only the output and user feedback

## Reference Map
| Step | Reference | When to load |
|------|-----------|-------------|
| 2 | references/<platform>.md | After platform is confirmed |
| 3 | references/examples.md | Only if model needs format clarification |
```

**Include invalidation signals:**

Tell the model when a reference is no longer applicable:

```markdown
After completing step 2, the content from `references/requirements-template.md`
is no longer needed. Do not apply its formatting to subsequent steps.
```

**Re-verify reference applicability at phase transitions:**

For multi-phase workflows, add a check at each phase boundary:

```markdown
## On Phase Transition
Before starting the next phase:
- Confirm which phase you're entering
- Load the reference for that phase (not the previous one)
- State which reference you're now using
```

**Use reference headers that name their scope:**

Inside each reference file, state when it applies:

```markdown
# Platform: Claude Code
Applies to: Step 3 (generation) when target platform is Claude Code.
Does not apply to: other platforms, review steps, or requirement gathering.
```

**Prefer stateless reference use:**

Load, use, and discard. Don't carry reference content forward across steps where it doesn't apply:

```markdown
For each step that needs a reference:
1. State which reference you're loading and why
2. Apply it to the current step
3. After the step: the reference's guidance applies only to what was just generated
```

## Example

**Bad — references loaded without lifecycle management:**

```markdown
## Setup
Load these references at the start:
- references/phase-1-basics.md
- references/phase-2-advanced.md
- references/phase-3-project.md

## Workflow
1. Teach Phase 1 basics
2. Teach Phase 2 advanced topics
3. Guide Phase 3 project
```

All three references load at once. Phase 1 content competes with Phase 3 content. By the time the user reaches Phase 3, Phase 1 guidance is stale but still in context and still influencing responses.

**Good — references bound to steps with explicit lifecycle:**

```markdown
## Workflow
1. **Phase 1: Basics**
   Load `references/phase-1-basics.md` at the start of this phase.
   Phase 1 content applies only to lessons in this phase.

2. **Phase 2: Advanced**
   Load `references/phase-2-advanced.md`. Phase 1 reference is no longer active —
   do not apply its guidance to Phase 2 content.

3. **Phase 3: Project**
   Load `references/phase-3-project.md`. Prior phase references are context only,
   not active guidance.

## Reference Rule
Load one phase reference at a time. State which reference is active
at the start of each response during multi-phase work.
```

Same references. Clear lifecycle. Model knows what's current and what's expired.
