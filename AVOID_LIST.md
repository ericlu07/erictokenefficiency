# The Avoid List

Ten common mistakes. Each one with the exact fix. Ranked by silent damage.

---

## 1. `cat`-ing whole files into context

**Why it kills:** A 10K-line log read at message 3 is still in context at message 50. Tool output volume usually exceeds chat. One `cat` of a 5MB log = 1.2M tokens permanent baseline.

**Fix:**
```bash
# bad
cat /var/log/something.log

# good
head -n 100 /var/log/something.log
tail -n 50 /var/log/something.log
grep ERROR /var/log/something.log | head -n 20
jq '.errors[]' result.json | head
```

In Claude Code, use `Read` with `offset` and `limit`. Never load whole files when you only need a section.

---

## 2. All MCP servers globally enabled

**Why it kills:** Each MCP server = ~25K tokens of tool defs in your context every turn. 5 servers = 55K baseline before you type. Anthropic itself had 134K tokens of tool defs before they fixed it.

**Fix:** Per-project `.claude/settings.json`:
```json
{
  "enabledMcpjsonServers": ["github"]
}
```

Whitelist only what THIS project uses.

---

## 3. CLAUDE.md as prose

**Why it kills:** CLAUDE.md is loaded every turn, every session, every directory. A 5K-token CLAUDE.md = 5K permanent tax on every interaction. Forever.

**Fix:** Caveman style — bullets, imperatives, <800 tokens total.

Bad:
```
You should always make sure to read the existing files in the directory
before creating new ones, because it is important to maintain consistency
with the patterns that have been established by the team.
```

Good:
```
- Read existing files before creating
- Match existing patterns
```

Move detail into per-skill `SKILL.md` or `.claude/agents/*.md` loaded on demand.

---

## 4. Letting autocompact fire

**Why it kills:** Autocompact triggers near 187K tokens (sometimes 76K on Opus 1M). Each cascade = 100-200K tokens consumed by the summarization pass itself.

**Fix:**
- Manual `/compact preserve code samples, decisions, file paths only` at task boundaries
- Opt into `compact-2026-01-12` server-side compaction
- `/clear` between unrelated tasks

Never let autocompact fire uncontrolled.

---

## 5. "Please think step by step" on reasoning models

**Why it kills:** Wharton GAIL 2025 confirmed: on reasoning models (o3, o4-mini, Claude with extended thinking, Gemini reasoning), explicit CoT gains only 2-3% accuracy while adding 200-400% output tokens. Net loss.

**Fix:**
- Delete the phrase
- Raise `thinking.effort` (or `thinking.budget_tokens`) instead
- A/B test: if accuracy gain <5% and tokens +200%, drop the CoT

---

## 6. Extended thinking ON by default

**Why it kills:** Extended thinking bills as **output** tokens (5x input rate). Default thinking budgets are tens of thousands of tokens. Default ON in Claude Code. On Opus 4.7 that's $25 per million.

**Fix:**
```python
thinking={"type": "disabled"}  # default OFF
# enable per-task only:
thinking={"type": "enabled", "budget_tokens": 1024}
```

Worth it: novel coding, multi-doc synthesis, complex math.
Waste: classification, lookups, simple Q&A, formatting.

---

## 7. Re-pasting full conversation to next agent

**Why it kills:** Forwarding full convo to the next agent scales **quadratically** with handoffs. 5 hops = 25x the original cost.

**Fix:** Structured briefing schema (5 fields, ~200-500 tokens):
```json
{
  "objective": "Single sentence outcome",
  "constraints": ["constraint 1", "constraint 2"],
  "prior_decisions": ["what was decided + why"],
  "evidence_pointers": ["/path/to/file", "memory:tag", "https://url"],
  "expected_output": "Schema or shape of desired return"
}
```

Pass pointers (file paths, memory tags, URLs). Never full documents.

---

## 8. Polite framing in system prompts

**Why it kills:** "Please", "kindly", "you should always make sure to", "it is important that you" — adds tokens with zero quality benefit. ~15% of typical system prompts is compressible padding.

**Fix:** Imperative mood only.

Bad:
```
Please make sure to always check the user's intent before responding.
It is important that you ask clarifying questions if needed.
```

Good:
```
- Verify intent before responding
- Ask 1 clarifying question if ambiguous
```

---

## 9. Few-shot blocks with 5+ examples

**Why it kills:** Brown et al. (GPT-3) curve still holds in 2026. Sharp gain 0->2 examples, plateau by 4-5. **10 examples = 5x input tokens of 2 examples but NOT 5x more accurate.** Past 8, quality often degrades from noise.

**Fix:**
- Cap at 2-3 for simple/familiar tasks
- 4-5 max for hard reasoning tasks
- Put few-shots inside the cached prefix — effectively free per call

---

## 10. `cache_control` placed mid-dynamic-block

**Why it kills:** Cache reuses K/V vectors only for byte-identical prefix up to the breakpoint. If the breakpoint is anywhere AFTER dynamic content, you get zero cache hits because the dynamic content changes every call.

**Fix:** Order matters:
```
1. system prompt (static)
2. tool defs (static)
3. few-shot examples (static)
4. RAG context (semi-static)
5. cache_control breakpoint  <- put it here
6. user input (dynamic)
```

Place breakpoint on the LAST byte-identical block. One whitespace drift before that = total miss.

---

## Bonus: Three more silent killers

**11. Re-reading the same file in one session.** Claude already has it in context. Cite from prior context unless the file changed.

**12. Sequential tool calls instead of batching.** Three `Read`s in three messages = 3x context cost. Three `Read`s in one message = 1x.

**13. Tool wrappers that return everything.** A tool returning a 50K log when you need `{trace_id, latency, cost}` wastes 49K tokens. Make wrappers accept `fields=`/`max_tokens=` and slice server-side.
