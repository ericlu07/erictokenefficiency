# Quick Wins — Ship Today

Seven changes, <30 min each. Compounds to 40-60% reduction within 24 hours.

---

## 1. `/clear` discipline (free, 5 min)

Make this muscle memory. At every unrelated topic switch:
```
/clear
```

Claude re-reads the entire conversation each turn. Message 50 costs more than message 5 because 49 prior messages get re-processed.

When the topic continues but history is heavy:
```
/compact preserve code samples, decisions, file paths only
```

---

## 2. Caveman CLAUDE.md (15-30 min)

CLAUDE.md is paid every turn, every session, every directory. Bloat = permanent baseline tax.

**Target: <800 tokens.** Bullets + imperatives only. No prose.

Bad:
```
You should always make sure to follow the existing patterns in the codebase
when adding new files. Please ensure that you check what exists before
creating new files. It is important to maintain consistency.
```

Good:
```
- Read existing patterns before adding files
- Edit > Write
- Check before creating
```

Use `templates/CLAUDE.md.template` as a starting point. Move detail to per-agent `.claude/agents/*.md` loaded on demand.

Audit current size:
```bash
wc -w ~/.claude/CLAUDE.md
# >800 words = ~1100 tokens = too big
```

---

## 3. Prune MCP servers per project (10 min)

Each MCP server = ~25K tokens of tool defs loaded every turn. 5 servers = 55K baseline before you type anything.

In project `.claude/settings.json`:
```json
{
  "enabledMcpjsonServers": ["github", "playwright"]
}
```

Whitelist only what you actively use in THIS project. Disable Gmail/Calendar/Drive/Higgsfield/Vercel for projects that don't need them.

---

## 4. Output suffix on every prompt (free, ongoing)

Append to your standard prompts:

| Use case | Suffix |
|---|---|
| Code edit | `Just the diff. No commentary.` |
| Research | `Three bullets max. Cite sources inline.` |
| Lookup | `Answer in one sentence.` |
| Extract | `Output: <schema>. No prose.` |
| Generate | `Just the code, no explanation.` |

Cuts response 50%+ on output (which costs 5x input).

---

## 5. One `cache_control` breakpoint (30 min, requires API access)

Add a single breakpoint after system + tools + few-shot, BEFORE dynamic user input:

```python
messages.create(
    system=[
        {"type": "text", "text": SYSTEM_PROMPT},
        {"type": "text", "text": TOOLS_PRIMER, "cache_control": {"type": "ephemeral"}}
    ],
    messages=[{"role": "user", "content": user_input}]
)
```

90% off the cached portion. See `patterns/cache-control-example.py` for full example.

Refresh inside 5 min OR use 1-hour beta header for hot prefixes.

---

## 6. Move loops to Batch API (20 min)

Any non-realtime work — research loops, evals, backfills — flat 50% off both directions via `/batches`. Stacks with caching = ~5% of normal cost.

Eric: candidates are `run_prompt_eng_research_loop.sh` and `run_token_research_loop.sh` if they exist.

---

## 7. Extended thinking OFF by default (5 min)

Extended thinking bills as OUTPUT (5x rate). Default ON in Claude Code is a major drain.

In settings or per-call:
```python
thinking={"type": "disabled"}
# or
thinking={"type": "enabled", "budget_tokens": 1024}  # minimal
```

Enable per-task only when novel reasoning is genuinely required.

---

## Verify it worked

End of next session, run:
```
/cost
```

Expected: output tokens <40% of total. Above 60% = wins didn't land or rules slipped.

---

## What's next

After Quick Wins land, see [MASTER_GUIDE.md](MASTER_GUIDE.md) section 7 for the multi-week roadmap (measurement layer, subagent isolation, structured briefings, LLMLingua compression).
