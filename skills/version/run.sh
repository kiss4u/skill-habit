#!/usr/bin/env bash
set -euo pipefail
_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_PLUGIN_ROOT="$(cd "${_DIR}/../.." && pwd)"
python3 - "${_PLUGIN_ROOT}" <<'EOF'
import sys, re
from pathlib import Path
base = Path(sys.argv[1])
toml = base / "pyproject.toml"
if toml.exists():
    m = re.search(r'^version\s*=\s*"([^"]+)"', toml.read_text(), re.MULTILINE)
    if m:
        print("skill-habit", m.group(1))
        raise SystemExit(0)
cl = base / "CHANGELOG.md"
if cl.exists():
    m = re.search(r'## \[([^\]]+)\]', cl.read_text())
    if m:
        print("skill-habit", m.group(1))
        raise SystemExit(0)
print("Version info not found")
EOF
