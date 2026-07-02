#!/usr/bin/env bash
set -euo pipefail
_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_PLUGIN_ROOT="$(cd "${_DIR}/../.." && pwd)"
exec python3 "${_PLUGIN_ROOT}/skills/uninstall/run.py" "${_PLUGIN_ROOT}"
