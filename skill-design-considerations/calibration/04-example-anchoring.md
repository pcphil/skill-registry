# Example Anchoring

## What it is

When a skill includes examples to illustrate desired output, the model treats the example as a template rather than an illustration. It copies incidental details — variable names, structure, formatting choices, specific values — that were arbitrary in the example but become mandatory in the model's interpretation. The example was meant to show "this kind of thing"; the model reads it as "this exact thing."

This is distinct from hallucination amplification (calibration/02), which covers fabrication. Example anchoring doesn't fabricate — it over-fits. The output is real but rigidly patterned on the example's specifics rather than the underlying principle.

## Why it happens

Examples are the strongest grounding signal available in a skill. They show the model a concrete instance of what correct output looks like — and the model's pattern-matching optimizes for producing output that resembles the example as closely as possible. The model cannot reliably distinguish which parts of the example are essential (the structure, the format) from which are incidental (the variable names, the specific values, the exact number of items).

This is amplified when:
- The skill includes only one example (no variation to learn from)
- The example is detailed and specific (more incidental details to anchor on)
- The instruction text is vague about what matters ("generate output like this")
- The example is placed close to the generation point (high recency weight)

## Analogy

A cooking student watches a chef plate a dish: protein at 6 o'clock, sauce swoosh from 10 to 2, garnish at the top. The student replicates the exact placement on every dish they make — including salads, desserts, and soups. They learned the plating, not the principle behind it (balance, contrast, focal point). The chef showed one instance; the student treated it as the only valid arrangement.

## Symptoms

- Skill shows a `Profile` component as an example; model names every subsequent component with similar conventions even when inappropriate
- Example uses 3 items in a list; model always generates exactly 3 items regardless of context
- Example uses a specific YAML field order; model forces that order even when another order is more logical
- Changing the example changes the model's output in ways that shouldn't matter (renaming a variable in the example renames variables in all output)
- Multiple users report that skill output "all looks the same" despite different inputs

## Fix

**Use minimal examples — strip incidental detail:**

Include only what's structurally necessary. Replace specific values with generic placeholders where the specific value doesn't matter:

```markdown
# Over-detailed example (anchors on specifics)
name: profile-viewer
description: Displays user profile information including avatar and bio.

# Minimal example (anchors on structure)
name: <skill-name>
description: <one-line description of what it does>
```

**Vary incidental details across multiple examples:**

If you must include detailed examples, include at least two with different incidental details. The model learns "what's common" across examples:

```markdown
## Examples
Example 1: name: data-fetcher, description: Retrieves and caches API responses.
Example 2: name: code-reviewer, description: Analyzes code for quality issues.
```

Different names, different domains, different descriptions — the model learns the pattern, not the specifics.

**State what's essential vs. incidental:**

Explicitly label which parts of the example matter:

```markdown
## Example (structure matters, values are illustrative)
The `name` field must be kebab-case (as shown). The `description` text
is illustrative — yours will differ based on the skill's actual purpose.
```

**Prefer principles over examples when possible:**

An instruction like "use kebab-case for the name field" is more reliable than showing an example with a kebab-case name and hoping the model generalizes. Use examples to clarify ambiguous principles, not as the primary instruction.

**Move examples to references/ and load only when needed:**

Examples in SKILL.md load every time and anchor every generation. Examples in `references/examples.md` load only when the model or user needs clarification:

```markdown
For output format examples, see `references/examples.md`.
Load only if the format instructions above are unclear.
```

## Example

**Bad — one detailed example, no separation of essential vs. incidental:**

```markdown
## Output Format
Generate output like this:

name: weather-dashboard
description: Displays real-time weather data for configured locations.
triggers:
  - weather
  - forecast
  - temperature
```

Every user's skill will have weather-related naming, exactly 3 triggers, and the same field ordering — because that's what the example showed.

**Good — minimal example with explicit guidance:**

```markdown
## Output Format
- `name`: kebab-case, descriptive of the skill's function
- `description`: one sentence, starts with a verb
- `triggers`: 2–5 keywords specific to the skill's domain

Structure (values are placeholders — yours will differ):
name: <your-skill-name>
description: <verb-first one-liner>
triggers:
  - <domain-keyword-1>
  - <domain-keyword-2>
```

The model knows what to vary and what to preserve. No incidental details to anchor on.
