"""
Anthropic SDK cache_control example.

Rules:
- cache_control on the LAST byte-identical block
- order: system -> tools -> few-shot -> RAG -> user input
- TTL is 5 min (since early 2026); use ephemeral OR 1-hour beta header
- one whitespace drift before breakpoint = total miss
- workspace-isolated since Feb 5 2026

Savings: 90% off cached tokens. Stacks with Batch API (50% off) = ~5% of normal.
"""

import anthropic

client = anthropic.Anthropic()

# 1. Static system prompt (loaded every call, identical bytes)
SYSTEM_PROMPT = """You are a code review assistant.
- Cite files by path:line
- Flag security issues first
- Suggest minimal diffs
- Output: bullet list, ≤10 items
"""

# 2. Tool definitions (static)
TOOLS = [
    {
        "name": "read_file",
        "description": "Read a file by path with optional offset/limit",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "offset": {"type": "integer"},
                "limit": {"type": "integer"}
            },
            "required": ["path"]
        }
    }
]

# 3. Few-shot examples (static)
FEW_SHOT = """
<example>
<input>Review utils.py</input>
<output>
- utils.py:42 — SQL injection in build_query, use parameterized
- utils.py:89 — secret hardcoded, move to env
</output>
</example>
"""


def review(user_input: str):
    """Call with cache_control on the LAST static block."""
    return client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=600,
        system=[
            {"type": "text", "text": SYSTEM_PROMPT},
            {
                "type": "text",
                "text": FEW_SHOT,
                "cache_control": {"type": "ephemeral"}  # <- breakpoint here
            }
        ],
        tools=TOOLS,
        messages=[
            {"role": "user", "content": user_input}  # dynamic, NOT cached
        ]
    )


# Cost math (Sonnet 4.6 pricing $3 in / $15 out per M):
#   First call:  cache write ~1.25x input rate on the cached block, full rate on the rest
#   Subsequent: 0.10x input rate on cached block (90% off), full rate on user_input + output
#   Break-even: ~2 calls within the 5-min TTL window
#
# For high-traffic prompts: use the 1-hour beta header
#   extra_headers={"anthropic-beta": "extended-cache-ttl-2025-04-11"}
#   cache_control: {"type": "ephemeral", "ttl": "1h"}
#   Cache write becomes 2x but TTL is 12x longer.

if __name__ == "__main__":
    response = review("Review src/auth/login.py")
    print(response.usage)
    # Inspect: cache_creation_input_tokens, cache_read_input_tokens, input_tokens, output_tokens
