# Monolithic Workflow

## What it is

A skill's workflow is a single flat list of numbered steps where every step has the same structural weight and no grouping, even though the steps represent fundamentally different behavioral modes. Steps that gather information, steps that generate output, steps that wait for user input, and steps that verify results are all presented as peers in one undifferentiated sequence.

The model cannot distinguish between behavioral modes when they're all formatted identically:
- **Gathering** (ask questions, wait for answers) requires patience and follow-up
- **Generating** (produce artifacts) requires sustained creative output
- **Waiting** (pause for user) requires stopping and not proceeding
- **Verifying** (check output against criteria) requires critical evaluation of own work

Without structural differentiation, the model treats the entire workflow as a uniform to-do list and either rushes through wait points, skips verification steps, or re-enters gathering mode during generation.

## Why it happens

Numbered lists are the easiest structure to write. Authors draft workflows as sequential instructions: "first do this, then this, then this." The mental model is a recipe — and recipes work because a human cook naturally knows when to switch modes (mixing vs. baking vs. decorating). Models don't have that implicit knowledge; they need structural signals.

The problem compounds with length. A 5-step flat workflow is usually fine. A 12-step flat workflow with three behavioral mode switches buried in the numbering will break.

## Analogy

A film script doesn't write dialogue, stage directions, and camera instructions in the same format. Dialogue is character name + colon + words. Stage directions are italicized in brackets. Camera angles are capitalized. A script written as one continuous paragraph — dialogue, blocking, camera — would confuse any crew member trying to figure out which part is their job. Structural formatting is the signal that tells each department what mode to be in.

## Symptoms

- Model generates output during a step that was meant to wait for user input
- Model asks questions during a generation phase ("what format would you like?" mid-generation)
- Verification steps are rushed or skipped entirely — model moves from "generate" to "present" without checking
- User corrects the model for not pausing when expected, or for pausing when it should have continued
- Model completes the entire workflow in a single response, including steps that require user interaction between them

## Fix

**Identify behavioral mode switches.** Read through the workflow and mark each step with its mode: Gather, Generate, Wait, Verify, Present. Where the mode changes, that's a phase boundary.

**Use named phases for mode changes:**

```markdown
## Workflow

### Phase 1: Requirements (Gather)
1. Ask about target audience
2. Ask about constraints
3. Confirm requirements before proceeding

### Phase 2: Generation (Generate)
4. Produce the artifact based on confirmed requirements
5. Apply formatting rules

**Wait for user review before proceeding.**

### Phase 3: Refinement (Iterate)
6. Incorporate feedback
7. Present revised version
```

**Add explicit wait points.** Bold, separated, unambiguous. Not "(wait for response)" parenthetical in a step — a standalone structural marker:

```
**Stop here. Present output and wait for user feedback before Phase 3.**
```

**Apply the behavioral mode test.** If removing a step would change *what kind of thing* the model is doing (not just *which thing*), it deserves phase separation. Removing "ask about constraints" doesn't change the mode (still gathering). Removing "generate the artifact" changes from gathering to... nothing. That's a phase boundary.

**Keep flat structure for uniform-mode workflows.** Not every workflow needs phases. If all steps are the same behavioral mode (five generation steps in sequence), a flat list is correct. Phases are for mode switches, not for visual organization.

## Example

**Bad — flat list with hidden mode switches:**

```markdown
## Workflow
1. Ask the user what they want to build
2. Clarify requirements
3. Confirm understanding
4. Generate the component code
5. Add tests
6. Present the result to the user for review
7. Incorporate user feedback
8. Finalize and present the updated version
```

Steps 1-3 are Gather mode. Step 4-5 are Generate mode. Step 6 is a Wait point. Steps 7-8 are Iterate mode. But the model sees eight equal steps. Common failure: model races from step 1 through step 8 in a single response, generating everything including "incorporating" feedback that hasn't been given yet.

**Good — phases with explicit mode signals:**

```markdown
## Workflow

### Gather
1. Ask what the user wants to build
2. Clarify requirements (language, framework, constraints)
3. Restate requirements and confirm before generating

### Generate
4. Produce component code matching confirmed requirements
5. Write tests covering core behavior

**Present output. Wait for user review before continuing.**

### Refine
6. Incorporate specific feedback from user
7. Present updated version with a summary of changes made
```

Same content. Phases signal mode switches. Wait point is structural, not inline. Model knows when to stop, when to generate, when to iterate.
