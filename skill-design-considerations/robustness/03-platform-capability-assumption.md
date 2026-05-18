# Platform Capability Assumption

## What it is

Platform capability assumption occurs when a skill is written to rely on features that aren't guaranteed to exist on the target platform. The skill silently breaks — or produces degraded output — whenever it's used on a platform that doesn't support the assumed capability. Common assumptions that fail across platforms:

- **Persistent memory** — Claude Code has a memory system; most other agents do not
- **Specific tool names** — `Read`, `Grep`, `Glob` are Claude Code tools; OpenCode and Cursor have different tool sets
- **File system access** — some platforms restrict or sandbox file operations
- **Slash commands** — Claude Code supports `/skill-name`; other platforms may not
- **Multi-file output** — some platforms can only write one file per interaction
- **Structured question UI** — `AskUserQuestion` with option buttons is Claude Code-specific

The failure is silent because the model doesn't throw an error — it just tries to use the assumed capability and either halts, produces garbled output, or falls back to default behavior without telling anyone.

## Why it happens

Skill authors typically write and test on one platform — usually the one they use daily. That platform's capabilities become invisible assumptions baked into the skill body. The skill is described as "portable" or "agnostic," but underneath it's hardwired to a specific runtime.

Additionally, platform documentation is often incomplete or lags behind actual capabilities. Authors assume features exist because they seem like basics, not because they've verified them.

## Analogy

Writing a recipe that calls for a convection oven — you assume everyone has one because you do. Most people have a standard oven. The recipe "works" but the timing is wrong, the texture is off, and the cook doesn't know why. The recipe should either specify convection only or include conventional-oven adjustments. "It works on my machine" is a platform capability assumption in disguise.

## Symptoms

- Skill works perfectly in Claude Code, breaks in OpenCode or Cursor with no obvious error
- Memory-dependent skill loses all state when used on a platform without persistent memory
- Skill instructs model to "use the Grep tool" — model on non-Claude-Code platform halts or narrates confusion
- Skill generates slash commands that don't exist on the target platform
- Structured question prompts render as plain text instead of interactive UI
- Skill author tests on one platform, users report it "doesn't work" on another — and both are right

## Fix

**Audit assumptions before publishing:**

Before finalizing a skill, list every capability it depends on and verify each is available on the target platform(s):

| Capability | Claude Code | OpenCode | Cursor | Copilot | Aider |
|------------|-------------|----------|--------|---------|-------|
| Persistent memory | Yes | Verify | No | No | No |
| File read/write tools | Yes | Yes | Limited | Limited | Yes |
| Slash commands | Yes | No | No | No | No |
| Structured question UI | Yes | No | No | No | No |

**Use intent-based language for tools:**

Instead of naming platform-specific tools, describe intent. The agent resolves the intent using whatever tools it has:

```markdown
# Bad — platform-specific
Use the Grep tool to search for existing SKILL.md files.

# Good — intent-based
Search the codebase for existing SKILL.md files.
```

**Make memory optional:**

Design skills to be stateless by default. If memory is available, use it to enhance the experience. If not, the skill still works:

```markdown
## State
If persistent memory is available: save progress after each step.
If not: summarize current state in each response so the user can resume manually if needed.
```

**Declare platform requirements explicitly:**

If a skill genuinely requires a platform-specific feature and cannot degrade gracefully, say so at the top:

```markdown
**Requires:** Claude Code with memory enabled. Not compatible with stateless agents.
```

This is better than silently failing.

**Test on the lowest-capability target:**

If a skill claims to support multiple platforms, test it on the most restricted one. If it works there, it works everywhere. If it doesn't, add fallbacks until it does or narrow the stated compatibility.

## Example

**Bad — hardwired to Claude Code:**

```markdown
## Workflow
1. Use the Read tool to load the existing SKILL.md
2. Use AskUserQuestion to confirm the target platform with structured options
3. Save progress to memory after each step
4. Use the Bash tool to run the install script
```

This breaks on every non-Claude-Code platform. The skill claims portability but delivers none.

**Good — intent-based with fallbacks:**

```markdown
## Workflow
1. Read the existing SKILL.md if one exists in the current directory
2. Ask the user which platform to target — list options: Claude Code, Cursor, OpenCode, Windsurf, Copilot, Aider
3. Track progress in the conversation; if memory is available, save state after each step
4. If an install script exists in `scripts/`, offer to run it; otherwise provide manual install instructions
```

Same workflow. Resolves to platform-appropriate tools at runtime. Degrades gracefully where features are absent.
