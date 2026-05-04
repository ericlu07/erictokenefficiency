#!/usr/bin/env python3
"""
count_tokens.py — Count tokens in a file or stdin.

Uses tiktoken (cl100k_base) as a portable approximation.
For exact Anthropic counts, use the messages.countTokens API.

Usage:
    python count_tokens.py CLAUDE.md
    cat prompt.md | python count_tokens.py -
    python count_tokens.py file1.md file2.md file3.md   # totals at end

Install:
    pip install tiktoken
"""

import sys
from pathlib import Path

try:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    HAVE_TIKTOKEN = True
except ImportError:
    HAVE_TIKTOKEN = False


def count(text: str) -> int:
    if HAVE_TIKTOKEN:
        return len(enc.encode(text))
    # Fallback: rough estimate
    return int(len(text.split()) / 0.75)


def cost_estimate(tokens: int) -> dict:
    """Estimate cost across models if this were input."""
    return {
        "haiku_in": tokens * 1 / 1_000_000,
        "sonnet_in": tokens * 3 / 1_000_000,
        "opus_in": tokens * 5 / 1_000_000,
        "sonnet_out_if_response": tokens * 15 / 1_000_000,
        "opus_out_if_response": tokens * 25 / 1_000_000,
        "cached_in": tokens * 0.30 / 1_000_000,  # cached input ~0.10x of base
    }


def main():
    if len(sys.argv) < 2:
        print("usage: count_tokens.py <file|-> [file ...]")
        sys.exit(1)

    if not HAVE_TIKTOKEN:
        print("[warn] tiktoken not installed, using word-count approximation")
        print("[warn] pip install tiktoken for accurate counts")
        print()

    total = 0
    for arg in sys.argv[1:]:
        if arg == "-":
            text = sys.stdin.read()
            label = "stdin"
        else:
            p = Path(arg)
            if not p.exists():
                print(f"{arg}: NOT FOUND")
                continue
            text = p.read_text()
            label = str(p)

        tokens = count(text)
        total += tokens
        print(f"{label:50s} {tokens:>8} tokens")

    if len(sys.argv) > 2:
        print("-" * 60)
        print(f"{'TOTAL':50s} {total:>8} tokens")

    print()
    costs = cost_estimate(total or count(text))
    print("Cost estimate (USD per call, if used as input):")
    print(f"  Haiku 4.5    ${costs['haiku_in']:.6f}")
    print(f"  Sonnet 4.6   ${costs['sonnet_in']:.6f}")
    print(f"  Opus 4.7     ${costs['opus_in']:.6f}  (note: +35% tokenizer inflation)")
    print(f"  Cached       ${costs['cached_in']:.6f}  (90% off, after first call)")
    print()
    print(f"If response = same size on Sonnet: ${costs['sonnet_out_if_response']:.6f} additional")


if __name__ == "__main__":
    main()
