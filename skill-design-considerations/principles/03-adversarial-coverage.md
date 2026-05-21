# Adversarial Coverage

## What it is

A skill is only as reliable as the inputs it has been tested against. Testing only the happy path — correct platform, valid file, cooperative user — proves the skill works under ideal conditions. Real usage is messier: users paste the wrong file, provide no context, ask questions outside the skill's scope, or interact in ways the author didn't anticipate. Adversarial coverage means deliberately testing these cases before shipping.

"Adversarial" doesn't require malicious intent. It just means: what happens when the input isn't what you expected?

## Why it matters

Skills that work in demos break in production not because the happy path fails — but because off-path inputs trigger undefined behavior. The model follows the skill's workflow as far as it goes, then defaults to general behavior for the rest. That default may conflict with what the skill was trying to accomplish.

Testing adversarial inputs before shipping surfaces these gaps while they're cheap to fix. After shipping, every user who hits the undefined behavior discovers the gap the hard way.

## How to apply

**Test against these input categories for every skill:**

| Category | Example |
|----------|---------|
| Missing required input | User provides no platform, no file, no target |
| Wrong type of input | User pastes code where a skill file was expected |
| Partial input | User provides some required fields but not others |
| Out-of-scope request | User asks something clearly outside the skill's domain |
| Adversarial trigger | Request that looks like the skill's topic but isn't |
| Conflicting signals | User says one thing in the request, provides another in context |
| Empty input | User sends a blank message or just "go" |
| Injection-style input | Input contains instruction-like text (see prompt-injection-blindness, security/01) |

**Run each test and check:**

- Did the skill surface a visible, specific failure? (see fail-visible, principles/02)
- Did the skill stay within its domain, or drift into another?
- Did any undefined behavior produce output that looked correct but wasn't?
- Did the skill's constraints hold, or did they get overridden by the unusual input?

**Fix gaps before shipping:**

Every test that produces unexpected behavior is a missing case in the skill's workflow. Add it:

```markdown
## Edge Cases
- No platform provided → ask for it (see Blocking Conditions)
- Non-skill-file input → "This doesn't look like a SKILL.md. [description]. Should I proceed anyway?"
- Out-of-scope request → "This is outside this skill's scope. [what skill covers]. [redirect or exit]."
```

**Use negative triggers to handle adversarial triggers:**

Skills with vague descriptions fire on too many inputs (see trigger-pollution, robustness/01). Negative triggers are the primary defense:

```markdown
description: "Creates and refines SKILL.md files for agent platforms. NOT for general writing,
code generation, or questions about Claude Code features."
```

**Adversarial coverage is a pre-ship checklist:**

Before marking a skill ready:
- [ ] Tested with missing required input
- [ ] Tested with wrong input type
- [ ] Tested with out-of-scope request
- [ ] Every off-path case produces a visible, specific response
- [ ] No off-path case produces plausible-looking wrong output

## Example

**Before — happy-path only:**

The skill was tested with:
- Valid SKILL.md file → correct review delivered
- Platform specified → correct platform-specific output generated

Not tested: what happens when the user pastes something that isn't a SKILL.md? What if they provide a path to a directory? What if they ask about skill design theory instead of a specific file?

**After — adversarial coverage applied:**

```markdown
## Edge Cases (added after adversarial testing)

- Input is not a SKILL.md file:
  "This looks like [file type], not a skill file. Should I review it as-is,
  or did you mean to provide a different file?"

- Input is a directory path:
  "That's a directory. Which skill file inside it should I review?
  Found: [list SKILL.md files in directory]"

- Request is conceptual (not about a specific file):
  "You're asking about skill design in general — not asking me to review a specific file.
  For that, try the skill-tutor skill. Or provide a skill file to review."

- No input at all:
  "To start a review, paste a skill file or provide its path."
```

Every off-path case has a visible, specific response. No case produces plausible wrong output.
