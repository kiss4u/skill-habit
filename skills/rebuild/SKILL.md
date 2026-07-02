---
name: skill-habit:rebuild
description: 立即重建 skill-habit 快捷技能 / Rebuild skill shortcuts immediately
---

Use the Bash tool to run the command below. Do NOT show the command to the user — just say "Rebuilding skill-habit shortcuts…" then report success or any error.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/rebuild/run.sh"
```

Run this after manually editing `~/.skill-habit/config.json` to apply changes without restarting the session.
