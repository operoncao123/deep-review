# Integrations — one skill, six agents

The skill is a plain **Agent Skills** folder (`SKILL.md` + `assets/` +
`references/`), which most current coding agents load natively. Everything here
installs from the repo root:

```bash
git clone https://github.com/operoncao123/deep-review.git
cd deep-review
./integrations/install.sh            # install everywhere detected
./integrations/install.sh codex zcode  # …or only specific tools
```

| Agent | How it loads DeepReview | Installed by script | Invoke with |
|---|---|---|---|
| **Claude Code** | native Agent Skills loader | `~/.claude/skills/deep-review/` | just ask: `深度调研 X` / `deep dive on X` |
| **OpenAI Codex CLI** | native skills support (Dec 2025+) | `~/.codex/skills/deep-review/` | just ask, or mention the skill by name |
| **ZCode** | native skills loader | `~/.zcode/skills/deep-review/` | just ask |
| **TRAE** | Anthropic-style skills; rules fallback | `~/.trae/skills/deep-review/` + snippet for `.trae/rules/project_rules.md` | just ask (rules guarantee routing) |
| **OpenCode** | slash-command file | `~/.config/opencode/command/deep-review.md` | `/deep-review <topic>` |
| **WorkBuddy** | its own Create Skills flow (`skill.yml`) | manual — see [workbuddy-skill.yml.md](workbuddy-skill.yml.md) | new task with any 深度调研 topic |
| *anything reading `~/.agents/skills`* | cross-agent standard dir | `~/.agents/skills/deep-review/` | agent-dependent |

Notes:

* The OpenCode command file points at `~/.agents/skills/deep-review/`, so run
  `./integrations/install.sh agents opencode` together (the script reminds you).
* For TRAE builds that do not auto-discover skills, paste
  [trae-rules-snippet.md](trae-rules-snippet.md) into `.trae/rules/project_rules.md`.
* The script never touches tool config beyond the paths listed above; it skips
  `demo/` and `integrations/` when copying (they are repo packaging, not skill).

Sources for the per-tool mechanisms: [Codex skills](https://simonwillison.net/2025/Dec/12/openai-skills/) ·
[OpenCode commands](https://opencode.ai/docs/commands/) ·
[TRAE rules & agents](https://docs.trae.ai/ide/rules) ·
[WorkBuddy skills](https://www.tencentcloud.com/techpedia/145692?lang=en)
