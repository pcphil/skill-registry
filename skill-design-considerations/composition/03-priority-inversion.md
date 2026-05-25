# Priority Inversion

## What it is

When multiple skills are active simultaneously, the model resolves conflicts by implicit recency and proximity rather than by declared priority. The skill whose instructions appear closest to the current request in context tends to dominate — even if it's the lower-priority skill for the task at hand. The intended primary skill loses to a secondary one without any conflict being visible.

This is distinct from skill composition blindness (composition/01), which covers skills that don't account for other skills existing at all. Priority inversion assumes both skills are at least passively aware they share space — but neither has declared how conflicts should be resolved, so resolution defaults to an artifact of how context is ordered.

## Why it happens

Models weight recent context more heavily than distant context (see lost-in-the-middle, attention/01). In a loaded skill environment, the skill that was loaded last, or whose instructions are positioned closest to the user's message, has the highest effective weight at inference time.

This creates an accidental priority system based on load order — which has nothing to do with which skill is actually responsible for the current request. A debug-helper skill loaded after a code-generation skill will dominate code generation tasks simply because it appeared later in the context.

## Analogy

Two managers send the same employee different instructions for a project. The employee defaults to whichever manager's email they read last — not because that manager has authority over the project, but because it's fresher in their mind. The first manager's instructions are technically still "active" but functionally subordinate. Neither manager thought to say "my instructions take priority for this project type."

## Symptoms

- Correct skill is loaded but wrong skill's format/workflow is applied to the request
- Skill behavior changes depending on which other skills are active in the same session
- A utility skill (debugging, formatting) overrides a domain skill (code generation, review) on tasks clearly in the domain skill's territory
- Adding or removing an unrelated skill changes the behavior of a different skill
- User explicitly invokes one skill ("use the code reviewer") but gets behavior from another

## Fix

**Declare request-type ownership:**

Every skill should state which types of requests it owns. The model uses these declarations to resolve which skill should lead when multiple are active:

```markdown
## Owns
This skill handles: skill file creation and modification requests.
Yields to other skills for: code review, debugging, documentation, general coding.
```

**Include a trigger specificity signal:**

More specific triggers win. If a skill is meant to be secondary (a utility that activates only when the primary skill requests it), say so:

```markdown
## Activation
Secondary skill — activate only when explicitly requested by another skill
or by the user naming this skill directly. Do not self-activate based on
topic match alone.
```

**Establish a yield protocol between known co-loaded skills:**

If two skills commonly co-exist and have overlapping domains, define a handoff:

```markdown
## On Conflict with Code Review Skill
If a code review skill is active and the request involves reviewing code:
yield to it. This skill handles generation; the review skill handles evaluation.
Complete generation first, then signal that review may proceed.
```

**Test load-order sensitivity:**

Load the skill in two orders:
1. This skill last (recency advantage)
2. This skill first (recency disadvantage)

Behavior should be the same in both cases. If it isn't, add stronger ownership declarations and yield conditions.

## Example

**Bad — no priority declaration, vulnerable to load order:**

```markdown
## Skill: Code Generator
Generates implementation code based on requirements.

## Skill: Debug Helper  
Analyzes code for bugs and suggests fixes. Responds to any code-related request.
```

"Any code-related request" means the debug helper activates on generation requests too. Load the debug helper last and it dominates. The user asked for generation; they got debugging analysis.

**Good — ownership declared, conflict resolved:**

```markdown
## Skill: Code Generator
## Owns
Code generation requests: producing new implementations from requirements.
Yields to debug/review skills when the request is about existing code.

---

## Skill: Debug Helper
## Owns
Debugging and error analysis of existing code.
Does not activate for new code generation requests — yields to generation skills.

## Activation
Activate when: user provides code with an error, test failure, or explicit debug request.
Do not activate when: user is asking for new code to be written from scratch.
```

Ownership is declared. Yield conditions are mutual. Load order doesn't change the outcome.
