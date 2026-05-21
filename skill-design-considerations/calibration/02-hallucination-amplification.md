# Hallucination Amplification

## What it is

Certain skill instruction patterns reliably trigger fabrication. Open-ended enumeration ("list all X that support Y"), authority-framing without source grounding ("as an expert, explain all the ways..."), and exhaustive inventory requests ("cover every case") push the model to generate content beyond what it can verify. The skill structure doesn't create the model's tendency to hallucinate — it amplifies it by selecting prompting patterns that are known to produce fabricated output.

## Why it happens

Language models generate the most probable next token given prior context. When a skill frames a request as "list all X," the model learns from context that a comprehensive list is expected — and generates one, including entries it cannot verify, because a long list is more consistent with "all" than a short honest one. The instruction pattern preselects for volume over accuracy.

Other amplifying patterns:
- **Authority framing**: "You are an expert" raises the model's confidence in its own output, reducing self-correction
- **No-hedge instructions**: "Give a definitive answer" suppresses the qualifications that would flag uncertainty
- **Comparative claims**: "What's the best framework for X?" invites confident rankings without data
- **Historical specificity**: "What version introduced X?" asks for exact facts the model may not reliably know

## Analogy

Asking a knowledgeable friend "name every restaurant in the city that serves authentic Szechuan food" instead of "do you know any good Szechuan restaurants?" The first framing demands comprehensiveness; the second allows honest scoping. Your friend will either make some up to seem thorough, or admit the question is too broad. The first framing doesn't give them the option to admit the limit.

## Symptoms

- Skill output contains specific names, versions, URLs, or facts that don't exist or are wrong
- Library lists include fabricated packages; framework comparisons cite made-up benchmarks
- Model gives confident specific answers to questions with genuinely uncertain or contested answers
- Output is impressive-looking but fails immediately when checked against real sources
- Adding "comprehensive" or "complete" to an instruction increases both output length and error rate

## Fix

**Replace enumeration with scoped requests:**

```markdown
# Amplifying pattern
List all frameworks that support server-side rendering.

# Calibrated pattern
Name up to 5 frameworks you're confident support server-side rendering.
For each, state what you're confident about and what the user should verify.
```

**Give the model a hard cap and a fallback:**

```markdown
Provide up to 5 examples. If you can't confirm more than that with confidence,
stop at what you know and say so. Do not generate examples you're uncertain about.
```

**Replace authority framing with task framing:**

```markdown
# Authority framing (amplifies overconfidence)
As an expert in distributed systems, explain all the failure modes.

# Task framing (preserves honest calibration)
Explain the failure modes you're most confident about.
Flag any that the user should verify with current documentation.
```

**Require source grounding for factual claims:**

```markdown
For any specific version number, API signature, or benchmark figure:
either cite a source the user can check, or mark it as [unverified — check docs].
Do not present unverified specifics as confirmed facts.
```

**Test with a verification pass:**

If the skill produces factual lists or specific claims, include a verification step:

```markdown
After generating: review each specific claim. Mark any you're uncertain about.
Better to deliver 3 verified items than 10 that include errors.
```

## Example

**Bad — patterns that amplify hallucination:**

```markdown
## Workflow
As an expert in agent skill design, generate a comprehensive list of every
platform that supports SKILL.md files. For each platform, include the exact
version that introduced support and the precise character limit for skill files.
```

This instruction requests: expert framing + "comprehensive" + "every" + "exact version" + "precise limit." Every element amplifies fabrication.

**Good — scoped, honest, verifiable:**

```markdown
## Workflow
List the platforms you're confident support skill files (or an equivalent mechanism).
For each:
- State what you know with confidence
- Mark version numbers and limits as [verify in docs] unless you're certain
- Stop at platforms you can speak to reliably — partial and honest beats comprehensive and wrong

Target: 3–5 platforms you know well. The user can extend the list from there.
```

Same intent. Scoped. Honest about limits. Output is smaller but trustworthy.
