#!/usr/bin/env bash
# skill-habit: SessionStart hook
# Rebuilds the frequency-ranked shortcut skills and pre-computes analytics cache.
# Installed by: scripts/install.sh

set -euo pipefail

# ── Resolve repo root ─────────────────────────────────────────────────────────
# scripts/install.sh replaces the literal 'SKILL_HABIT_REPO' with the real path.
# When running as a Claude Code plugin (no replacement), resolve dynamically.
_REPO="SKILL_HABIT_REPO"
if [[ "$_REPO" == "SKILL_HABIT_REPO" ]]; then
    _REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
fi
# ─────────────────────────────────────────────────────────────────────────────

SKILL_HABIT_DIR="${HOME}/.skill-habit"
mkdir -p "$SKILL_HABIT_DIR"

# Rebuild shortcut skills in background so session start isn't blocked
(
    python3 "${_REPO}/adapters/claude_code/skill_generator.py" \
        2>>"${SKILL_HABIT_DIR}/errors.log" || true

    python3 "${_REPO}/scripts/build_cache.py" \
        2>>"${SKILL_HABIT_DIR}/errors.log" || true
) &

exit 0
