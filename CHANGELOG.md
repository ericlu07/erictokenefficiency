# Changelog

## v2.0 — 2026-05-04

Full playbook expansion based on Nova's 6-phase token efficiency research.

### Added
- `MASTER_GUIDE.md` — top 20 techniques ranked by ROI, full stacking math
- `CHEATSHEET.md` — one-page printable reference
- `QUICKWINS.md` — 7 actions <30 min each (40-60% reduction in 24h)
- `DECISION_MATRIX.md` — task -> model + technique stack
- `AVOID_LIST.md` — the 10 most damaging mistakes + exact fix
- `templates/CLAUDE.md.template` — caveman <800 token starter
- `templates/agent-subagent.template.md` — drop-in `.claude/agents/` definition
- `templates/structured-briefing.json` — 5-field handoff schema (replaces quadratic context forwarding)
- `patterns/cache-control-example.py` — Anthropic SDK caching done right
- `patterns/toon-vs-json.md` — when to use TOON/JSON/XML/Markdown
- `patterns/output-suffixes.md` — 5 suffixes that cut output 50%+
- `tools/lint_prompt.py` — bloat detector for prompts/CLAUDE.md (pre-commit ready)
- `tools/count_tokens.py` — token counter + cross-model cost estimator
- Updated `README.md` — full navigation of v2 assets

### Knowledge added (vs v1)
- KV-cache static prefix (90% off cached input, 5-min TTL since early 2026)
- Subagent isolation (60-70% per call savings)
- Multi-model routing (97.7% accuracy at 61% cost)
- Extended thinking gating (10x trap when misapplied — bills as output)
- Skip CoT on reasoning models (Wharton 2025: +2-3% acc, +200-400% output)
- MCP server defs ≈ 25K tokens each (disable per project)
- Opus 4.7 tokenizer +35% inflation
- Autocompact cascade costs 100-200K (manual `/compact` instead)
- TOON > JSON > XML for data payload
- Programmatic Tool Calling for >2 sequential tools (~10x cheaper)
- LLMLingua compression (2-17x)
- Batch API (50% off, stacks with caching)

### Receipts cited
- $720/mo -> $72/mo via disciplined caching
- Spotify $18K/day -> $4.5K/day
- Naive LUSKI agent board $50/day -> $5-10/day with full stack
- Realistic compounded ceiling: 85-92% reduction

## v1.0 — 2026-05-01

Initial release.
- Single SKILL.md with override-first ordering
- Three profiles: Coding, Content/Business, Conversation
- Explicit quality safeguards (clarification, tests, root cause, security, destructive-op confirmations)
- Anti-pattern table (top 10)
- Model selection table (Haiku/Sonnet 4.6/Opus 4.7)
- Measurement ritual via `/cost`
- "When NOT to apply" list
- Bench prompts in `bench/`
- Cross-platform install
