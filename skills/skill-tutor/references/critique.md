# Critique Mode

When reviewing a user's skill draft, evaluate against both checklists below.
Provide feedback as: **strengths** (what works), **issues** (what to fix), **suggestions** (optional improvements).

## Universal Poly-Agent Layout Checklist

- [ ] **Frontmatter complete?** — name, description, globs, tags all present
- [ ] **Description rich in keywords?** — would trigger correctly in semantic search
- [ ] **Activation boundaries defined?** — both positive AND negative triggers
- [ ] **Context variables used?** — no hardcoded paths; uses `{{REPO_ROOT}}`, `{{CURRENT_FILE}}` where needed
- [ ] **Persona/goals clear?** — one paragraph defining role and standard
- [ ] **Workflow has 3 phases?** — Validate → Execute → Verify
- [ ] **Verification step concrete?** — names specific command or check, not vague "test it"
- [ ] **Constraints section present?** — at least one critical guardrail + supporting rules
- [ ] **Reference boilerplate included?** — code examples or schemas for complex outputs
- [ ] **Under 500 lines?** — heavy content moved to references/

## Portability Check

- [ ] Core intent separable from platform syntax?
- [ ] Could this translate to a Cursor rule or Windsurf workflow?
- [ ] Are tool dependencies explicit and minimal?
- [ ] Would this work if the agent had different tool names?
- [ ] No hardcoded paths or platform-specific assumptions in core logic?

## Quality Check

- [ ] Instructions are actionable, not vague (verbs, not adjectives)
- [ ] Examples included for complex behaviors
- [ ] Consistent voice and formatting
- [ ] Negative triggers prevent false activation on adjacent topics
- [ ] Progressive disclosure used (references/ for heavy content)
