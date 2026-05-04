# erictokenefficiency

The complete playbook for cutting Claude Code token waste **by 85-92%** without degrading quality.

Built from the 6-phase token efficiency research (May 2026): empirical benchmarks, real-world cost reports ($720/mo -> $72/mo, Spotify $18K/day -> $4.5K/day), and validated against Anthropic's official docs.

---

## Start here

| File | What it gives you |
|---|---|
| **[CHEATSHEET.md](CHEATSHEET.md)** | One-page reference — print and pin |
| **[QUICKWINS.md](QUICKWINS.md)** | 7 changes to ship today (<30 min each) |
| **[MASTER_GUIDE.md](MASTER_GUIDE.md)** | The full playbook — top 20 techniques ranked by ROI |
| **[DECISION_MATRIX.md](DECISION_MATRIX.md)** | Task -> model + technique stack |
| **[AVOID_LIST.md](AVOID_LIST.md)** | The 10 mistakes + exact fix for each |

---

## Reusable assets

### Templates
- **[templates/CLAUDE.md.template](templates/CLAUDE.md.template)** — caveman CLAUDE.md, <800 tokens
- **[templates/agent-subagent.template.md](templates/agent-subagent.template.md)** — drop-in `.claude/agents/` definition
- **[templates/structured-briefing.json](templates/structured-briefing.json)** — 5-field handoff schema (replaces full-context forwarding)

### Patterns
- **[patterns/cache-control-example.py](patterns/cache-control-example.py)** — Anthropic SDK `cache_control` done right (90% off)
- **[patterns/toon-vs-json.md](patterns/toon-vs-json.md)** — when to use TOON, JSON, XML, Markdown (TOON cuts 60% on tabular)
- **[patterns/output-suffixes.md](patterns/output-suffixes.md)** — the 5 length suffixes that cut response 50%+

### Tools
- **[tools/lint_prompt.py](tools/lint_prompt.py)** — detects bloat in prompts/CLAUDE.md (use as pre-commit hook)
- **[tools/count_tokens.py](tools/count_tokens.py)** — token counter + cost estimator across models

### Skill
- **[SKILL.md](SKILL.md)** — the original token-efficient response-style skill (auto-loaded by Claude Code)

---

## Install

### macOS / Linux

```bash
git clone https://github.com/ericlu07/erictokenefficiency.git ~/erictokenefficiency
mkdir -p ~/.claude/skills/token-efficient
ln -sf ~/erictokenefficiency/SKILL.md ~/.claude/skills/token-efficient/SKILL.md
```

### Windows (PowerShell as Admin)

```powershell
git clone https://github.com/ericlu07/erictokenefficiency.git $HOME\erictokenefficiency
New-Item -ItemType Directory -Force "$HOME\.claude\skills\token-efficient" | Out-Null
New-Item -ItemType SymbolicLink -Path "$HOME\.claude\skills\token-efficient\SKILL.md" -Target "$HOME\erictokenefficiency\SKILL.md"
```

### Verify

In Claude Code, run `/skills` — `token-efficient` should appear.

### Set up the linter (optional)

```bash
pip install tiktoken
echo "python ~/erictokenefficiency/tools/lint_prompt.py CLAUDE.md" > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

---

## Use

The skill auto-activates based on its description. To bypass for a turn, use words like "explain", "walk me through", "detailed", "verbose" — the override at the top of `SKILL.md` yields immediately.

For repo-wide token efficiency:
1. Today: read [QUICKWINS.md](QUICKWINS.md), do all 7
2. This week: read [MASTER_GUIDE.md](MASTER_GUIDE.md), pick top 3 from "ranked by ROI"
3. Ongoing: keep [CHEATSHEET.md](CHEATSHEET.md) on a second monitor

---

## Measure

End every session with `/cost`.

| Output % of total | Status |
|---|---|
| <40% | Skill working |
| 40-60% | Could be tighter |
| >60% | Skill not firing or rules slipping |

For production agents, wire up Langfuse and track **TPQU** (Tokens Per Quality Unit) by `task_type`.

---

## Benchmarking

See `bench/` for validation prompts. Methodology: same prompt, isolated worktree, ≥2 reps, measure tokens to green test.

---

## What's new in v2.0

The original v1.0 was a single SKILL.md focused on response verbosity. v2.0 expands to the full token efficiency stack:
- Caching (90% off cached input)
- Subagent isolation (60-70% per call)
- Structured briefings (replaces quadratic context forwarding)
- Multi-model routing (97.7% accuracy at 61% cost)
- Extended thinking gating (10x trap when misapplied)
- TOON > JSON > XML for data
- MCP server pruning (~25K tokens saved per disabled server)
- The `/clear` discipline + manual `/compact` strategy
- Linter + token counter for prompts

See [CHANGELOG.md](CHANGELOG.md) for the full list.

---

## Sources

Nova's 6-phase research (2026-05-04). Validated against:
- [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Claude Code costs docs](https://code.claude.com/docs/en/costs)
- [Anthropic — effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Wharton GAIL 2025 (CoT on reasoning models)
- TOON benchmarks ([toon-format/toon](https://github.com/toon-format/toon))
- LLMLingua-2 ([arXiv 2403.12968](https://arxiv.org/html/2403.12968v2))
- Real-world reports: BuildToLaunch, MindStudio, Mehul Gupta, labeveryday, Steve Kinney
- Empirical benchmarks: adam-s/testing-claude-agent

---

## License

MIT
