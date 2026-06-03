# Archetype Mismatch

## What it is

A skill uses the structural pattern of the wrong archetype for its actual purpose. Three structural archetypes exist, each designed for a fundamentally different interaction shape:

| Archetype | Structure | Characteristic |
|-----------|-----------|----------------|
| Teaching | Curriculum, assessment, progress tracking, loops, subcommands | Multi-session, stateful, learner-paced |
| Generator / Meta | Named phases, review loops, artifact production | Multi-step, iterative, output-focused |
| Simple Utility | Flat workflow, no state, single pass | One-shot, stateless, task-focused |

Archetype mismatch means applying the wrong structural template. A single-purpose utility skill built with the full ceremony of a teaching skill — assessment, curriculum references, progress tracking, five subcommands — when it needs a flat 30-line workflow. Conversely, a genuine multi-session teaching skill written as a simple utility — flat steps, no state, no progression — that collapses when the user returns for session two.

## Why it happens

Authors tend toward one of two failure modes:

**Over-engineering:** The author has seen well-structured teaching or generator skills and copies their ceremony for everything. Assessment sections, memory tracking, subcommands — all added "because good skills have them." The structure becomes cargo cult.

**Under-engineering:** The author defaults to the simplest structure (flat list of steps) regardless of task complexity. Works for a demo, fails in sustained use. The assumption: "if I describe the steps clearly enough, the model will figure out state management on its own." It won't.

## Analogy

A form letter, a textbook, and a recipe are all documents — but you wouldn't write a recipe in textbook format (chapters, exercises, review questions for "preheat oven to 375"). You wouldn't write a textbook as a flat recipe ("step 1: learn calculus, step 2: learn linear algebra"). The content might be correct either way, but the structural mismatch makes it unusable for its purpose.

## Symptoms

- Simple utility skill has sections that are always empty or skipped (assessment with nothing to assess, progress tracking for a one-shot task)
- Teaching skill loses all context between sessions because it has no state management
- Generator skill runs its "review loop" zero times because the flat structure has no loop mechanism
- Model invents its own structural workarounds — adding state tracking commentary the skill didn't ask for, or skipping ceremony sections with "not applicable"
- Skill works perfectly in a single demo conversation but fails on second invocation or with a different user

## Fix

**Classify before writing.** Ask three questions:
1. Does this skill need to remember anything between sessions? → Not a utility
2. Does this skill produce an artifact that needs iterative refinement? → Generator
3. Does this skill teach or guide over multiple interactions? → Teaching

**Start flat, add structure only when earned.** Begin with Simple Utility. Add named phases only when you have at least two stages that behave differently. Add state/memory only when the skill demonstrably needs to resume. Add subcommands only when users need multiple distinct entry points.

**Archetype smell test:**
- Utility with an Assessment section → Probably over-engineered. Does the skill actually need to gather requirements, or can it extract them from the invocation message?
- Teaching skill without memory/progress → Under-engineered. How does it know what the learner already covered?
- Generator without a review loop → Missing its core mechanism. When does the user approve or reject the artifact?

**Use the decisions framework.** For each structural element (phases, references, subcommands, memory, budget allocation), apply the decision criteria from the decisions reference: does this element earn its attention cost?

**Name and path hygiene (applies to every archetype).** Two conventions are cheap and portable:

- **Name the skill in gerund form** — `processing-pdfs`, `analyzing-spreadsheets`, `reviewing-skills`. The `-ing` verb states the activity, which reads naturally in a registry and reinforces single-responsibility (see scope-creep, composition/02). The `name` field allows lowercase letters, numbers, and hyphens only. Noun phrases (`pdf-processing`) are an acceptable fallback; vague names (`helper`, `utils`) are not.
- **Use forward slashes in every path**, even when authoring on Windows: `references/guide.md`, not `references\guide.md`. Backslashes break on Unix runtimes, and skills are meant to be portable.

## Example

**Bad — utility skill with teaching ceremony:**

```markdown
## On Invoke
Check memory for prior formatting sessions.
If returning user, ask what they'd like to review.
If new user, begin assessment.

## Assessment
Ask the user:
1. What languages do they format?
2. What style guides do they follow?
3. What is their experience level with formatters?

## Workflow
Module 1: Understanding Format Rules
- Lesson 1.1: What formatting means...

## Subcommands
- `/formatter` — start
- `/formatter next` — next lesson
- `/formatter status` — show progress
```

This skill formats code. It doesn't need lessons, assessment, progress, or subcommands. The teaching archetype adds ~80 lines of structure the model must process on every invocation, all of it irrelevant.

**Good — same skill as utility:**

```markdown
## On Invoke
Extract target file and style preference from user message. If ambiguous, ask.

## Workflow
1. Read the target file
2. Apply formatting rules for the detected language and stated style
3. Present the diff for user approval
4. Apply on confirmation

## Rules
- Preserve semantic content — formatting only, no logic changes
- Show diff before applying — never auto-apply
```

Flat, stateless, one-shot. Matches the task shape.
