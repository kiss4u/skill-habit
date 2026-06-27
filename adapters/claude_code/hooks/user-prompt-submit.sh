#!/usr/bin/env bash
# skill-habit: UserPromptSubmit hook
# Detects skill invocations (prompts starting with /) and records them.
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

INPUT=$(cat)

PROMPT=$(printf '%s' "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('prompt', ''))
except Exception:
    pass
" 2>/dev/null || true)

# Only track slash-commands
[[ "$PROMPT" == /* ]] || exit 0

SESSION_ID=$(printf '%s' "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('session_id', 'unknown'))
except Exception:
    print('unknown')
" 2>/dev/null || echo "unknown")

# Extract skill name: "/opsx:propose fix the bug" -> "opsx:propose"
SKILL_NAME=$(printf '%s' "$PROMPT" | sed 's|^/||' | awk '{print $1}')
[[ -n "$SKILL_NAME" ]] || exit 0

# Count characters after the skill name as args_len
ARGS=$(printf '%s' "$PROMPT" | sed "s|^/$SKILL_NAME||" | sed 's|^ *||')
ARGS_LEN=${#ARGS}

SKILL_HABIT_DIR="${HOME}/.skill-habit"
mkdir -p "$SKILL_HABIT_DIR"

SEQ_FILE="${SKILL_HABIT_DIR}/session-${SESSION_ID}.seq"
LOCK_FILE="${SKILL_HABIT_DIR}/tracker.lock"

# Expand paths before heredoc so bash interpolates them into the Python source
_REPO_RECORD="${_REPO}/adapters/claude_code/record.py"

# Cross-platform locking: use flock (Linux) or Python fcntl (macOS/fallback)
python3 - <<PYEOF 2>/dev/null || true
import sys, os, fcntl, json

seq_file = "$SEQ_FILE"
lock_file = "$LOCK_FILE"

try:
    with open(lock_file, 'a') as lf:
        fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            seq = 0
            if os.path.exists(seq_file):
                try:
                    seq = int(open(seq_file).read().strip())
                except Exception:
                    seq = 0
            seq += 1
            open(seq_file, 'w').write(str(seq))
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)

    import subprocess
    subprocess.run([
        sys.executable,
        "${_REPO_RECORD}",
        "--skill", "$SKILL_NAME",
        "--session-id", "$SESSION_ID",
        "--session-seq", str(seq),
        "--args-len", "$ARGS_LEN",
        "--cwd", os.getcwd(),
    ], capture_output=True)
except Exception:
    pass
PYEOF

# Re-rank shortcuts (throttled). Interval is read from config; default 60s.
LAST_RANKED="${SKILL_HABIT_DIR}/last-ranked.ts"
NOW=$(date +%s)
LAST=0
[[ -f "$LAST_RANKED" ]] && LAST=$(cat "$LAST_RANKED" 2>/dev/null || echo 0)
INTERVAL=$(python3 -c "
import json, os
try:
    cfg = json.load(open(os.path.expanduser('~/.skill-habit/config.json')))
    print(int(cfg.get('rerank_interval_secs', 60)))
except Exception:
    print(60)
" 2>/dev/null || echo 60)
if (( NOW - LAST > INTERVAL )); then
    printf '%s' "$NOW" > "$LAST_RANKED"
    (python3 "${_REPO}/adapters/claude_code/skill_generator.py" \
        2>>"${SKILL_HABIT_DIR}/errors.log" || true) &
fi

exit 0
