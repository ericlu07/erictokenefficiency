#!/usr/bin/env python3
"""
lint_prompt.py — Detects common bloat patterns in prompts and CLAUDE.md files.

Usage:
    python lint_prompt.py path/to/prompt.md
    python lint_prompt.py path/to/CLAUDE.md
    python lint_prompt.py path/to/file1.md path/to/file2.md ...

Exit codes:
    0 = clean
    1 = warnings (bloat detected)
    2 = errors (must fix)

Use as pre-commit hook:
    # .git/hooks/pre-commit
    python tools/lint_prompt.py CLAUDE.md prompts/**/*.md || exit 1
"""

import re
import sys
from pathlib import Path

# Approximate token count: 1 token ≈ 0.75 words ≈ 4 chars
WORDS_PER_TOKEN = 0.75
CLAUDE_MD_TOKEN_BUDGET = 800
PROMPT_TOKEN_BUDGET = 2000

POLITE_PADDING = [
    r"\bplease\b",
    r"\bkindly\b",
    r"\bmake sure to\b",
    r"\bbe sure to\b",
    r"\balways remember to\b",
    r"\bit is important (?:to|that)\b",
    r"\byou should always\b",
    r"\bplease ensure\b",
    r"\bI hope this helps\b",
    r"\bgreat question\b",
    r"\bI'll go ahead and\b",
    r"\blet me know if\b",
    r"\bfeel free to\b",
]

CLAIMS_BUT_NO_RATIONALE = [
    r"\bnever\b(?!.*because)",
    r"\balways\b(?!.*because)",
]

THINK_STEP_BY_STEP = re.compile(r"think step by step|let'?s think step by step", re.I)
EXPERT_PERSONA = re.compile(r"you are (?:an? )?(?:expert|world[- ]class|senior|professional)", re.I)


def estimate_tokens(text: str) -> int:
    return int(len(text.split()) / WORDS_PER_TOKEN)


def strip_examples(text: str) -> str:
    """Remove fenced code blocks, blockquotes, table rows, and lines marked as anti-examples.

    Lets the linter run on actual prose rules without false-positives from quoted bad examples.
    """
    out_lines = []
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if stripped.startswith(">"):  # blockquote
            continue
        if stripped.startswith("|"):  # markdown table row
            continue
        # Anti-example markers
        low = stripped.lower()
        if any(m in low for m in ["bad:", "anti-pattern", "don't write", "anti-example", "instead of"]):
            continue
        out_lines.append(line)
    return "\n".join(out_lines)


QUOTED_RE = re.compile(r'"[^"]*"|\'[^\']*\'')


def strip_quotes(text: str) -> str:
    """Remove quoted spans. Quoted content = discussion of patterns, not usage."""
    return QUOTED_RE.sub("", text)


def lint_file(path: Path) -> tuple[int, list[str]]:
    """Returns (severity, messages). Severity: 0=clean, 1=warn, 2=error."""
    raw = path.read_text()
    # Two-pass strip: first remove example structure, then remove quoted spans
    text = strip_quotes(strip_examples(raw))
    msgs = []
    severity = 0

    # 1. Token budget (use raw text — examples count toward budget too)
    tokens = estimate_tokens(raw)
    is_claude_md = path.name == "CLAUDE.md"
    budget = CLAUDE_MD_TOKEN_BUDGET if is_claude_md else PROMPT_TOKEN_BUDGET
    if tokens > budget:
        severity = max(severity, 2)
        msgs.append(f"  ERROR  ~{tokens} tokens exceeds budget ({budget}) — caveman it")
    elif tokens > budget * 0.8:
        severity = max(severity, 1)
        msgs.append(f"  WARN   ~{tokens} tokens approaches budget ({budget})")

    # 2. Polite padding
    for pattern in POLITE_PADDING:
        matches = re.findall(pattern, text, re.I)
        if matches:
            severity = max(severity, 1)
            msgs.append(f"  WARN   polite padding {len(matches)}x: '{pattern}' — use imperative")

    # 3. Think step by step (always bad on reasoning models)
    if THINK_STEP_BY_STEP.search(text):
        severity = max(severity, 2)
        msgs.append("  ERROR  'think step by step' found — harmful on reasoning models, raise thinking.effort instead")

    # 4. Expert persona (hurts factual tasks)
    if EXPERT_PERSONA.search(text):
        severity = max(severity, 1)
        msgs.append("  WARN   expert persona found — drops MMLU 3-5 pts, only use for tone/voice tasks")

    # 5. Repeated instructions (same line >1x)
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    seen = {}
    for l in lines:
        seen[l] = seen.get(l, 0) + 1
    for l, count in seen.items():
        if count > 1 and len(l) > 30:
            severity = max(severity, 1)
            msgs.append(f"  WARN   line repeated {count}x: '{l[:60]}...'")

    # 6. Few-shot bloat (>5 example blocks)
    example_blocks = len(re.findall(r"<example[^>]*>", text))
    if example_blocks > 5:
        severity = max(severity, 1)
        msgs.append(f"  WARN   {example_blocks} <example> blocks — cap at 3-5 (Brown curve plateaus)")

    # 7. Claims without WHY
    claim_count = 0
    for pattern in CLAIMS_BUT_NO_RATIONALE:
        claim_count += len(re.findall(pattern, text, re.I))
    if claim_count > 5:
        severity = max(severity, 1)
        msgs.append(f"  WARN   {claim_count} 'never/always' without 'because' — Claude generalizes from rationale")

    # 8. Stacked negatives (>3 "don't" in close proximity)
    dont_count = len(re.findall(r"\bdon'?t\b", text, re.I))
    if dont_count > 5:
        severity = max(severity, 1)
        msgs.append(f"  WARN   {dont_count} negations — convert to positives, stacked don'ts hurt accuracy")

    return severity, msgs


def main():
    if len(sys.argv) < 2:
        print("usage: lint_prompt.py <file> [file ...]")
        sys.exit(2)

    overall = 0
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"{path}: NOT FOUND")
            overall = max(overall, 2)
            continue
        severity, msgs = lint_file(path)
        status = ["CLEAN", "WARN ", "ERROR"][severity]
        print(f"[{status}] {path}")
        for m in msgs:
            print(m)
        overall = max(overall, severity)

    sys.exit(overall)


if __name__ == "__main__":
    main()
