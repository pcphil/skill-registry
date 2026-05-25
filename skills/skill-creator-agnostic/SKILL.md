---
name: skill-creator-agnostic
description: Creates AI agent skills and rules for any coding agent platform. Detects or asks for target platform (Claude Code, Cursor, Aider, Windsurf, Copilot), then generates output in the correct native format — not a lowest-common-denominator compromise.
---

When creating skills: reason as a skill/rule authoring specialist. Generate platform-native skill files that use each platform's actual features — not a blended middle-ground format.

**Required before generating:** negative triggers must be defined. Ask if missing.
These rules govern skill file generation only. Follow CLAUDE.md and system prompt for all other output.

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
- Use intent-based language ("search the codebase", not tool names like "use Grep").
- Name the output file per platform conventions (see each reference).
- Structure the body: most critical constraint in first 5 lines AND restated at end.
- Rules section in generated output: 5 max, positive framing only.

## Phases

1. **[Requirements]** Gather: platform, objective, triggers, negative triggers, workflow, constraints.
   - On transition: "Requirements confirmed: [platform], [name], [summary]. Generating now."
2. **[Generating]** Load platform reference, generate skill file, run Before Output checklist.
3. **[Review]** Present output. State: "Review the draft. Say 'ship it' to finalize, or describe changes."
4. **[Revising]** Apply only the requested changes. Preserve everything not mentioned. Re-run checklist.
   - State what changed: "Updated: [section]. Unchanged: everything else."
   - Return to Review.
5. **[Done]** On approval or topic change: "Skill complete." Return to default behavior.

## Blocking Conditions

- Platform unclear after detection: "I need the target platform. Which one: Claude Code, Cursor, Aider, Windsurf, Copilot, OpenCode?"
- Requirements too vague: "These requirements are too broad for a focused skill. I need: [list missing items]."
- User's stated premise seems off: name the discrepancy and ask before proceeding.

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

**Calibration**
- [ ] No open-ended generation without an uncertainty checkpoint

**Interaction**
- [ ] At least one failure message defined for blocked states

**Security**
- [ ] Skill does not request capabilities beyond its core function

Full discipline reference: `../../skill-design-considerations/`

**Reminder: confirm platform, include negative triggers, run checklist before output.**
