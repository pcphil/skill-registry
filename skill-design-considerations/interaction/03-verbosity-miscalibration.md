# Verbosity Miscalibration

## What it is

A skill that doesn't specify output volume produces responses that are either too long for the task (a paragraph of analysis for a yes/no question) or too short (a one-liner for something that needed detailed explanation). The model defaults to whatever verbosity it was trained to favor for that input type — which may be completely wrong for what the skill is trying to accomplish.

Both directions create friction: over-verbose output buries the useful signal; under-verbose output leaves the user without enough to act on.

## Why it happens

Language models don't have an intrinsic sense of how much output a task requires. They calibrate from training signals — certain input patterns correlate with certain output lengths. A skill that says "review this skill file" looks like a code review request, and the model defaults to a thorough, multi-section code review response format. But the user might have wanted a quick pass that surfaces only critical issues.

Without explicit calibration, the model matches volume to the apparent complexity of the input rather than the actual need of the user.

## Analogy

A meeting where the facilitator hasn't set an agenda length. Someone asks a process question and gets a 20-minute discussion. Someone asks for a status update and gets a one-word answer. Both are wrong. A good facilitator says "two minutes per update, five minutes for open questions." Same principle for skills.

## Symptoms

- Skill output takes a long time to read for a simple question
- Skill output for a complex task is so terse the user has to ask follow-up questions that should have been covered
- Output format changes unpredictably between similar requests
- User skims the output because it's too long; misses the key finding buried in paragraph 3
- User has to ask for more detail on something that should have been explained up front

## Fix

**Specify output length relative to task type, not absolutely:**

```markdown
## Output Format
- Quick question (yes/no, lookup): answer in 1–2 sentences max
- Single-file review: findings as a bulleted list, 1–2 lines per finding
- Full skill creation: skill file in code block + 3–5 bullet summary of design decisions
- Multi-file analysis: one section per file, each section capped at 150 words
```

**Separate signal from explanation, let user control depth:**

```markdown
Lead with the finding. Follow with explanation only if the finding isn't self-evident.
Default to finding-first, explanation-optional:

"Critical: negation-failure in Rules section. (see below for detail)"
— not —
"After carefully reviewing the skill file, I noticed that the Rules section contains
several instances of negation-based constraints, which based on research into..."
```

**Give the model a volume heuristic per output type:**

```markdown
## Volume Targets
- Status / check: 1 paragraph
- Finding list: 1 line per item, no prose between items unless critical
- Generated skill body: 50–150 lines (push detail to references/)
- Explanation: stop when you've answered the question — don't extend for thoroughness
```

**Allow user to override:** 

```markdown
Default to concise output. If the user asks for more detail on any item, expand that item only.
```

**Test with both simple and complex inputs:**

Send a simple yes/no question to the skill and a complex multi-part request. Both should produce output proportional to the question — not both at the same length.

## Example

**Bad — no volume calibration:**

```markdown
## Workflow
1. Review the skill file
2. Identify issues using the skill-design-considerations taxonomy
3. Provide a detailed report with your findings
```

"Detailed report" anchors the model to high-verbosity output for all reviews. A skill with one minor issue gets a five-section report. A skill with a critical flaw gets the same format — so the critical finding is diluted by volume.

**Good — volume calibrated to finding severity and task type:**

```markdown
## Workflow
1. Review the skill file
2. Classify findings by severity: Critical / Warning / Minor
3. Deliver findings in this format:

**Critical** (must fix before using):
- [finding] — [one-line reason] — [one-line fix]

**Warning** (recommended fix):
- [finding] — [one-line reason]

**Minor** (optional improvement):
- [finding]

If no findings in a category: omit that section.
If the skill is clean: output "No issues found." — nothing else.

## Volume Rule
Each finding: 1–3 lines max. No prose between findings.
If a finding needs more than 3 lines to explain: add it to a "Details" section at the end,
referenced from the finding as "(see Details)".
```

Same coverage. Output size scales with number and severity of findings. Critical issues don't get buried.
