#!/usr/bin/env bash
# skill-habit one-command installer
# Usage: curl -sSL https://raw.githubusercontent.com/kiss4u/skill-habit/main/scripts/bootstrap.sh | bash
set -euo pipefail

# Reconnect stdin to the real terminal so git clone can show progress
# (when piped via curl|bash, stdin is the pipe — this fixes it)
exec </dev/tty

REPO_URL="https://github.com/kiss4u/skill-habit.git"
INSTALL_DIR="${SKILL_HABIT_INSTALL_DIR:-${HOME}/.local/share/skill-habit}"

log() { printf "\033[34m[skill-habit]\033[0m %s\n" "$*"; }
ok()  { printf "\033[32m[skill-habit]\033[0m %s\n" "$*"; }
err() { printf "\033[31m[skill-habit]\033[0m %s\n" "$*" >&2; exit 1; }

command -v python3 &>/dev/null || err "python3 3.9+ is required but not found. Install: brew install python3 (macOS) or https://python.org/downloads"
command -v git    &>/dev/null || err "git is required but not found."

if [[ -d "$INSTALL_DIR/.git" ]]; then
    log "Updating existing install at ${INSTALL_DIR}..."
    git -C "$INSTALL_DIR" pull --ff-only
else
    log "Installing to ${INSTALL_DIR}..."
    mkdir -p "$(dirname "$INSTALL_DIR")"
    git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
fi

log "Registering hooks..."
bash "${INSTALL_DIR}/scripts/install.sh"

ok ""
ok "Done! Start a new Claude Code session to activate tracking."
ok ""
ok "To open the management UI:"
ok "  python3 ${INSTALL_DIR}/ui/server.py"
ok ""
ok "To uninstall:"
ok "  bash ${INSTALL_DIR}/scripts/install.sh --uninstall"
