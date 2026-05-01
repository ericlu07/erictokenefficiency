# erictokenefficiency

A Claude Code skill that cuts token waste without degrading work quality.

Built from empirical research across the top GitHub repos on Claude token efficiency: SpharxTeam/AgentOS (memory stratification), get-zeked/token-efficient (skill format), drona23/claude-token-efficient (terse output rules), egorfedorov/claude-context-optimizer (read-cache patterns), tamzid958/claude-architect (clarify-first), seojoonkim/agentlinter (CLAUDE.md hygiene), adam-s/testing-claude-agent (the only empirical benchmark — proved long CLAUDE.md files cost more than they save).

## What it does

- Strips preamble, closing fluff, narration, sycophancy, decorative unicode.
- Blocks redundant file reads, prefers Grep + offset/limit.
- Suggests Haiku/Sonnet/Opus by task type.
- Has explicit safeguards so terseness never cuts: clarification, tests, root-cause analysis, security review, destructive-op confirmations.
- Auto-disables on verbose requests ("explain", "walk me through", "huge plan", planning mode).

## Install

### macOS / Linux

```bash
git clone https://github.com/ericlu07/erictokenefficiency.git ~/erictokenefficiency
mkdir -p ~/.claude/skills/token-efficient
ln -sf ~/erictokenefficiency/SKILL.md ~/.claude/skills/token-efficient/SKILL.md
```

### Windows (PowerShell, run as Admin for the symlink)

```powershell
git clone https://github.com/ericlu07/erictokenefficiency.git $HOME\erictokenefficiency
New-Item -ItemType Directory -Force "$HOME\.claude\skills\token-efficient" | Out-Null
New-Item -ItemType SymbolicLink -Path "$HOME\.claude\skills\token-efficient\SKILL.md" -Target "$HOME\erictokenefficiency\SKILL.md"
```

Or just copy `SKILL.md` into `%USERPROFILE%\.claude\skills\token-efficient\` if symlinks are blocked.

### Verify

In Claude Code, run `/skills` — `token-efficient` should appear.

## How to use

Once installed, the skill auto-activates based on its description. No command needed.

To bypass for one turn, ask for "detailed", "verbose", "explain", or "walk me through" — the override at the top of `SKILL.md` yields immediately.

## Measure if it's working

End every session with `/cost`. Target: output tokens <40% of total. Above 60% means the skill isn't firing or rules need tightening.

## Updating across machines

Pull the repo on each machine:

```bash
cd ~/erictokenefficiency && git pull
```

The symlink picks up the new `SKILL.md` automatically.

## Benchmarking

See `bench/` for the validation prompts. Methodology mirrors adam-s/testing-claude-agent: same prompt, ≥2 reps, measure tokens to first green test.

## License

MIT
