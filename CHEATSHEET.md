# Token Efficiency Cheat Sheet

One-page reference. Print and pin.

```
COST PHYSICS
  output  = 5x input            cache  = 0.10x input (90% off)
  ext.thk = bills as output     Opus 4.7 tokenizer = +35%
  MCP srv = ~25K tok each       CLAUDE.md = paid every turn

ATTACK ORDER
  1. cap output           (5x leverage)
  2. cache input          (90% off prefix)
  3. compress context     (LLMLingua, anchored summary)

OUTPUT SUFFIXES (pick one, cuts ~50%)
  "Just the diff. No commentary."
  "Three bullets max."
  "Answer in one sentence."
  "Output: <schema>. No prose."
  "Just the code, no explanation."

QUICK WINS TODAY
  /clear at every topic switch                  free
  caveman CLAUDE.md to <800 tokens              4-15K/session
  disable unused MCP servers                    50-100K baseline
  add output suffix to every prompt             50% output

CACHING RULES
  - cache_control on LAST byte-identical block
  - order: system -> tools -> few-shot -> RAG -> user
  - TTL = 5 min (refresh inside window or use 1h beta)
  - workspace-isolated since Feb 5 2026

REASONING
  NEVER write "think step by step" on reasoning models
  extended thinking OFF by default, ON per-task
  never combine extended thinking + CoT (pay twice)

MODEL ROUTING
  Haiku 4.5  $1/$5     simple/mechanical/orchestration
  Sonnet 4.6 $3/$15    execution/scaffolding/refactor (default)
  Opus 4.7   $5/$25    novel architecture/deep synthesis ONLY

DATA FORMATS
  XML for prompt structure (Claude trained on it)
  JSON or TOON for data payload (TOON 50% lighter)

AGENT HANDOFFS (5-field schema)
  { objective, constraints[], prior_decisions[],
    evidence_pointers[], expected_output }
  Pass paths/URLs/memory tags. Never full documents.

AVOID
  cat whole file              -> head/grep/jq first
  all MCP enabled             -> whitelist per project
  prose CLAUDE.md             -> bullets, <800 tok
  autocompact fires           -> manual /compact at boundaries
  "please think step by step" -> delete, raise effort
  ext thinking always-on      -> per-task only
  full convo to next agent    -> 5-field briefing JSON
  polite padding              -> imperative only
  5+ few-shot                 -> cap at 2-3
  cache mid-dynamic-block     -> move after last identical

MEASURE
  /cost at end of every session
  output tokens <40% of total = skill working
  output tokens >60% = tighten cuts
  Langfuse + TPQU (tokens per quality unit) for production
```

See [MASTER_GUIDE.md](MASTER_GUIDE.md) for the full playbook.
