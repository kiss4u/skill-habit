#!/usr/bin/env bash
# Sync dev repo to local install directory (developer use only)
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_DIR="${HOME}/.local/share/skill-habit"

if [[ ! -d "$INSTALL_DIR" ]]; then
  echo "[dev-sync] Install dir not found: $INSTALL_DIR" >&2
  exit 1
fi

rsync -av --exclude='.git' --exclude='.claude' --exclude='__pycache__' \
  "${REPO_DIR}/" "${INSTALL_DIR}/"

echo "[dev-sync] Done."
