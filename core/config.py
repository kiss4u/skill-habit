from __future__ import annotations
import copy
import json
from pathlib import Path
from typing import Any

SKILL_HABIT_DIR = Path.home() / ".skill-habit"
CONFIG_FILE = SKILL_HABIT_DIR / "config.json"
LOG_FILE = SKILL_HABIT_DIR / "skill-usage.log"
CACHE_FILE = SKILL_HABIT_DIR / "cache.json"
LOCK_FILE = SKILL_HABIT_DIR / "tracker.lock"
GENERATED_MANIFEST = SKILL_HABIT_DIR / "generated-skills.json"
EVER_GENERATED_MANIFEST = SKILL_HABIT_DIR / "ever-generated-skills.json"
SHORTCUT_MAP = SKILL_HABIT_DIR / "shortcut-map.json"

SCHEMA_VERSION = 1

# M-02: module-level cache to avoid reading from disk on every load() call
_config_cache: dict | None = None

DEFAULT_CONFIG: dict[str, Any] = {
    "config_version": "0.0.1",
    "prefix": "sh",
    "top_n": 5,
    "numeric_n": 5,         # how many numeric shortcuts to generate (sh1…shN)
    "time_window": "all",       # "today" | "week" | "month" | "all"
    "track_all": True,
    "track_namespaces": [],     # used when track_all is False
    "exclude_skills": [],
    "theme": "system",          # "light" | "dark" | "system"
    "language": "auto",         # "zh" | "en" | "auto"
    "shortcut_mode": "both",    # "numeric" | "command" | "both" — which types are supported
    "active_mode": "both",      # "numeric" | "command" | "both" — which type is currently active
    "enable_sequence_prediction": True,
    "prediction_n": 5,              # how many next-skill candidates to boost (1–5)
    "top_skills_n": 5,            # rows shown in the Top Skills chart
    "analytics_cards": {
        "heatmap": True,
        "top_skills": True,
        "transition_graph": True,
        "hourly_distribution": True,
        "weekday_distribution": True,
    },
    "custom_descriptions": {},  # {skill_name: "custom desc"}
    "pinned_skills": [],        # always shown at top regardless of frequency
    "blacklist": [],            # skills excluded from frequency ranking and shortcuts
    "log_retention_days": 30,   # rolling window; 0 = keep forever
    "rerank_interval_secs": 60, # how often to auto re-rank shortcuts after skill use (seconds)
}


def load() -> dict[str, Any]:
    global _config_cache
    if _config_cache is not None:
        return copy.deepcopy(_config_cache)
    SKILL_HABIT_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        _config_cache = DEFAULT_CONFIG.copy()
        return copy.deepcopy(_config_cache)
    with open(CONFIG_FILE) as f:
        data = json.load(f)
    # Merge: new keys in DEFAULT_CONFIG are added, user values take precedence
    merged = _deep_merge(DEFAULT_CONFIG, data)
    _config_cache = merged
    return copy.deepcopy(merged)


def save(config: dict[str, Any]) -> None:
    global _config_cache
    SKILL_HABIT_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    _config_cache = None


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = base.copy()
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = val
    return result


# Static fallback for built-in Claude Code slash commands.
# Used when dynamic binary scan is unavailable.
_CLAUDE_CODE_BUILTINS_STATIC: frozenset[str] = frozenset({
    # Core
    "help", "status", "skills", "compact", "clear", "doctor",
    "memory", "config", "mcp", "review", "init", "sandbox",
    "statusline", "stickers", "security-review",
    # Navigation / session
    "resume", "continue", "reset", "new", "background", "bg",
    "branch", "fork", "stop", "tasks", "bashes", "recap",
    # Model / settings
    "model", "effort", "theme", "settings", "agents", "plan",
    "autocompact", "update", "upgrade", "update-config",
    # Info / help
    "usage", "cost", "stats", "version", "release-notes",
    "hooks", "keybindings", "context", "debug", "feedback",
    "ide", "login", "logout", "reload-plugins", "plugins",
    # Chat shortcuts
    "btw", "brief", "batch",
    # Misc
    "chrome", "voice", "zoom", "loops", "schedule", "routines",
    "ultraplan", "ultrareview", "code-review", "simplify",
    "remote-control", "toggle-memory", "rewind", "run",
})

# Module-level cache for dynamic detection result (populated once per process)
_builtins_cache: frozenset[str] | None = None


def _detect_claude_code_builtins() -> frozenset[str]:
    """Scan the Claude Code binary to extract built-in slash command names."""
    global _builtins_cache
    if _builtins_cache is not None:
        return _builtins_cache

    try:
        import re as _re
        import shutil
        import os

        claude_bin = shutil.which("claude")
        if not claude_bin:
            _builtins_cache = _CLAUDE_CODE_BUILTINS_STATIC
            return _builtins_cache

        # Resolve symlinks to actual binary
        real_bin = os.path.realpath(claude_bin)
        # Look for the minified bundle next to the binary
        exe = Path(real_bin).with_suffix(".exe")
        if not exe.exists():
            exe = Path(real_bin)
        if not exe.exists() or exe.stat().st_size < 1_000_000:
            _builtins_cache = _CLAUDE_CODE_BUILTINS_STATIC
            return _builtins_cache

        with open(exe, "rb") as f:
            data = f.read()

        # Slash commands have {name:"cmd", ... + one of these properties nearby
        slash_ctx = [
            b"load:()=>Promise", b"isEnabled:()=>", b"immediate:!0",
            b"immediate:(", b"argumentHint:", b"thinClientDispatch:",
            b"whenToUse:", b"isHidden:!", b"supportsNonInteractive:",
        ]
        name_re = _re.compile(rb'[{,]name:"([a-z][a-z0-9-]{1,25})"')
        alias_re = _re.compile(rb'aliases:\[([^\]]+)\]')
        alias_name_re = _re.compile(rb'"([a-z][a-z0-9-]{1,20})"')

        found: set[str] = set()
        for m in name_re.finditer(data):
            ctx = data[m.start(): m.start() + 600]
            if any(kw in ctx for kw in slash_ctx):
                found.add(m.group(1).decode())

        for am in alias_re.finditer(data):
            ctx = data[max(0, am.start() - 300): am.start() + 300]
            if any(kw in ctx for kw in slash_ctx):
                for alias in alias_name_re.findall(am.group(1)):
                    found.add(alias.decode())

        _builtins_cache = frozenset(found) | _CLAUDE_CODE_BUILTINS_STATIC
    except Exception:
        _builtins_cache = _CLAUDE_CODE_BUILTINS_STATIC

    return _builtins_cache


# Backwards-compatible alias used by get_all_command_names()
CLAUDE_CODE_BUILTINS: set[str] = set(_CLAUDE_CODE_BUILTINS_STATIC)


def get_all_command_names(cur_prefix: str | None = None) -> dict[str, list[str]]:
    """Return all command names grouped by source, excluding cur_prefix's own shortcuts."""
    result: dict[str, list[str]] = {"builtin": [], "skill": [], "plugin": []}
    result["builtin"] = sorted(_detect_claude_code_builtins())

    skills_dir = Path.home() / ".claude" / "skills"
    cur_exc = f"{cur_prefix}-" if cur_prefix else None

    def _is_own(name: str) -> bool:
        if not cur_prefix:
            return False
        return (
            name.startswith(cur_exc)
            or (name.startswith(cur_prefix) and len(name) > len(cur_prefix) and name[len(cur_prefix)].isdigit())
            or name == cur_prefix
            or name == f"{cur_prefix}-manage"
            or name == f"{cur_prefix}_manage"
        )

    if skills_dir.exists():
        for d in skills_dir.iterdir():
            if d.is_dir() and (d / "SKILL.md").exists() and not _is_own(d.name):
                result["skill"].append(d.name)

    # ~/.claude/commands/ — project/user commands (e.g. gsd)
    commands_dir = Path.home() / ".claude" / "commands"
    if commands_dir.exists():
        for d in commands_dir.iterdir():
            if d.is_dir():
                result["skill"].append(d.name)

    # ~/.claude/plugins/cache/{marketplace}/{plugin-name}/{version}/skills/…
    # Claude Code fuzzy search matches BOTH the namespace prefix AND the skill name after ':'
    # so we must track both: "didi-ee-toolkit" (namespace) and "kunpeng" (skill name)
    plugins_dir = Path.home() / ".claude" / "plugins" / "cache"
    if plugins_dir.exists():
        plugin_namespaces: set[str] = set()
        plugin_skill_names: set[str] = set()
        for marketplace in plugins_dir.iterdir():
            if not marketplace.is_dir():
                continue
            for plugin_dir in marketplace.iterdir():
                if not plugin_dir.is_dir():
                    continue
                plugin_namespaces.add(plugin_dir.name)
                # Collect individual skill dir names under all versions
                for version_dir in plugin_dir.iterdir():
                    if not version_dir.is_dir():
                        continue
                    skills_subdir = version_dir / "skills"
                    if skills_subdir.is_dir():
                        for skill_dir in skills_subdir.iterdir():
                            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                                plugin_skill_names.add(skill_dir.name)
        for ns in sorted(plugin_namespaces):
            result["plugin"].append(ns)
        # Store skill names as "plugin_skill" type for richer conflict reporting
        result["plugin_skill"] = sorted(plugin_skill_names)

    result["plugin"].sort()
    result["skill"].sort()
    return result


def suggest_prefix(cur_prefix: str | None = None, n: int = 5) -> list[dict[str, Any]]:
    """Return up to n conflict-free single-letter prefix suggestions with reason detail."""
    import string
    all_cmds = get_all_command_names(cur_prefix)
    all_names: list[tuple[str, str]] = (
        [(name, "builtin") for name in all_cmds["builtin"]]
        + [(name, "skill") for name in all_cmds["skill"]]
        + [(name, "plugin") for name in all_cmds.get("plugin", [])]
        + [(name, "plugin_skill") for name in all_cmds.get("plugin_skill", [])]
    )

    results: list[dict[str, Any]] = []
    for letter in string.ascii_lowercase:
        conflicts = [
            {"name": name, "type": src}
            for name, src in all_names
            if name.startswith(letter)
        ]
        results.append({"prefix": letter, "conflicts": conflicts})
        if len([r for r in results if not r["conflicts"]]) >= n:
            break

    clean = [r for r in results if not r["conflicts"]]
    return clean[:n]
