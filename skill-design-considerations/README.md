# Skill Design Considerations

A field guide to the failure modes that break agent skills — and how to avoid them.

Skills fail in predictable ways. Understanding why helps you write skills that hold up in real use, not just in demos. These considerations are organized into four disciplines drawn from cognitive psychology, systems design, and engineering.

---

## Attention

How models allocate focus. Critical instructions get ignored not because they're wrong, but because of where they land in context.

| File | Problem |
|------|---------|
| [Lost in the Middle](attention/01-lost-in-the-middle.md) | Rules buried mid-file get less attention than rules at the edges |
| [Over-Specification](attention/04-over-specification.md) | Too many rules → model satisfies few reliably |
| [Primacy / Recency Bias](attention/07-primacy-recency-bias.md) | First and last items in a list stick; middle items are forgotten |
| [Context Bloat](attention/08-context-bloat.md) | Loading too much at once crowds out the instructions that matter |

---

## Grounding

Keeping the model tethered to skill instructions as conversations evolve and pressure mounts.

| File | Problem |
|------|---------|
| [Negation Failure](grounding/02-negation-failure.md) | "Don't do X" is unreliable — positive framing works; negation doesn't |
| [State Leakage](grounding/05-state-leakage.md) | Skill keeps influencing behavior after its task ends |
| [Instruction Conflict](grounding/06-instruction-conflict.md) | Skill instructions clash with system prompt, CLAUDE.md, or user messages |
| [Conversational Drift](grounding/13-conversational-drift.md) | Recent conversation gradually overrides skill instructions |

---

## Robustness

Designing for the real world — where inputs are incomplete, platforms vary, and things go wrong.

| File | Problem |
|------|---------|
| [Trigger Pollution](robustness/03-trigger-pollution.md) | Vague description causes skill to fire for unrelated requests |
| [Happy-Path-Only Design](robustness/09-happy-path-only.md) | Skill only defines what to do when everything goes right |
| [Platform Capability Assumption](robustness/10-platform-capability-assumption.md) | Skill assumes tools or features not available on all platforms |

---

## Composition

How skills behave as part of a larger system — with other skills, platforms, and growing scope.

| File | Problem |
|------|---------|
| [Skill Composition Blindness](composition/11-skill-composition-blindness.md) | Skill assumes it's the only active skill; breaks when others are loaded |
| [Scope Creep](composition/12-scope-creep.md) | Skill grows beyond its original purpose and loses focus |

---

## How to Use This

Read these before authoring a new skill, or diagnose a skill that isn't behaving as expected.

Each file follows the same structure: **what it is → why it happens → analogy → symptoms → fix → example**.

Start with the discipline most relevant to your problem, then read the specific failure mode.
