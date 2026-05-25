# Feedback Loop Absence

## What it is

A skill defines how to generate output but not how to revise it. When the user says "change X," the model either regenerates everything from scratch — losing the parts that were correct — or applies the feedback inconsistently, changing X but also altering Y and Z as side effects. There's no defined mechanism for incremental revision, so each iteration is unpredictable.

Most skills treat generation as the terminal step. In practice, the first output is rarely the final one. Users iterate — and the skill should define how.

## Why it happens

Skill authors focus on the generation path because that's the skill's core value. Revision feels like an afterthought: "the user will just ask for changes and the model will apply them." But without explicit revision instructions, the model defaults to its general editing behavior, which may conflict with the skill's format, constraints, or workflow.

Specific failure modes:
- Model regenerates the entire artifact instead of making a targeted change (context-expensive, risks losing correct parts)
- Model applies the requested change but also "improves" other sections the user didn't ask about
- Model loses track of what the current version is after multiple revision rounds
- Revision breaks format constraints the original generation followed because the revision path doesn't reference those constraints

## Analogy

An architect who redraws the entire blueprint when the client asks to move one door. The foundation, walls, and plumbing were fine — but the architect's process only knows "draw from scratch," not "modify in place." Each redraw risks introducing new errors in parts that were already approved. A good architect marks up the existing blueprint: "door moves here, everything else unchanged."

## Symptoms

- User asks for one change; model regenerates the entire output
- Regenerated output changes things the user didn't ask about (regressions)
- After 2–3 revision rounds, the output has diverged significantly from the approved original
- Model loses track of the "current version" — applies feedback to an older draft
- Format or structure degrades with each revision because revision doesn't re-check constraints
- User gives up on iterating and manually edits the output themselves

## Fix

**Define a revision step in the workflow:**

Make revision an explicit, defined step — not an implicit capability:

```markdown
## Workflow
1. Gather requirements
2. Generate draft
3. Present for review
4. **Revise** — if user requests changes:
   - Apply only the requested changes
   - Preserve everything not mentioned in the feedback
   - Re-verify format constraints after applying changes
   - Present the updated version with changes highlighted
5. Repeat step 4 until approved or user exits
```

**Specify what changes vs. what's preserved:**

Give the model explicit permission to make targeted edits:

```markdown
## On Revision
When the user requests a change:
- Change only what was requested
- Do not modify sections the user didn't mention
- If the requested change conflicts with an existing constraint, flag the conflict
  rather than silently resolving it
- State what was changed: "Updated: [section]. Unchanged: everything else."
```

**Maintain version awareness:**

In multi-round revision, the model needs to know which version is current:

```markdown
## Revision Tracking
After each revision, note: "Version [N]: [what changed from previous version]"
Apply all subsequent feedback to the most recent version.
```

**Re-apply constraints after revision:**

Revision can break constraints that the original generation satisfied. Add a post-revision check:

```markdown
## Post-Revision Check
After applying changes:
- Verify output still meets format requirements
- Verify no unintended changes were introduced
- If format broke: fix the format issue, note it to the user
```

**Scope feedback to sections:**

For complex output, let the user target feedback to specific sections:

```markdown
## Feedback Format
Users can target feedback to specific sections:
- "Change the description" → modify only the description field
- "Add a trigger" → add to triggers list, don't touch anything else
- General feedback ("make it shorter") → apply proportionally, note what was trimmed
```

## Example

**Bad — no revision mechanism:**

```markdown
## Workflow
1. Gather requirements
2. Generate skill file
3. Deliver output
```

User says "change the description." Model regenerates the entire skill file. The triggers changed too. The format is slightly different. The user has to diff the two versions to figure out what else moved.

**Good — revision defined and scoped:**

```markdown
## Workflow
1. Gather requirements
2. Generate skill file — present as "Draft v1"
3. Review — ask: "Changes needed, or ready to finalize?"
4. If changes requested:
   - Apply only the stated changes
   - Preserve all other sections exactly as they were
   - Output the updated file as "Draft v[N]" with a one-line summary: "Changed: [what]. Kept: everything else."
   - Re-verify: frontmatter valid, body under 150 lines, negative triggers present
5. Repeat step 4 until user approves
6. On approval: deliver final version, exit skill

## Revision Rule
Each revision touches only what the user asked to change.
Unsolicited improvements are not applied during revision — suggest them separately if important.
```

Targeted revisions. No regressions. User knows exactly what changed.
