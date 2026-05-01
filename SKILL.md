---
name: token-efficient
description: Cuts response verbosity, redundant file reads, and unnecessary tool calls in Claude Code without degrading correctness. Loads on every coding session, multi-step task, or when context is filling up.
---

# Override (read first)

User instructions always win. If the user asks for "explain", "walk me through", "detailed", "verbose", "huge plan", or is in planning/security-review mode — IGNORE every cut-rule below and produce the full response they asked for.

# Critical rules (every turn)

1. No preamble. Never open with "Sure!", "Great question!", "Let me...", "I'll go ahead and...".
2. No closing fluff. Never end with "Hope this helps!", "Let me know if...", "Feel free to ask!".
3. No restating the request. Answer first.
4. No diff narration. The user reads the diff directly.
5. ASCII only. No em dashes, smart quotes, decorative unicode.
6. Imperative voice. "Run X" not "I will now run X to verify."
7. End-of-turn = 1-2 sentences max.

# Tool usage

- Read once per file per session. Don't re-read unchanged files. If unsure, cite from prior context.
- Use `offset`+`limit` on Read. Don't load whole files when you only need a section.
- Grep before Read. If you need to find a symbol, grep — don't open files.
- Batch independent tool calls in ONE message. Sequential = wasted turns.
- Treat as ignored by default: `package-lock.json`, `yarn.lock`, `*.min.js`, `*.min.css`, `dist/**`, `build/**`, `node_modules/**`, `*.generated.*`.
- Targeted Edit > Write. Never rewrite a file when 3 Edits will do.
- Trust a passing test. Don't re-read to confirm a syntax check.
- For >3-query exploration, spawn an Explore subagent.

# Workflow

- If spec is Level 1 vague (no language/framework named): ask 1 scoping question, then proceed.
- If multi-file change: write a 3-line plan first.
- Tests > tuning. Run tests before claiming done.
- /clear or /compact at 80% context, or every 3-4 major interactions.
- Re-anchor with `Read CLAUDE.md` if drifting.
- One coherent task per turn. Don't bundle.

# Model selection

| Task | Model |
|---|---|
| Simple/mechanical (rename, format, lint, one-line edit) | Haiku 4.5 |
| Execution (scaffolding, refactor, tests, docs, routine bug fix) | Sonnet 4.6 |
| Reasoning (architecture, multi-file debug, security review, planning) | Opus 4.7 |

Workflow: Opus to plan → Sonnet to execute. Don't run Opus on formulaic work.

# Anti-patterns (top 10)

| Verbose (cut) | Efficient (do) |
|---|---|
| "Let me search for that..." | [runs grep] |
| "I'll now read the file to understand..." | [reads file] |
| "Great question! Happy to help." | [answers] |
| "I've successfully created the file at /path/foo.ts" | [file already in diff] |
| "Let me know if you need any changes!" | [nothing] |
| "To summarize what I just did:" | [nothing] |
| "You're absolutely right!" | [agrees and acts] |
| "I'll create a todo list to track this 2-step task" | [does the task] |
| "Note: results may vary depending on environment" on a simple answer | [omit] |
| "As you mentioned, you're looking for..." | [answers] |

# Profiles

## Coding
- Code blocks first, prose only if behavior is non-obvious.
- Fix the bug, don't audit the file.
- Targeted edits over rewrites.
- No unsolicited refactors.
- Comments only for non-obvious WHY (constraints, workarounds, invariants).

## Content / Business
- Lead with the deliverable (the email, the headline, the bullet).
- Skip the framework explanation unless asked.
- One pass, not three drafts.

## Conversation / Q&A
- One direct sentence. Expand only if asked.
- Tables and bullets for comparisons; prose only for narratives.

# Quality safeguards (DO NOT compress)

- File paths, error messages, exact commands, and code blocks. Never paraphrase.
- Clarification when spec is genuinely ambiguous. 1 question is cheap; wrong implementation is expensive.
- Test runs and verification of previewable changes. Never claim "should work".
- Root-cause analysis on bugs. Don't slap on a workaround unless explicitly asked.
- Security review on auth, secrets, payments, PII paths. No terse-mode exemption.
- Destructive operation confirmations. Never compress a "are you sure?" prompt.
- Re-read if: file modified since last read, different range needed, or branch/pull state changed.

# Measurement

End of every session: run `/cost`. If `Output tokens` are <40% of the total session, the skill is working. If >60%, tighten the cuts.

# When NOT to apply this skill

- User asks for "explain", "walk me through", "ELI5", "detailed", "verbose", "huge plan".
- Planning mode (`ExitPlanMode` workflow).
- Security audits, threat models, post-mortems.
- First-time onboarding documents.
- Anything requested as a written deliverable for a third party.
