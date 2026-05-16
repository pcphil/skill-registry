# skill-registry

Useful skills for everyday use with Claude Code.

## Skills

| Skill | Description |
|-------|-------------|
| `skill-tutor` | Teaches how to build optimal, portable agent skills for coding agents |

## Installation

### Project-scoped (recommended)

Copy a skill into your project's `.claude/skills/` directory:

```bash
cp -r skill-tutor/ /path/to/your-project/.claude/skills/skill-tutor
```

The skill will only be active when working in that project.

### Global

Install a skill into your skills directory:

```bash
# GitHub shorthand — install all skills
npx skills add pcphil/skill-registry

# Install a specific skill from the repo
npx skills add pcphil/skill-registry --skill skill-tutor

# Full GitHub URL
npx skills add https://github.com/pcphil/skill-registry

# Direct path to a specific skill
npx skills add https://github.com/pcphil/skill-registry/tree/main/skill-tutor

# Local path
npx skills add ./skill-tutor
```

The skill will be available in all projects.

### Verify

After installing, run `/reload-plugins` in Claude Code, then check `/skills` to confirm it appears.
