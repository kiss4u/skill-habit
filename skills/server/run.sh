#!/usr/bin/env bash
# Locate and launch the skill-habit web UI server.
# Port priority: last-used port → configured port (default 5027) → random fallback.
set -euo pipefail

_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_PLUGIN_ROOT="$(cd "${_DIR}/../.." && pwd)"

PORT_FILE="${HOME}/.skill-habit/ui.port"
CONFIG_FILE="${HOME}/.skill-habit/config.json"

# Configured port (default 5027)
_CFG_PORT=$(python3 -c "
import json
try:
    c = json.load(open('${CONFIG_FILE}'))
    print(c.get('ui_port', 5027))
except Exception:
    print(5027)
" 2>/dev/null || echo 5027)

# If a server is running, shut it down and remember its port
_LAST_PORT=""
if [[ -f "$PORT_FILE" ]]; then
    _LAST_PORT=$(cat "$PORT_FILE" 2>/dev/null || true)
    if [[ -n "$_LAST_PORT" ]]; then
        curl -s -m 2 -X POST "http://127.0.0.1:${_LAST_PORT}/api/shutdown" \
            -H "Content-Type: application/json" -d '{}' >/dev/null 2>&1 || true
        for _ in 1 2 3 4 5 6; do
            [[ -f "$PORT_FILE" ]] || break
            sleep 0.5
        done
        rm -f "$PORT_FILE"
    fi
fi

# Use last-used port if available, otherwise fall back to configured port
_TARGET_PORT="${_LAST_PORT:-${_CFG_PORT}}"
exec python3 "${_PLUGIN_ROOT}/ui/server.py" --port "${_TARGET_PORT}"
