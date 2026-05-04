# Master Token Efficiency Guide

The consolidated synthesis. **85-92% reduction is achievable**, most of it ships in a week.

---

## 1. The cost physics (memorize)

| Lever | Multiplier | Why |
|---|---|---|
| Output tokens | **5x input** | Autoregressive generation is sequential, memory-bandwidth-bound |
| Cached input | **0.10x input** (90% off) | KV vectors reused for byte-identical prefix |
| Extended thinking | **bills as output** (5x) | Even though it's "thinking," not visible response |
| Opus 4.7 tokenizer | **+35% inflation** | Same text, more tokens — worst on code |
| MCP server defs | **~25K tokens each** | Loaded every turn whether used or not |
| CLAUDE.md | **paid every turn** | Every session, every directory, forever |
| Autocompact cascade | **100K-200K tokens** | Fires uncontrolled near 187K context |

**Strategic order:** cut output first, cache input second, compress context third. Most teams do this in reverse.

---

## 2. Top 20 techniques, ranked by ROI

| # | Technique | Mechanism | Savings | Difficulty |
|---|---|---|---|---|
| 1 | KV-cache static prefix | `cache_control` on LAST identical block | 90% off cached input | Easy |
| 2 | `/clear` between tasks | CC re-reads full convo every turn | 50%+ on long sessions | Easy |
| 3 | Caveman CLAUDE.md (<800 tok) | Loaded every turn, every directory | 4-15K tokens/session | Easy |
| 4 | Output length suffix | Shifts mass to EOS | 50%+ output cut | Easy |
| 5 | Disable unused MCP servers | 5 servers ≈ 55K baseline | 50-100K baseline | Easy |
| 6 | Subagent isolation | Each `.claude/agents/` runs in own context | 60-70% per call | Medium |
| 7 | Skip CoT on reasoning models | Wharton 2025: +2-3% acc, +200-400% output | 200-400% output | Easy |
| 8 | Extended thinking gating | Bills as OUTPUT, max=10x low effort | 10x on simple tasks | Easy |
| 9 | Tool-output filter at source | head/grep/jq before context entry | 5-20x per call | Easy |
| 10 | Structured briefing handoffs | 200-500 tok JSON pointers vs 5-20K full forward | 90% per handoff | Medium |
| 11 | Multi-model routing | Haiku orch / Opus synth — 97.7% acc at 61% cost | 40-60% | Medium |
| 12 | Batch API | 50% off both directions | 50% | Easy |
| 13 | TOON > JSON > XML for data | TOON ~50% lighter than JSON | 40-50% on structured | Easy |
| 14 | Right-size few-shot (2-3 ex) | Brown curve plateaus at 4-5 | 60%+ vs over-shot | Easy |
| 15 | Anchored iterative summary | Persistent state vs full re-summary | 60-80% context | Medium |
| 16 | Programmatic Tool Calling | Claude writes code, only summary returns | ~10x vs sequential | Medium |
| 17 | Hard token budget + 80% alert | Pre-execution check kills runaways | Prevents disasters | Medium |
| 18 | LLMLingua compression | Strips low-perplexity tokens | 2-17x | Medium |
| 19 | Langfuse + TPQU benchmark | Tokens-per-quality-unit by task_type | Measurement enabler | Medium |
| 20 | DSPy MIPROv2 / PromptWizard | Auto-optimize prompts + few-shot | Replaces handcraft | Hard |

---

## 3. Stacking math

Cache (90% off prefix) x Subagent (60-70%) x Structured briefings (90% per handoff) x Multi-model routing (40-60%) x Extended thinking gating (10x) x Native compaction = **realistic 85-92% compounded reduction** vs naive baseline.

**Real receipts:**
- $720/mo -> $72/mo via disciplined caching
- Spotify podcast transcription: $18K/day -> $4.5K/day (75%)
- Naive LUSKI board $50/day -> $5-10/day with full stack

---

## 4. Decision matrix

| Task | Model | Stack |
|---|---|---|
| Simple (lookup, classify, format) | Haiku 4.5 | Zero-shot, "one sentence", thinking OFF, cached system |
| Research (multi-source synthesis) | Opus 4.7 (thinking ON, medium) | Cached XML system, structured briefing in, `<budget>800</budget>`, cite-inline |
| Code (edit/review/implement) | Sonnet 4.6 | "Just the diff", PTC for >2 tools, cached repo context, max_tokens 600 |
| Creative (drafting, copy) | Sonnet 4.6 | Cached persona <300 tok, 2 few-shot, "3 variants 1 paragraph each", max_tokens 400 |
| Agent orchestration | Haiku 4.5 | Briefing schema, route only, no thinking, TOON for state |
| Long-form writing | Sonnet 4.6 | Outline (Haiku, 200 tok) -> draft (Sonnet, anchored summary), cached style guide |

---

## 5. The avoid list (10 mistakes, exact fix)

| Anti-pattern | Fix |
|---|---|
| `cat`-ing whole files | `Read offset/limit`; pipe shell through `head -n 100`/`jq` |
| All MCP servers globally enabled | `enabledMcpjsonServers: []` whitelist per project |
| CLAUDE.md as prose | Bullets + imperatives, ≤800 tokens |
| Letting autocompact fire | Manual `/compact` at task boundaries |
| "Please think step by step" on reasoning models | Delete; raise `thinking.effort` instead |
| Extended thinking ON by default | Flip default OFF; per-task ON |
| Re-pasting full convo to next agent | 5-field structured briefing JSON |
| Polite framing ("please", "kindly", "you should always make sure to") | Imperative mood only — cuts ~15% of system prompt |
| Few-shot blocks with 5+ examples | Cap at 2-3, cache the block |
| `cache_control` mid-dynamic-block | Move to AFTER last byte-identical section |

---

## 6. Claude-specific rules (10)

1. Opus 4.7 tokenizer **inflates +35%** vs Sonnet/Haiku — default to Sonnet for long code
2. Cache TTL is **5 min** since early 2026 (was 60min). Refresh inside window or pay 1-hour beta header
3. `cache_control` on the **LAST byte-identical block**. One whitespace before that = total miss
4. XML for prompt **structure** (`<thinking>`, `<answer>`); JSON or TOON for data **payload**
5. Extended thinking bills as **OUTPUT** (5x). Max effort = 10x low effort
6. Never combine extended thinking + "think step by step" — pay for reasoning twice
7. Autocompact fires near 187K, costs 100-200K cascade — always prefer manual `/compact`
8. CLAUDE.md loads every turn, every session, every directory
9. MCP server tool defs ≈ 25K tokens each. Anthropic itself hit 134K pre-optimization
10. Workspace-level cache isolation since Feb 5 2026 (was org)

---

## 7. Execution order

- **Today** (<30 min each): Quick Wins 1-4 — see [QUICKWINS.md](QUICKWINS.md)
- **This week**: Quick Wins 5-7 + LUSKI rules 2-3
- **Next week**: Measurement layer (Langfuse + TPQU benchmark)
- **Month**: LUSKI rules 1, 4, 5 + ranked techniques 15-17
- **Long-term**: 18-20 (LLMLingua, DSPy)

---

## Sources

Nova's 6-phase research (2026-05-04). Validated against:
- Anthropic prompt caching docs, pricing docs, batch docs
- Wharton GAIL 2025 (CoT on reasoning models)
- TOON benchmarks (toon-format/toon)
- LLMLingua-2 paper (arXiv 2403.12968)
- Real-world cost reports: BuildToLaunch, MindStudio, Mehul Gupta, labeveryday, Steve Kinney
