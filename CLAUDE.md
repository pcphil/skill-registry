# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a **skill registry** — a collection of reusable agent skills authored primarily for Claude Code, with portability to Cursor, Windsurf, Copilot, Aider, and OpenCode as a first-class design goal.

There is **no build system, no tests, and no lint config**. The repo is markdown prose. Do not search for `package.json`, a test runner, or CI — there isn't one. "Correctness" of a skill is judged against the design rubric in `skill-design-considerations/` (see Validating a Skill below), not by a compiler.

## Two Content Trees

The repo has two top-level trees that depend on each other:

- **`skills/`** — the actual skills. Each is a directory with a `SKILL.md` entry point. This is the shippable product.
- **`skill-design-considerations/`** — a field guide to the failure modes that break agent skills, organized into 9 disciplines (attention, grounding, robustness, composition, anatomy, calibration, interaction, security, principles). 39 documents total. This is the **rubric that the skills in `skills/` are written against**.

The link between them is direct: the `skill-tutor` skill *teaches* this taxonomy, and every skill here is expected to hold up against it. When authoring or reviewing a skill, the design considerations are the standard — read the relevant discipline before changing skill instructions.

## Skill Structure

```
skill-name/
├── SKILL.md          # Required. YAML frontmatter (name, description) + markdown instructions.
├── references/       # Heavy docs loaded on demand, not upfront.
├── scripts/          # Deterministic executables (Python/Bash).
└── assets/           # Templates/boilerplate — never loaded into context.
```

### Hard constraints
- SKILL.md stays under 500 lines — move heavy content to `references/`.
- The `description` frontmatter field drives trigger matching and semantic search. Write it keyword-rich and specific, and state when the skill should **not** activate.
- Keep each skill directory flat (no deep nesting).

## Recurring Skill Conventions

The skills here share an authoring pattern — match it when adding or editing one:

- **On Invoke contract** — most skills open with an explicit `## On Invoke` section defining the entry sequence (e.g. check memory for prior progress → resume or assess). This prevents the model from improvising entry differently each run.
- **Memory for progress** — learning skills (`learn-*`, `skill-tutor`) persist progress to Claude Code memory (`type: project`), not to files in the repo. Learning state is never committed.
- **Mode/phase labeling** — multi-mode skills restate the active mode in every response (e.g. `[Tutor: Module X, Lesson Y]`) so state is never carried implicitly.
- **Progressive disclosure** — `SKILL.md` holds the workflow; detailed curricula/checklists live in `references/*.md` and are loaded only when that phase is reached.
- **Express intent, not mechanism** — write "search the codebase for X", not "use the Grep tool". Tool names are platform-specific and break portability.
- **Positive constraint grammar** — phrase rules as actions to take, not things to avoid ("Don't do X" is unreliable across models).

## Validating a Skill (no test runner)

Since there's nothing to run, validate by review:

1. Check `SKILL.md` against the disciplines in `skill-design-considerations/` — start with `principles/`, then the discipline matching the skill type.
2. Confirm the `description` triggers on the right requests and excludes the wrong ones (robustness/01-trigger-pollution).
3. Confirm every path referenced in `SKILL.md` actually exists in `references/`/`scripts/`/`assets/` (anatomy/05-phantom-reference-architecture).
4. The `skill-tutor` Reviewer mode encodes this checklist — use it as the canonical review flow.

## Installing Skills

```bash
# Project-scoped (only active in that project)
cp -r skills/<skill-name>/ /path/to/project/.claude/skills/<skill-name>

# Global, via the skills CLI
npx skills add ./skills/<skill-name>
```

After installing in Claude Code: run `/reload-plugins`, then `/skills` to confirm it appears.
