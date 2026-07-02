---
name: skill-habit:uninstall
description: 卸载 skill-habit / Uninstall skill-habit
---

Before running anything, ask the user:

"Uninstall skill-habit — what should be removed?
1. Plugin & shortcuts only (keep usage history and config in ~/.skill-habit)
2. Everything (plugin, shortcuts, and all user data in ~/.skill-habit)"

Wait for their answer. Then run these steps silently (do not show any commands):

1. Run `bash "${CLAUDE_PLUGIN_ROOT}/skills/uninstall/run.sh"` and show only its output.
2. Run `claude plugins uninstall skill-habit 2>/dev/null || true` to remove the plugin from Claude Code's registry.
3. If the user chose **2**, also run `rm -rf ~/.skill-habit`.

Tell the user: "Uninstall complete. Please restart Claude Code for the changes to take effect."
