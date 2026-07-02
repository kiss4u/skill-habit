#!/usr/bin/env bash
# skill-habit full uninstaller — for method-B bootstrap installs
# Usage: bash ~/.claude/skills/skill-habit/scripts/uninstall.sh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

log() { printf "\033[34m[skill-habit]\033[0m %s\n" "$*"; }
ok()  { printf "\033[32m[skill-habit]\033[0m %s\n" "$*"; }

log "Removing hooks and generated skills..."
bash "${REPO_DIR}/scripts/install.sh" --uninstall

log "Removing install directory: $REPO_DIR"
(cd "$HOME" && rm -rf "$REPO_DIR")

ok "skill-habit uninstalled."
printf "\n  \033[2mOptional — remove user data too:\033[0m\n"
printf "  \033[2mrm -rf ~/.skill-habit\033[0m\n\n"
