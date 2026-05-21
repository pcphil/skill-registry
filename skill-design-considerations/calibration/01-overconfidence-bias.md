# Overconfidence Bias

## What it is

A skill that instructs the model to produce output directly — "generate the implementation", "create the plan", "write the skill" — pushes the model toward confident, complete-looking output even when the model's actual knowledge is limited, the requirements are ambiguous, or the task genuinely requires information the model doesn't have. The model follows the instruction to produce and suppresses the natural signal that would surface uncertainty.

The result is output that reads as authoritative but contains fabrications, wrong assumptions, or low-confidence guesses presented as facts.

## Why it happens

Models are trained to follow instructions and to be helpful. "Generate X" is a clear instruction. Completing it requires producing output. Producing output requires resolving ambiguity — and the model resolves it silently, filling gaps with plausible-sounding content rather than stopping to flag them.

Skills amplify this by removing the natural pause points where the model would otherwise hedge. A bare user request ("write me a plan") allows the model to say "I'd need to know X first." A skill instruction ("generate the plan from the requirements provided") frames the requirements as already sufficient and removes the model's justification for asking.

## Analogy

A consultant hired to deliver a report by Friday. They don't have all the data they need, but the deadline is the instruction. They fill the gaps with reasonable-sounding estimates, present them as findings, and deliver on time. The report looks complete. The errors are invisible until someone checks the sources. The deadline instruction didn't allow for "I need more time to verify this."

## Symptoms

- Skill output contains specific facts, statistics, or code that appear correct but are wrong
- Model generates a complete implementation for an underspecified requirement without flagging gaps
- User asks a follow-up question and discovers the skill's output was built on incorrect assumptions
- Model produces lists of items (frameworks, libraries, methods) that include fabricated entries
- Skill works well on well-specified inputs but silently degrades on ambiguous ones

## Fix

**Build uncertainty checkpoints into the workflow:**

Before the generation step, add a verification gate where the model assesses whether it has what it needs:

```markdown
## Workflow
1. Assess requirements — identify any missing, ambiguous, or unverifiable information
2. Surface gaps — if gaps exist, list them and ask before proceeding
3. Generate — only after gaps are resolved or user accepts stated assumptions
```

**Allow the model to state assumptions explicitly:**

Instead of suppressing uncertainty, give the model permission to name it:

```markdown
Before generating, state any assumptions you're making about unspecified details.
If you're uncertain about a specific fact, say so — do not fabricate.
```

**Limit open-ended generation requests:**

The more open-ended the generation instruction, the more the model will fill in. Constrain scope:

```markdown
# Overconfident framing
Generate a complete implementation plan.

# Calibrated framing
Generate an implementation plan for the parts we've confirmed.
Mark any section that requires information not yet provided as [TBD: <what's needed>].
```

**Treat knowledge limits as valid output:**

Give the model explicit permission to produce partial output:

```markdown
If you don't know something with confidence, produce a partial output with
clearly marked gaps rather than filling those gaps with guesses.
A correct partial is better than a complete but wrong output.
```

## Example

**Bad — instructs full generation with no uncertainty gate:**

```markdown
## Workflow
1. Read the user's requirements
2. Generate a complete implementation based on those requirements
3. Deliver the output
```

On underspecified input, the model generates a complete implementation — filling every gap with its best guess. Gaps are invisible in the output.

**Good — uncertainty checkpoint before generation:**

```markdown
## Workflow
1. Read the requirements
2. Identify what's clear, what's ambiguous, what's unknown
3. If anything is ambiguous or unknown:
   - List the gaps explicitly
   - Ask the user to resolve them, or state the assumptions you'll proceed with
4. Generate — scoped to confirmed requirements, with [TBD] markers for unresolved sections
5. Deliver — note any sections that require further input

## Output Standard
Never fabricate specific facts (version numbers, API signatures, statistics).
If uncertain, use placeholder syntax and explain what's needed to fill it.
```

Same workflow. Uncertainty is surfaced and handled. The output is honest about what it knows.
