# skillanomics

A personalized skill registry for coding agents — reusable agent skills designed for Claude Code, with portability to Cursor, Windsurf, Copilot, Aider, and OpenCode.

## Skills

| Skill | Description |
|-------|-------------|
| `skill-tutor` | Teaches how to build optimal, portable agent skills for coding agents |
| `skill-creator-agnostic` | Generates skill and rule files for any coding agent platform in the correct native format |
| `learn-react` | Guided React + Vite learning assistant — teaches by doing with real project goals and code review |
| `learn-typescript` | Adaptive TypeScript tutor that teaches through explanations, examples, and hands-on exercises |

## Design Considerations

`skill-design-considerations/` is a field guide to the failure modes that break agent skills. Organized into four disciplines:

- **Attention** — how models allocate focus and why critical instructions get ignored
- **Grounding** — keeping the model tethered to skill instructions as conversations evolve
- **Robustness** — designing for incomplete inputs, platform variance, and edge cases
- **Composition** — how skills behave alongside other skills and grow over time

13 failure modes in total, each with an analogy, symptoms, fix, and before/after example.

## Installation

### Project-scoped (recommended)

Copy a skill into your project's `.claude/skills/` directory:

```bash
cp -r skills/<skill-name>/ /path/to/your-project/.claude/skills/<skill-name>
```

The skill will only be active when working in that project.

### Global

Install a skill into your global skills directory:

```bash
# Install all skills
npx skills add pcphil/skillanomics

# Install a specific skill
npx skills add pcphil/skillanomics --skill skill-tutor

# Full GitHub URL
npx skills add https://github.com/pcphil/skillanomics

# Local path
npx skills add ./skills/<skill-name>
```

The skill will be available in all projects.

### Manual

Clone the repo and copy the skill directory to your coding agent's skills folder.

### Verify

After installing, run `/reload-plugins` in Claude Code, then check `/skills` to confirm it appears.
