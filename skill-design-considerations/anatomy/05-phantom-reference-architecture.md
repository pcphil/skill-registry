# Phantom Reference Architecture

## What it is

A skill's SKILL.md body is written *as if* reference files exist and will be loaded, but the references are absent, incomplete, or structurally mismatched with the loading instructions.

The SKILL.md says "Load `references/platform-formats.md` for detailed format specifications" but one of the following is true:
- The file does not exist
- The file exists but contains different content than what the SKILL.md expects
- The file exists and matches, but the loading instruction points to the wrong path
- The file was renamed or restructured since the SKILL.md was last updated

When the model encounters a reference instruction and the reference is missing or mismatched, it will:
1. **Halt** — "I cannot find the referenced file" (best case, but disrupts flow)
2. **Fabricate** — Generate the expected content from training data (worst case, produces plausible but wrong output)
3. **Skip** — Proceed without the information, producing output that lacks critical constraints or context

This is a build-time defect: the blueprint calls for a component that was never built or was built to a different spec.

## Why it happens

Reference architecture is designed top-down but implemented bottom-up. The SKILL.md is written first, with placeholders for reference files that will be "filled in later." Later never comes, or comes with different content than originally planned.

Common lifecycle failures:
- **Draft amnesia:** Author writes SKILL.md with five reference load points, creates three files, ships, forgets about the other two
- **Refactor drift:** Reference files are renamed or reorganized but SKILL.md loading instructions aren't updated
- **Content migration:** Content is moved from one reference to another, breaking the SKILL.md's expectation of what each file contains
- **Copy-paste inheritance:** Skill is forked from another skill; reference load instructions are copied but reference files aren't

## Analogy

An architect's blueprint specifies "load-bearing wall, see structural detail sheet S-401." The contractor opens the plan set — sheet S-401 doesn't exist, or it shows plumbing details instead of structural specs. The wall still gets built, but without the structural specification, the contractor guesses. The building passes visual inspection. It fails under load.

## Symptoms

- Model says "I'll now load the reference file" and then produces content that doesn't match what the reference actually contains (or would contain)
- Skill works perfectly in some conversations and fails in others, depending on whether the model encounters the broken reference path
- Model fabricates content that sounds authoritative but contains subtle inaccuracies — the hallmark of training-data fill-in for a missing reference
- Error messages about files not found during skill execution
- Author adds a reference file and behavior suddenly changes in unexpected ways — the model was previously fabricating, and now the real content conflicts with its fabrication

## Fix

**Pre-publish verification.** Before shipping, verify every reference path in SKILL.md:
- File exists at the stated path
- File contains the content the SKILL.md expects (not just "a file exists there")
- Path is relative and correct from the skill's root directory

**Name expectations at the load point.** Don't just reference a path — state what the file must contain:

```markdown
Load `references/platform-formats.md` (contains: format table for Claude Code,
Cursor, Windsurf, Copilot; required fields per platform; size limits).
```

This serves as documentation, a verification signal, and a fallback prompt if the file is missing.

**Add fallback instructions for every reference load:**

```markdown
Load `references/criteria.md` for the evaluation rubric.
If unavailable: use these minimum criteria: [list 3-5 essentials inline].
```

The fallback prevents hallucination by giving the model a degraded-but-correct path when the reference is missing.

**Maintain a reference manifest.** In SKILL.md or as a separate file, keep a table mapping each reference to its purpose and the workflow step that loads it:

```markdown
## Reference Map
| File | Contains | Loaded by |
|------|----------|-----------|
| references/formats.md | Platform format specs | Step 2: Detect platform |
| references/examples.md | Before/after skill examples | Step 4: Review |
| references/checklist.md | Quality criteria | Step 5: Verify |
```

**Treat reference paths as dependencies.** When renaming or restructuring reference files, search SKILL.md for every path that points to the old location. This is the same discipline as updating import paths after refactoring code.

**Keep references one level deep.** Every reference file should link directly from SKILL.md — not from another reference. When a reference points to a further reference, the model tends to preview the nested file partially (e.g. reading only the first lines) rather than loading it whole, so it acts on incomplete content. A phantom reference fails loudly; a deeply-nested one fails quietly with half the information.

```markdown
# Bad — nested (SKILL.md → advanced.md → details.md)
SKILL.md:   See references/advanced.md
advanced.md: See references/details.md   ← model may only preview this

# Good — flat (every file linked from SKILL.md)
SKILL.md:   Advanced: references/advanced.md
            API:      references/reference.md
            Examples: references/examples.md
```

## Example

**Bad — phantom references:**

```markdown
## Workflow
1. Assess user's current skill draft
2. Load `references/quality-criteria.md` for evaluation rubric
3. Load `references/platform-guide.md` for format validation
4. Score draft against criteria
5. Present feedback

## References
- `references/quality-criteria.md` — evaluation rubric
- `references/platform-guide.md` — platform format specs
- `references/examples.md` — annotated examples
```

Reality: `quality-criteria.md` exists but was last updated three versions ago and is missing two new criteria. `platform-guide.md` was renamed to `formats.md` during a refactor. `examples.md` is referenced in the manifest but never loaded in the workflow. The model encounters step 2, finds stale criteria, and step 3 fails or fabricates platform specs.

**Good — verified references with fallbacks:**

```markdown
## Workflow
1. Assess user's current skill draft
2. Load `references/quality-criteria.md` for evaluation rubric
   (Expected: 9-item checklist covering purpose, triggers, workflow, constraints, size)
   If unavailable: evaluate against — clear purpose, defined triggers, concrete workflow steps, positive constraints, under size limit
3. Load `references/formats.md` for platform format validation
   (Expected: format table for 6 platforms with required fields and size limits)
   If unavailable: validate against Claude Code format (YAML frontmatter, name + description required)
4. Score draft against loaded criteria
5. Present feedback as Strengths / Issues / Suggestions

## Reference Map
| File | Contains | Loaded at | Last verified |
|------|----------|-----------|---------------|
| references/quality-criteria.md | 9-item evaluation rubric | Step 2 | 2025-01-15 |
| references/formats.md | Platform format table (6 platforms) | Step 3 | 2025-01-15 |
```

Every reference has: expected content, a fallback, and a verification date. No phantoms.
