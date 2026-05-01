# Benchmarks

Methodology copied from adam-s/testing-claude-agent: same prompt, isolated worktree, ≥2 reps per task, measure tokens to green.

## Run

For each task in this folder:

1. Open Claude Code in a clean worktree with the skill installed.
2. Paste the task prompt.
3. Wait for completion.
4. Run `/cost` and record `Total tokens`.
5. Repeat once more (different session).
6. Average.

Then repeat the whole thing without the skill (rename `~/.claude/skills/token-efficient` to `.bak` first). Compare averages.

## Pass criteria

- All tests/assertions pass on both runs.
- Total tokens averaged across reps is at least 20% lower with the skill than without.

If the skill loses on simple tasks (CSV reporter), that's expected — the skill description loads as input on every turn, and on tiny tasks the input cost dominates. The win shows up on multi-step debug tasks.
