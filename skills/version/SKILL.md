---
name: skill-habit:version
description: 显示 skill-habit 当前版本 / Show current installed version
---

Run this now:

```bash
python3 -c "
import re, os
base = os.path.expanduser('~/.local/share/skill-habit')
# Try pyproject.toml first
toml = os.path.join(base, 'pyproject.toml')
if os.path.exists(toml):
    m = re.search(r'^version\s*=\s*\"([^\"]+)\"', open(toml).read(), re.MULTILINE)
    if m:
        print('skill-habit', m.group(1))
        exit()
# Fall back to CHANGELOG.md
cl = os.path.join(base, 'CHANGELOG.md')
if os.path.exists(cl):
    m = re.search(r'## \[([^\]]+)\]', open(cl).read())
    if m:
        print('skill-habit', m.group(1))
        exit()
print('Version info not found')
"
```
