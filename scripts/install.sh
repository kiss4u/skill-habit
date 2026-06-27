#!/usr/bin/env bash
# skill-habit installer for Claude Code
# Usage: bash scripts/install.sh [--uninstall]
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_HABIT_DIR="${HOME}/.skill-habit"
HOOKS_DIR="${SKILL_HABIT_DIR}/hooks"
CLAUDE_SETTINGS="${HOME}/.claude/settings.json"

log() { printf "\033[34m[skill-habit]\033[0m %s\n" "$*"; }
ok()  { printf "\033[32m[skill-habit]\033[0m %s\n" "$*"; }
err() { printf "\033[31m[skill-habit]\033[0m %s\n" "$*" >&2; }

# ── uninstall ────────────────────────────────────────────────────────────────
if [[ "${1:-}" == "--uninstall" ]]; then
    log "Removing generated shortcut skills..."
    python3 "${REPO_DIR}/adapters/claude_code/skill_generator.py" --clear 2>/dev/null || true
    log "Removing hooks..."
    rm -rf "$HOOKS_DIR"
    log "Removing hook entries from settings.json..."
    python3 - "$CLAUDE_SETTINGS" <<'PYEOF'
import json, sys
path = sys.argv[1]
with open(path) as f:
    s = json.load(f)
hooks = s.get("hooks", {})
for event in list(hooks.keys()):
    hooks[event] = [h for h in hooks[event]
                    if "skill-habit" not in json.dumps(h)]
    if not hooks[event]:
        del hooks[event]
s["hooks"] = hooks
with open(path, "w") as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
print("settings.json updated")
PYEOF
    ok "Uninstalled."
    exit 0
fi

# ── pre-flight ───────────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    err "python3 is required but not found."
    exit 1
fi

if [[ ! -f "$CLAUDE_SETTINGS" ]]; then
    err "~/.claude/settings.json not found. Is Claude Code installed?"
    exit 1
fi

# ── install hooks ────────────────────────────────────────────────────────────
mkdir -p "$HOOKS_DIR"

for hook in user-prompt-submit session-start; do
    src="${REPO_DIR}/adapters/claude_code/hooks/${hook}.sh"
    dst="${HOOKS_DIR}/${hook}.sh"
    sed "s|SKILL_HABIT_REPO|${REPO_DIR}|g" "$src" > "$dst"
    chmod +x "$dst"
    log "Installed hook: ${hook}.sh"
done

# ── register hooks in settings.json ─────────────────────────────────────────
python3 - "$CLAUDE_SETTINGS" "$HOOKS_DIR" <<'PYEOF'
import json, sys
path, hooks_dir = sys.argv[1], sys.argv[2]
with open(path) as f:
    s = json.load(f)
hooks = s.setdefault("hooks", {})

def add_hook(event, matcher, command):
    entries = hooks.setdefault(event, [])
    # Remove stale skill-habit entries for this event
    hooks[event] = [h for h in entries
                    if "skill-habit" not in json.dumps(h)]
    hooks[event].append({
        "matcher": matcher,
        "_source": "skill-habit",
        "hooks": [{"type": "command", "command": command, "timeout": 5000}]
    })

add_hook("UserPromptSubmit", ".*",
         f"bash \"{hooks_dir}/user-prompt-submit.sh\"")
add_hook("SessionStart", "*",
         f"bash \"{hooks_dir}/session-start.sh\"")

with open(path, "w") as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
print("settings.json updated")
PYEOF

# ── initial skill generation ─────────────────────────────────────────────────
log "Generating initial shortcut skills..."
python3 "${REPO_DIR}/adapters/claude_code/skill_generator.py" || true

ok "skill-habit installed successfully!"
ok "Start a new Claude Code session to activate tracking."
ok "Run management UI: python3 ${REPO_DIR}/ui/server.py"
