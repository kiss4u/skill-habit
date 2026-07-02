#!/usr/bin/env bash
# skill-habit one-command installer
# Usage: curl -sSL https://raw.githubusercontent.com/kiss4u/skill-habit/main/scripts/bootstrap.sh | bash
set -euo pipefail

REPO_URL="https://github.com/kiss4u/skill-habit.git"
INSTALL_DIR="${SKILL_HABIT_INSTALL_DIR:-${HOME}/.claude/skills/skill-habit}"

step() { printf "\n\033[34m[%s/3]\033[0m %s\n" "$1" "$2"; }
log()  { printf "  \033[2m→\033[0m %s\n" "$*"; }
ok()   { printf "\033[32m✓\033[0m %s\n" "$*"; }
err()  { printf "\033[31m✗\033[0m %s\n" "$*" >&2; exit 1; }

# ── pre-flight ───────────────────────────────────────────────────────────────
command -v python3 &>/dev/null || err "python3 3.7+ not found — install: brew install python3"
command -v git     &>/dev/null || err "git not found — install: brew install git"

GIT_MAJOR=$(git --version | grep -oE '[0-9]+' | head -1)
if [[ "$GIT_MAJOR" -lt 2 ]]; then
    printf "\033[33m⚠\033[0m  git 1.x detected — upgrade recommended: brew install git\n"
fi

# ── step 1: download ─────────────────────────────────────────────────────────
step 1 "Downloading skill-habit to $INSTALL_DIR ..."
mkdir -p "$(dirname "$INSTALL_DIR")"
if [[ -d "$INSTALL_DIR/.git" ]]; then
    log "Existing install found — updating to latest..."
    git -C "$INSTALL_DIR" fetch --depth 1 origin main \
        && git -C "$INSTALL_DIR" reset --hard origin/main \
        || err "git update failed — check your network and try again"
elif [[ -d "$INSTALL_DIR" ]]; then
    err "Directory exists but is not a git repo: $INSTALL_DIR
       Remove it first or use a custom path:
         rm -rf \"$INSTALL_DIR\" && re-run this script
         SKILL_HABIT_INSTALL_DIR=~/skill-habit curl -sSL ... | bash"
else
    log "Cloning repository..."
    GIT_TERMINAL_PROMPT=0 git clone --depth 1 --progress "$REPO_URL" "$INSTALL_DIR" \
        || err "git clone failed — check your network and try again"
fi
[[ -f "$INSTALL_DIR/scripts/install.sh" ]] || err "Download incomplete — $INSTALL_DIR/scripts/install.sh missing"
ok "Download complete"

# ── step 2: hooks + shortcuts ────────────────────────────────────────────────
step 2 "Installing hooks and generating shortcuts..."
bash "${INSTALL_DIR}/scripts/install.sh" 2>&1 | sed 's/^/  /'
ok "Hooks registered"

# ── step 3: done ─────────────────────────────────────────────────────────────
step 3 "Done!"
printf "\n"
ok "skill-habit installed at: $INSTALL_DIR"
printf "\n"
printf "  \033[1mNext steps:\033[0m\n"
printf "  1. Start a new Claude Code session — tracking activates automatically\n"
printf "  2. Open the management UI — run this skill in Claude Code:\n"
printf "     /skill-habit:server\n"
printf "\n"
printf "  \033[2mTo uninstall: bash %s/scripts/install.sh --uninstall\033[0m\n" "$INSTALL_DIR"
printf "\n"
