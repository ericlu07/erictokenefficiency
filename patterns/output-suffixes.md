# Output Length Suffixes

The five suffixes that cut response 50%+ instantly. Pair with a `max_tokens` cap as a hard backstop.

`max_tokens` does NOT count against rate limits — use it freely as a safety net.

---

## The five

### 1. One-liner
> "Answer in one sentence."

Use for: lookups, simple Q&A, fact retrieval, classification.

### 2. Code only
> "Just the code, no commentary."

Use for: snippet generation, function bodies, config files.

### 3. Diff only
> "Give me the diff only."

Use for: edits to existing code, refactors, fixes.

### 4. Bullets max
> "Three bullets max."

Use for: summaries, comparisons, options.

### 5. Schema only
> "Output: <schema>. No prose."

Use for: structured extraction, data transformation, anything machine-consumed downstream.

---

## Combined examples

```
Review src/auth.py for security issues. Three bullets max, file:line format.
max_tokens: 200
```

```
Fix the failing test in test_user.py. Just the diff. No explanation.
max_tokens: 400
```

```
Extract the email and phone from this text. Output: {"email": "...", "phone": "..."}. No prose.
max_tokens: 80
```

---

## For exact-length needs

CAPEL countdown-suffix paper hits >95% exact-match while keeping ROUGE-L within ±0.02:

> "Write exactly 50 words about X. Count down each word: [50] [49] [48]..."

Useful for tweet drafting, headline generation, ad copy.

---

## Why this works

Output costs 5x input on Anthropic. A response that drops from 800 -> 200 tokens saves more money than caching 5K tokens of input. Output suffixes are the highest single-action ROI lever.

The model is biased toward verbose by RLHF. You have to actively constrain it.

---

## Anti-patterns

- "Be concise" — vague, ignored
- "Keep it short" — vague, ignored
- "Brief response" — vague, ignored
- "Don't ramble" — negation without target

Always specify exact length OR exact format. Vague constraints fail.
