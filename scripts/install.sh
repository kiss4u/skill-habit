#!/usr/bin/env bash
# skill-habit installer for Claude Code
# Usage: bash scripts/install.sh [--uninstall]
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_HABIT_DIR="${HOME}/.skill-habit"
HOOKS_DIR="${SKILL_HABIT_DIR}/hooks"
CLAUDE_SETTINGS="${HOME}/.claude/settings.json"

log()  { printf "\033[34m[skill-habit]\033[0m %s\n" "$*"; }
ok()   { printf "\033[32m[skill-habit]\033[0m %s\n" "$*"; }
warn() { printf "\033[33m[skill-habit]\033[0m %s\n" "$*" >&2; }
err()  { printf "\033[31m[skill-habit]\033[0m %s\n" "$*" >&2; exit 1; }

# ── uninstall ────────────────────────────────────────────────────────────────
if [[ "${1:-}" == "--uninstall" ]]; then
    log "Removing generated shortcut skills..."
    if ! python3 "${REPO_DIR}/adapters/claude_code/skill_generator.py" --clear; then
        warn "Shortcut cleanup failed — you may manually remove ~/.claude/skills/sh* and ~/.claude/skills/skill-habit"
    fi
    log "Removing hooks..."
    rm -rf "$HOOKS_DIR"
    log "Removing hook entries from settings.json..."
    if [[ -f "$CLAUDE_SETTINGS" ]]; then
        python3 - "$CLAUDE_SETTINGS" <<'PYEOF'
import json, sys, os, tempfile
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
tmp = path + ".tmp"
with open(tmp, "w") as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
os.replace(tmp, path)
print("settings.json updated")
PYEOF
    fi
    ok "Uninstalled."
    exit 0
fi

# ── pre-flight ───────────────────────────────────────────────────────────────
command -v python3 &>/dev/null || err "python3 is required but not found."

[[ -f "$CLAUDE_SETTINGS" ]] || err "~/.claude/settings.json not found. Is Claude Code installed?"

# ── install hooks ────────────────────────────────────────────────────────────
mkdir -p "$HOOKS_DIR"

for hook in user-prompt-submit session-start; do
    src="${REPO_DIR}/adapters/claude_code/hooks/${hook}.sh"
    dst="${HOOKS_DIR}/${hook}.sh"
    [[ -f "$src" ]] || err "Hook source not found: $src"
    python3 -c "
import sys
src, dst, val = sys.argv[1:]
with open(src) as f: content = f.read()
with open(dst, 'w') as f: f.write(content.replace('SKILL_HABIT_REPO', val))
" "$src" "$dst" "$REPO_DIR"
    chmod +x "$dst"
    log "Installed hook: ${hook}.sh"
done

# ── register hooks in settings.json ─────────────────────────────────────────
python3 - "$CLAUDE_SETTINGS" "$HOOKS_DIR" <<'PYEOF'
import json, sys, os
path, hooks_dir = sys.argv[1], sys.argv[2]
with open(path) as f:
    s = json.load(f)
hooks = s.setdefault("hooks", {})

def add_hook(event, command, matcher=None):
    entries = hooks.setdefault(event, [])
    hooks[event] = [h for h in entries
                    if "skill-habit" not in json.dumps(h)]
    entry = {"_source": "skill-habit",
             "hooks": [{"type": "command", "command": command, "timeout": 5000}]}
    if matcher is not None:
        entry["matcher"] = matcher
    hooks[event].append(entry)

add_hook("UserPromptSubmit", f"bash \"{hooks_dir}/user-prompt-submit.sh\"", matcher=".*")
add_hook("SessionStart",     f"bash \"{hooks_dir}/session-start.sh\"")

tmp = path + ".tmp"
with open(tmp, "w") as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
os.replace(tmp, path)
print("settings.json updated")
PYEOF

# ── initial skill generation ─────────────────────────────────────────────────
log "Generating initial shortcut skills..."
if ! python3 "${REPO_DIR}/adapters/claude_code/skill_generator.py"; then
    warn "Shortcut generation failed — run '/skill-habit:server' to retry from the UI"
fi

echo ""
ok "✔ skill-habit installed successfully!"
echo ""
warn "⚠  Restart Claude Code now — skills won't appear until you do."
echo ""
ok "After restarting, run  /skill-habit:server  in Claude Code to open the"
ok "web management UI where you can add habits, view stats, and configure shortcuts."
