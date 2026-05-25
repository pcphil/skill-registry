# Version Assumption

## What it is

Skills written for a specific model version or capability level silently break when the model is updated, swapped for a different provider, or accessed through a platform with different defaults. The skill assumes a stable capability surface — specific tool names, output formats, reasoning styles, context window sizes, or instruction-following behaviors — that changes without notice.

## Why it happens

Skill authors observe the model's behavior at authoring time and write instructions that match it. The model follows a particular format. It responds to a specific phrasing. It uses certain tool names. These observations become assumptions, and the assumptions become dependencies baked into the skill's text.

Models change:
- New versions change instruction-following behavior
- Providers modify tool interfaces
- Context window sizes expand, changing what "too long" means
- Fine-tuned variants differ in tone, verbosity, and default behavior
- Platform wrappers (Claude Code, Cursor, Windsurf) evolve their skill loading mechanisms

None of these changes announce themselves to skills in the field.

## Analogy

A recipe written for a specific oven model: "Bake at 350°F for 22 minutes — this oven runs 10° hot so compensate." When the oven is replaced, the compensation is wrong. The recipe worked because of undocumented behavior in a specific appliance. Bake times are version-dependent and nobody wrote down why.

## Symptoms

- Skill works on one model version but breaks after a model update (different instruction-following defaults)
- Skill references tool names that changed in a platform update
- Skill relies on context window being "large enough" — breaks when run in a token-limited environment
- Output format degrades after a model update; the old model reliably used a format the new one ignores
- Skill works for one user (on Claude Code) but breaks for another (on Cursor) due to platform capability differences

## Fix

**Express intent, not mechanism:**

The most version-resilient skills describe what they want to accomplish, not how the model should accomplish it. Avoid naming specific tools, formats, or behaviors unless absolutely necessary.

```markdown
# Version-fragile — names a specific tool
Use the Grep tool to search the codebase for the symbol.

# Version-resilient — states intent
Search the codebase for the symbol using whatever search capability is available.
```

**State capability requirements explicitly:**

If the skill genuinely requires a specific capability (long context, tool use, etc.), declare it at the top so the model can surface the gap rather than silently fail:

```markdown
## Requirements
- Requires file search capability (to locate skill files in the codebase)
- Requires the ability to read and write files
- Works best with 100K+ context window; shorter contexts may require progressive loading
```

**Avoid hardcoded size limits based on observed behavior:**

"Keep output under 150 lines" is a design principle. "Keep output under 150 lines because that's the max the platform renders" is a version assumption. State the principle, not the inferred platform constraint.

**Test on the platforms you claim to support:**

If SKILL.md lists Claude Code, Cursor, Windsurf — test on all three before publishing. Note which capabilities each platform provides and which fallbacks the skill uses when they're absent.

**Prefer graceful degradation over hard failure:**

When a capability might not be available, give the model a fallback path:

```markdown
If file reading is available: load references/curriculum.md for lesson content.
If not available: ask the user to paste the relevant section directly.
```

## Example

**Bad — version and platform assumptions embedded:**

```markdown
## Workflow
1. Use the Grep tool to find all SKILL.md files in the project
2. Use the Read tool to load the target skill (must fit in context — files over 500 lines will be truncated)
3. Use the Edit tool to apply changes
4. Confirm with the user via the message interface
```

Every step names a specific tool. Line limits reference observed platform behavior. This breaks on any platform that doesn't have these exact tools or that changes their behavior.

**Good — intent-based with explicit requirements:**

```markdown
## Requirements
Requires: codebase search, file read/write, ability to send messages to user.
Falls back gracefully if any capability is absent (see Fallbacks section).

## Workflow
1. Locate all SKILL.md files in the project (search the codebase)
2. Load the target skill file into context
3. Apply the requested changes
4. Confirm changes with the user before finalizing

## Fallbacks
- If codebase search is unavailable: ask user to provide the file path
- If a file exceeds available context: process it in sections, ask user which section to address first
```

Same workflow. No tool-name dependencies. Degrades gracefully when capabilities are limited.
