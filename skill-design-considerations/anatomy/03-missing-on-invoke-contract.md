# Missing On Invoke Contract

## What it is

A skill defines what to do during its core workflow but not what to do at the moment of activation. The On Invoke section is absent or trivially defined ("start the workflow"), so the model has no guidance on how to initialize.

Without an invoke contract, the model must improvise:
- Whether to check for prior state
- How to handle being invoked mid-conversation versus fresh
- What context to gather before entering the workflow
- How to handle re-invocation after the skill previously completed
- What to do when the invocation message is ambiguous or incomplete

The improvisation varies from invocation to invocation. Sometimes the model asks clarifying questions. Sometimes it jumps straight to generating. Sometimes it re-runs assessment for a returning user who already completed it. Each invocation feels like a different skill.

## Why it happens

On Invoke is the least intuitive section to write. Authors think of skills as "what the skill does" (workflow) and "what the skill must not do" (rules). The initialization step feels implicit — "obviously the model will start by understanding what the user wants." But "obviously" produces different behavior each time because the model has no structural signal for what "starting" means for this specific skill.

The problem is amplified for skills with state. Without an invoke contract, the model has no way to distinguish a first-time user from a returning user, or a fresh invocation from a re-invocation after completion.

## Analogy

A pilot's pre-flight checklist exists because "get ready to fly" means different things depending on whether you're starting cold, resuming after a fuel stop, or restarting after an aborted takeoff. Without the checklist, each pilot improvises — and some skip critical steps. The On Invoke section is the pre-flight checklist: different entry conditions, same reliable initialization.

## Symptoms

- Same skill produces wildly different opening responses across invocations
- Model asks assessment questions to a returning user who already answered them
- Model skips assessment and jumps to generating for a new user, producing wrong output
- Re-invoking the skill after completion either restarts from scratch (ignoring prior work) or tries to continue (when the user wanted a fresh start)
- Model begins generating before it has enough context, then backtracks mid-workflow
- User complains "it worked differently last time" with no change to the skill

## Fix

**Every skill needs an On Invoke section.** Even simple utilities benefit from explicit initialization.

**Minimum viable On Invoke for stateless skills:**

```markdown
## On Invoke
Extract [required inputs] from the invocation message.
If [any required input] is missing or ambiguous, ask before proceeding.
```

**On Invoke for stateful skills must handle three paths:**

```markdown
## On Invoke
1. Check memory for prior progress
2. If returning with saved progress:
   - Summarize where they left off
   - Ask: continue from here, or start fresh?
3. If new (no saved progress):
   - Run assessment / gather requirements
4. If re-invoked after completion:
   - State that prior run completed
   - Ask: new task, or revisit previous output?
```

**Define what "ready to enter workflow" means.** The On Invoke section should end with a clear gate: "Proceed to workflow only when [conditions are met]." This prevents the model from entering the workflow prematurely.

**Handle the ambiguous invocation.** Users often invoke skills with incomplete messages ("do the thing", "help me with formatting"). On Invoke should define the minimum viable context needed before workflow entry, and how to request it.

## Example

**Bad — missing invoke contract:**

```markdown
## Workflow
1. Understand the user's API design requirements
2. Identify resources and relationships
3. Generate OpenAPI spec
4. Review with user
5. Iterate on feedback
```

First invocation: model asks 5 questions about requirements. Second invocation: model jumps straight to generating a spec. Third invocation: model asks "what did we decide last time?" The entry behavior is random.

**Good — explicit invoke contract:**

```markdown
## On Invoke
Extract from the invocation message:
- Target API purpose (what does it do?)
- Known resources (if any mentioned)
- Target spec format (OpenAPI 3.x assumed if not stated)

If the purpose is unclear, ask: "What will this API serve?"
If resources are not mentioned, proceed — they'll be identified in step 2.

Do not enter the workflow until the API purpose is confirmed.

## Workflow
1. Confirm resources and relationships (using purpose as anchor)
2. Generate OpenAPI spec
3. Present for review
4. Iterate on feedback
```

Every invocation starts the same way: extract purpose, confirm it, then enter workflow. Consistent, predictable, reliable.
