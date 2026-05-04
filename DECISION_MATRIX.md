# Decision Matrix — Task -> Model + Technique Stack

Pick the row. Apply the stack. Stop optimizing.

---

## By task type

| Task | Model | Stack |
|---|---|---|
| **Simple lookup, classify, format** | Haiku 4.5 | Zero-shot · "answer in one sentence" · thinking OFF · cached system |
| **Routine code edit/refactor** | Sonnet 4.6 | "Just the diff" · max_tokens 600 · cached repo context · no CoT |
| **Multi-step bug fix** | Sonnet 4.6 | Plan first (3 lines) · then edit · run tests · `<budget>1500</budget>` |
| **Novel architecture decision** | Opus 4.7 (thinking ON, medium) | Cached XML system · 2-3 few-shot · structured output schema |
| **Multi-source research synthesis** | Opus 4.7 (thinking ON, medium) | Cached system · structured briefing in · cite-inline · `<budget>800</budget>` |
| **Creative drafting (copy, posts)** | Sonnet 4.6 | Cached persona <300 tok · 2 few-shot · "3 variants, 1 paragraph each" |
| **Long-form writing** | Sonnet 4.6 | Outline (Haiku, 200 tok) -> draft (Sonnet, anchored summary) · cached style guide |
| **Agent orchestration / dispatch** | Haiku 4.5 | Briefing schema · route only · no thinking · TOON for state |
| **Format conversion (CSV<->JSON, XML<->TOON)** | Haiku 4.5 | Zero-shot · explicit schema · max_tokens tight |
| **Log filtering / regex extraction** | Haiku 4.5 | Slice with grep first · then ask · "rows only" |
| **Security audit / threat model** | Opus 4.7 (thinking ON, high) | Full context · NO terse-mode · explicit checklist · cite findings |
| **Documentation from code** | Sonnet 4.6 | "summary first" · `<budget>600</budget>` · skip getters/setters |

---

## By session phase

| Phase | Action |
|---|---|
| Session start | Cached system prompt loaded · CLAUDE.md re-read · MCP whitelist applied |
| Topic switch | `/clear` |
| Topic continues, context heavy | `/compact preserve code, decisions, paths only` |
| About to call >2 tools sequentially | Use Programmatic Tool Calling instead |
| Reading file you've seen | DON'T — cite from context |
| Need a snippet from a big file | `Read offset/limit` |
| Need to check existence/find pattern | Grep, never Read |
| Output exceeds 500 tokens routinely | Add length suffix |
| Turn count > 10 in one session | Plan a `/clear` checkpoint at next boundary |
| Approaching 80% context | `/compact` now, don't wait for autocompact |

---

## By cost-tier triggers

| Daily spend | Action |
|---|---|
| <$5/day | Quick Wins only (CLAUDE.md, /clear, MCP prune, output suffixes) |
| $5-20/day | + cache_control breakpoints + extended thinking gating + Batch API for loops |
| $20-50/day | + Langfuse measurement + per-agent TPQU + structured briefings + Haiku orchestrator |
| >$50/day | + LLMLingua compression + DSPy auto-optimization + dedicated SupervisorAgent |
| Surprise spike | Check: runaway subagent loop · MCP server added · CLAUDE.md grew · cache miss after TTL change |

---

## By output length need

| Need | Spec |
|---|---|
| One-liner | "Answer in one sentence." + max_tokens 50 |
| Short answer | "≤3 sentences" + max_tokens 150 |
| Bullet list | "N bullets max, ≤15 words each" + max_tokens (N*40) |
| Code only | "Just the code, no commentary." + max_tokens 800 |
| Diff only | "Diff only. No prose." + max_tokens 600 |
| Structured | "Output: <json schema>. No prose." + max_tokens (schema_size * 1.5) |
| Long-form | No cap, but anchored summary + outline-first |

---

## By data format

| Data shape | Use |
|---|---|
| Tabular, repeated schema (rows of records) | TOON |
| Hierarchical/nested, single object | JSON |
| Prompt structure (instructions, examples, thinking) | XML |
| Pure prose context | Markdown |
| Code | Code blocks (triple backtick + language) |
| Configuration | YAML or TOON |

TOON beats JSON by 30-60% on uniform records. JSON beats XML by ~14% for structured data. XML wins for prompt scaffolding because Claude was trained on it.
