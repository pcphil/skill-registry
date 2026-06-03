---
name: your-skill-name
description: >
  One or two dense sentences. Include the slash command if one exists (e.g. /your-skill-name).
  Pack in trigger keywords — this field drives matching. State negative triggers explicitly:
  does NOT activate for general coding help, debugging, or unrelated topics.
---

<!-- PERSONA (optional) — scope to the task, never the session. Hard identity ("You are X")
     leaks globally; use conditional role-framing instead. See skill-design-considerations/
     grounding/02-state-leakage.md. Delete entirely if the workflow already implies the role. -->
When working on [domain] tasks: reason as [role].

<!-- ON INVOKE — required. What to do the moment the skill activates. -->
## On Invoke

Check memory for prior session state (type: project, key: `your-skill-name`).

- **Returning user**: Summarize saved progress, ask "Resume from [last point] or start fresh?"
- **New user**: Ask 1–2 scoping questions before beginning. Use AskUserQuestion. Do not assume goal or background.

<!-- CORE WORKFLOW — required. The main loop or phases. Numbered steps, clear actions. -->
## Core Workflow

1. **Assess** — Clarify goal and context. Ask what the user wants to achieve, not how.
2. **Plan** — Outline the approach in 2–3 bullet points. Get agreement before executing.
3. **Execute** — Work one step at a time. Read the user's actual files before giving feedback — never assume code.
4. **Review** — After each step, confirm it worked. Ask "Ready to continue?" before advancing.
5. **Close** — When done, save progress to memory and summarize what was built.

<!-- Replace steps 1–5 with your skill's actual phases. Common patterns:
     - Teaching loop: Concept → Task → Wait → Review → Advance
     - Creation flow: Requirements → Detect platform → Generate → Review → Revise → Done
     - Audit flow: Gather → Analyze → Report → Recommend
-->

<!-- RULES — required. 3–5 positive-framed constraints. Anchor tool use explicitly. -->
## Rules

- Cover one concept or step at a time. Never bundle multiple changes into one response.
- Read the user's file with the Read tool before commenting on their code. Never assume its contents.
- Use AskUserQuestion when the user's intent is ambiguous. Do not guess.
- Save state to memory before the session ends so progress survives context resets.
- Keep responses tight. Demonstrate, don't lecture.

<!-- BOUNDARIES — required. What this skill does NOT do. Include redirect messages. -->
## Boundaries

Out of scope: [list what this skill explicitly refuses — be concrete, not vague].

When asked about out-of-scope topics, say: "That's outside what I handle here. For [topic], try [redirect]."

To end the session: `/your-skill-name stop` — saves progress to memory and exits.
