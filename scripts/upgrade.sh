#!/usr/bin/env bash
# skill-habit one-command upgrade
# Usage: bash scripts/upgrade.sh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

log() { printf "\033[34m[skill-habit]\033[0m %s\n" "$*"; }
ok()  { printf "\033[32m[skill-habit]\033[0m %s\n" "$*"; }
err() { printf "\033[31m[skill-habit]\033[0m %s\n" "$*" >&2; }

log "Pulling latest changes..."
git -C "$REPO_DIR" pull

log "Regenerating shortcut skills..."
python3 "$REPO_DIR/adapters/claude_code/skill_generator.py"

ok "Upgrade complete. Start a new Claude Code session to use updated skills."
