#!/usr/bin/env python3
import os, sys, subprocess, shutil, json
from pathlib import Path

home = Path.home()
skill_dir = home / ".claude" / "skills" / "skill-habit"
plugin_root = Path(sys.argv[1]) if len(sys.argv) > 1 else None

if plugin_root and (plugin_root / "adapters/claude_code/skill_generator.py").exists():
    method, base = "A", plugin_root
elif skill_dir.exists() and (skill_dir / ".git").exists():
    method, base = "B", skill_dir
else:
    method, base = "C", None


def _clean_settings_hooks():
    """Remove skill-habit hook entries from ~/.claude/settings.json."""
    settings_path = home / ".claude" / "settings.json"
    if not settings_path.exists():
        return
    try:
        data = json.loads(settings_path.read_text())
        hooks = data.get("hooks", {})
        changed = False
        for event in list(hooks.keys()):
            filtered = [
                entry for entry in hooks[event]
                if not any(
                    "skill-habit" in str(h.get("command", "")) or
                    "skill_habit" in str(h.get("command", ""))
                    for h in entry.get("hooks", [entry] if "command" in entry else [])
                )
            ]
            if len(filtered) != len(hooks[event]):
                hooks[event] = filtered
                changed = True
            if not hooks[event]:
                del hooks[event]
                changed = True
        if changed:
            data["hooks"] = hooks
            settings_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"  warning: could not clean settings.json hooks: {e}")


def _clean_plugin_cache():
    """Remove plugin cache and marketplace local clone for skill-habit."""
    for path in [
        home / ".claude" / "plugins" / "cache" / "skill-habit",
        home / ".claude" / "plugins" / "marketplaces" / "skill-habit",
    ]:
        if path.exists():
            shutil.rmtree(str(path), ignore_errors=True)


def _clean_installed_registry():
    """Remove skill-habit entry from installed_plugins.json."""
    registry = home / ".claude" / "plugins" / "installed_plugins.json"
    if not registry.exists():
        return
    try:
        data = json.loads(registry.read_text())
        plugins = data.get("plugins", {})
        removed = plugins.pop("skill-habit@skill-habit", None)
        if removed is not None:
            data["plugins"] = plugins
            registry.write_text(json.dumps(data, indent=4))
    except Exception as e:
        print(f"  warning: could not clean installed_plugins.json: {e}")


print("Cleaning up...")

if method == "A":
    subprocess.run([sys.executable, str(base / "adapters/claude_code/skill_generator.py"), "--clear"])
elif method == "B":
    subprocess.run(["bash", str(base / "scripts/install.sh"), "--uninstall"])
    shutil.rmtree(str(base), ignore_errors=True)
elif shutil.which("skill-habit"):
    subprocess.run(["skill-habit", "uninstall"])

_clean_settings_hooks()
_clean_plugin_cache()
_clean_installed_registry()

print()
if method == "C":
    print("Done. Complete the uninstall by running:")
    print("  pipx uninstall skill-habit   # or: pip uninstall skill-habit")
else:
    print("Done.")
