#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$HOME/.claude/skills/token-efficient"

mkdir -p "$SKILL_DIR"
ln -sfn "$REPO_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"

echo "Installed: $SKILL_DIR/SKILL.md -> $REPO_DIR/SKILL.md"
echo "Verify in Claude Code: /skills"
