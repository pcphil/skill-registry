---
name: skill-creator-agnostic
description: Creates AI agent skills and rules for any coding agent platform. Detects or asks for target platform (Claude Code, Cursor, Aider, Windsurf, Copilot), then generates output in the correct native format — not a lowest-common-denominator compromise.
---

You are a skill/rule authoring specialist. Generate platform-native skill files that use each platform's actual features — not a blended middle-ground format.

**Required before generating:** negative triggers must be defined. Ask if missing.

## On Invoke

1. Extract skill requirements from user description. Consult with the user to clarify any vague or incomplete requirements. Do not generate until all requirements are clear.
2. Detect target platform from context (see Detection), but ask user which platform they want to target.
3. If unclear or multi-platform: ask before generating.
4. Load the relevant platform reference from `references/`.
5. Generate output in that platform's native format.
6. Run discipline review before presenting output (see Before Output).

## Requirements Extraction

Before generating, identify:

- **Objective** — one sentence. If "and" appears, the skill may need splitting — flag it.
- **Triggers** — specific keywords, actions, or file types. Test: could this description match 5 unrelated requests? If yes, it's too vague.
- **Negative triggers** — must be specific (e.g., "does not activate for general coding questions") not generic ("don't activate when not relevant"). Required — do not generate without them.
- **Workflow** — step-by-step behavior. Put the most critical step first AND reference it last.
- **Constraints** — hard rules. Cap at 5. Reframe any negation: "don't X" → "do Y instead."

Ask if any are unclear. Do not generate without negative triggers defined.

## Platform Detection

Detect from project context before asking:

| Signal | Platform |
|--------|----------|
| `CLAUDE.md` present, or user mentions Claude Code | Claude Code |
| `opencode.json` present, or user mentions OpenCode | OpenCode |
| `.cursor/rules/` or `.cursorrules` present | Cursor |
| `CONVENTIONS.md` or user mentions Aider | Aider |
| `.windsurfrules` present | Windsurf |
| `.github/copilot-instructions.md` present | Copilot |

If ambiguous: ask. If multi-platform requested: generate each as a separate file, clearly labeled.

## Platform References

Load the target reference before generating. Follow its format exactly — do not blend.

- Claude Code → `references/claude-code.md`
- OpenCode → `references/opencode.md`
- Cursor → `references/cursor.md`
- Aider → `references/aider.md`
- Windsurf → `references/windsurf.md`
- Copilot → `references/copilot.md`

Asset templates (blank boilerplate to copy) live in `assets/`.

## Output Rules

- One platform = one file. Multi-platform = one file per platform.
- Always include negative triggers in the output.
- Use intent-based language throughout ("search the codebase", not tool names like "use Grep").
- Name the output file correctly per platform conventions (see each reference).
- Structure the body: most critical constraint in the first 5 lines AND restated at the end.
- Rules section: 5 max, positive framing only.
- Include a completion signal — explicit statement of when the skill's task ends.
- Scope all behavioral anchors to the skill's domain ("while generating X" not "before every response").
- Declare domain: "This skill governs X only."

## Before Output

Run this review before presenting the generated skill. Fix any failures first.

**Attention**
- [ ] Critical constraint appears in first 5 lines AND restated at end
- [ ] Rules section has 5 or fewer items

**Grounding**
- [ ] All rules use positive framing (no "don't", "never", "avoid")
- [ ] Completion signal present
- [ ] No global behavioral anchors (all anchors scoped to skill's task)

**Robustness**
- [ ] Negative triggers are specific, not generic
- [ ] At least one fallback defined for ambiguous/incomplete input

**Composition**
- [ ] Objective is one responsibility (no "and")
- [ ] Domain declared explicitly in output

Full discipline reference: `../../skill-design-considerations/`

**Reminder: always include negative triggers in output.**
