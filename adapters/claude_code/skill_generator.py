from __future__ import annotations
import fcntl
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any

# Allow running as a standalone script
_REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from core.config import (
    EVER_GENERATED_MANIFEST,
    GENERATED_MANIFEST,
    LOCK_FILE,
    LOG_FILE,
    SHORTCUT_MAP,
    SKILL_HABIT_DIR,
    load as load_config,
    save as save_config,
    suggest_prefix,
)
from core.analyzer import top_skills, predict_next, trim_log

CLAUDE_DIR = Path.home() / ".claude"
CLAUDE_SKILLS_DIR = CLAUDE_DIR / "skills"
CLAUDE_COMMANDS_DIR = CLAUDE_DIR / "commands"

# Plugin skills live under ~/.claude/plugins/cache/
PLUGIN_SKILLS_GLOB = str(CLAUDE_DIR / "plugins" / "cache" / "*" / "*" / "*" / "skills" / "*" / "SKILL.md")

# skill-habit:quick lives here — content is static (reads prefix from config.json at runtime)
_QUICK_SKILL_DIR = CLAUDE_SKILLS_DIR / "skill-habit" / "skills" / "quick"

_QUICK_SKILL_CONTENT = (
    "---\nname: skill-habit:quick\n"
    "description: 快速显示当前快捷前缀和技能映射 / Show current prefix and shortcut mappings\n---\n\n"
    "Use the Bash tool to run the command below. Do NOT show the command to the user — show only its output.\n\n"
    "```bash\npython3 -c \"\nimport json, os, locale\n\n"
    "cfg = os.path.expanduser('~/.skill-habit/config.json')\n"
    "smap = os.path.expanduser('~/.skill-habit/shortcut-map.json')\n\n"
    "d = json.load(open(cfg)) if os.path.exists(cfg) else {}\n"
    "prefix = d.get('prefix', 'sh')\n"
    "lang = d.get('language', 'auto')\n"
    "if lang == 'auto':\n"
    "    sys_lang = (locale.getdefaultlocale()[0] or '').lower()\n"
    "    lang = 'zh' if sys_lang.startswith('zh') else 'en'\n\n"
    "L = {\n"
    "    'zh': ('前缀', '管理界面', '快捷键', '技能'),\n"
    "    'de': ('Präfix', 'Web-UI', 'Kürzel', 'Skill'),\n"
    "    'fr': ('Préfixe', 'Interface web', 'Raccourci', 'Skill'),\n"
    "    'ru': ('Префикс', 'Веб-интерфейс', 'Ярлык', 'Навык'),\n"
    "    'ko': ('접두사', '관리 UI', '단축키', '스킬'),\n"
    "    'ja': ('プレフィックス', '管理UI', 'ショートカット', 'スキル'),\n"
    "}.get(lang, ('Prefix', 'Web UI', 'Shortcut', 'Skill'))\n"
    "lbl_prefix, lbl_webui, lbl_shortcut, lbl_skill = L\n\n"
    "print(f'{lbl_prefix}: {prefix}')\n"
    "print(f'{lbl_webui}: /skill-habit:server')\n\n"
    "if os.path.exists(smap):\n"
    "    sm = json.load(open(smap))\n"
    "    nums = sorted(\n"
    "        [(k, v) for k, v in sm.items()\n"
    "         if k != '_prefix' and k.startswith(prefix) and k[len(prefix):len(prefix)+1].isdigit()],\n"
    "        key=lambda x: len(x[0])\n"
    "    )\n"
    "    if nums:\n"
    "        print()\n"
    "        print(f'  {lbl_shortcut:<16}{lbl_skill}')\n"
    "        print(f'  {\\\"-\\\" * 16}{\\\"-\\\" * 20}')\n"
    "        for sh, skill in nums[:5]:\n"
    "            print(f'  /{sh:<15} {skill}')\n"
    "\"\n```\n"
)

# Static plugin skills to sync from repo → ~/.claude/skills/skill-habit/skills/
_PLUGIN_DIR = CLAUDE_SKILLS_DIR / "skill-habit"
_STATIC_SKILLS = ("server", "version", "rebuild", "uninstall")

_PLUGIN_JSON_CONTENT = json.dumps({
    "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
    "name": "skill-habit",
    "version": "0.0.1",
    "description": "skill-habit management skills — quick info, web UI, version, rebuild",
    "author": {"name": "kiss4u"},
    "skills": ["./skills/quick", "./skills/server", "./skills/version", "./skills/rebuild", "./skills/uninstall"],
}, indent=2, ensure_ascii=False) + "\n"


def scan_all_skills() -> dict[str, dict[str, str]]:
    """
    Return {skill_name: {description, content, source_path, dir_slug}} for all installed skills.
    Scans ~/.claude/skills/, marketplace plugin caches, and ~/.claude/commands/.
    """
    skills: dict[str, dict[str, str]] = {}
    _scan_dir(CLAUDE_SKILLS_DIR, skills)
    _scan_commands_dir(CLAUDE_COMMANDS_DIR, skills)
    plugin_base = CLAUDE_DIR / "plugins" / "cache"
    if plugin_base.exists():
        for skills_dir in plugin_base.glob("*/*/*/skills"):
            if skills_dir.is_dir():
                _scan_dir(skills_dir, skills)
        for skills_dir in plugin_base.glob("*/*/*/.claude/skills"):
            if skills_dir.is_dir():
                # Plugin namespace = second component after cache/ (e.g. "voicemode")
                plugin_name = skills_dir.relative_to(plugin_base).parts[1]
                before = set(skills.keys())
                _scan_dir(skills_dir, skills)
                for skill_name in set(skills.keys()) - before:
                    namespaced = f"{plugin_name}:{skill_name}"
                    if namespaced not in skills:
                        skills[namespaced] = skills[skill_name]
    return skills


def _scan_commands_dir(commands_dir: Path, out: dict[str, dict[str, str]]) -> None:
    """Scan ~/.claude/commands/ for .md slash-command files (flat and one level deep)."""
    if not commands_dir.exists():
        return
    for item in commands_dir.iterdir():
        if item.is_file() and item.suffix == ".md":
            _add_command_file(item, commands_dir, out)
        elif item.is_dir():
            for md_file in sorted(item.glob("*.md")):
                _add_command_file(md_file, commands_dir, out)


def _add_command_file(path: Path, commands_dir: Path, out: dict[str, dict[str, str]]) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return
    name, description = _parse_frontmatter(content)
    if not name:
        # Derive from path: commands/opsx/apply.md → opsx:apply, commands/apply.md → apply
        rel = path.relative_to(commands_dir)
        name = ":".join(rel.with_suffix("").parts)
    if name not in out:
        out[name] = {
            "description": description,
            "content": content,
            "source_path": str(path),
            "dir_slug": path.stem,
        }


def _scan_dir(skills_dir: Path, out: dict[str, dict[str, str]]) -> None:
    if not skills_dir.exists():
        return
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        try:
            content = skill_file.read_text(encoding="utf-8")
        except OSError:
            continue
        name, description = _parse_frontmatter(content)
        if not name:
            name = skill_dir.name
            print(f"[skill-habit] warn: {skill_file} has no name: in frontmatter, using dir name '{name}'", file=sys.stderr)
        if name not in out:
            out[name] = {
                "description": description,
                "content": content,
                "source_path": str(skill_file),
                "dir_slug": skill_dir.name,
            }


def _parse_frontmatter(content: str) -> tuple[str, str]:
    # Returns ("", "") for malformed frontmatter; callers skip skills with empty names.
    lines = content.split("\n")
    if not lines or lines[0].strip() != "---":
        return "", ""
    name = description = ""
    i = 1
    while i < len(lines):
        if lines[i].strip() == "---":
            break
        if lines[i].startswith("name:"):
            name = lines[i][5:].strip()
        elif lines[i].startswith("description:"):
            description = lines[i][12:].strip().lstrip(">").strip()
        i += 1
    return name, description


def _body_after_frontmatter(content: str) -> str:
    lines = content.split("\n")
    if not lines or lines[0].strip() != "---":
        return content
    i = 1
    while i < len(lines):
        if lines[i].strip() == "---":
            return "\n".join(lines[i + 1:]).strip()
        i += 1
    return content


def _safe_dir_name(skill_name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "-", skill_name)


def _last_used_skill() -> str | None:
    """Return the most recently logged skill across all sessions."""
    if not LOG_FILE.exists():
        return None
    with open(LOG_FILE, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
        f.seek(max(0, size - 4096))
        tail = f.read().decode(errors="replace")
    for line in reversed(tail.splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            s = entry.get("skill")
            if s:
                return s
        except Exception:
            continue
    return None


def _auto_detect_prefix(config: dict[str, Any]) -> dict[str, Any]:
    """On first install, pick a conflict-free prefix if the default 'sh' conflicts."""
    if GENERATED_MANIFEST.exists():
        return config  # Not first install
    current = config.get("prefix", "sh")
    suggestions = suggest_prefix(cur_prefix=None, n=1)
    if not suggestions:
        return config  # No clean prefix found, keep as-is
    clean_options = [s["prefix"] for s in suggestions]
    # If the current prefix is already clean, keep it
    if current in clean_options:
        return config
    # Check if current prefix actually has conflicts
    from core.config import get_all_command_names
    all_cmds = get_all_command_names(cur_prefix=None)
    has_conflict = any(
        name.startswith(current)
        for names in all_cmds.values()
        for name in names
    )
    if not has_conflict:
        return config  # Current prefix is fine
    # Auto-pick first clean option and save
    new_prefix = clean_options[0]
    config = config.copy()
    config["prefix"] = new_prefix
    save_config(config)
    print(f"[skill-habit] Auto-selected prefix '{new_prefix}' ('{current}' conflicts with existing commands)", flush=True)
    return config


def _atomic_write_skill(skill_dir: Path, content: str) -> bool:
    """Write content to skill_dir/SKILL.md using atomic tmp→rename. Returns True if changed."""
    existing_file = skill_dir / "SKILL.md"
    if skill_dir.exists() and existing_file.exists():
        try:
            if existing_file.read_text(encoding="utf-8") == content:
                return False
        except OSError:
            pass
    tmp_dir = skill_dir.parent / f"{skill_dir.name}.tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    (tmp_dir / "SKILL.md").write_text(content, encoding="utf-8")
    if skill_dir.exists():
        shutil.rmtree(skill_dir)
    tmp_dir.rename(skill_dir)
    return True


def _write_skill_file(path: Path, content: str) -> bool:
    """Write content to path/SKILL.md in place, skipping if unchanged. Returns True if changed."""
    path.mkdir(parents=True, exist_ok=True)
    skill_file = path / "SKILL.md"
    if skill_file.exists():
        try:
            if skill_file.read_text(encoding="utf-8") == content:
                return False
        except OSError:
            pass
    skill_file.write_text(content, encoding="utf-8")
    return True



def generate(config: dict[str, Any] | None = None) -> None:
    if config is None:
        config = load_config()
    config = _auto_detect_prefix(config)

    retention = config.get("log_retention_days", 180)
    if retention > 0:
        trim_log(retention)

    prefix = config.get("prefix", "sh")
    top_n = config.get("top_n", 10)
    numeric_n = config.get("numeric_n", 5)
    time_window = config.get("time_window", "all")
    pinned = config.get("pinned_skills", [])
    custom_desc = config.get("custom_descriptions", {})
    exclude = set(config.get("exclude_skills", [])) | set(config.get("blacklist", []))
    shortcut_mode = config.get("active_mode") or config.get("shortcut_mode", "both")
    commands_shortcuts = config.get("commands_generate_shortcuts", True)

    all_skills = scan_all_skills()

    # Never generate shortcuts for the prefix namespace or skill-habit's own meta-skills
    exclude.add(prefix)
    _commands_str = str(CLAUDE_COMMANDS_DIR) + "/"
    def _is_shortcut(s: str) -> bool:
        return s.startswith(f"{prefix}-") or (s.startswith(prefix) and s[len(prefix):][:1].isdigit())
    def _is_self(s: str) -> bool:
        return s.startswith("skill-habit:")
    def _is_command(s: str) -> bool:
        src = all_skills.get(s, {}).get("source_path", "")
        return bool(src and src.startswith(_commands_str))

    ranked = [
        r for r in top_skills(time_window, n=top_n * 5)
        if r["skill"] not in exclude
        and not _is_shortcut(r["skill"])
        and not _is_self(r["skill"])
        and r["skill"] in all_skills
        and (commands_shortcuts or not _is_command(r["skill"]))
    ]
    ranked_names = [r["skill"] for r in ranked]

    # Association boost: surface skills likely to follow your most recent usage.
    # Uses the global transition matrix (all sessions), not just the current one.
    if config.get("enable_sequence_prediction", True):
        last_skill = _last_used_skill()
        if last_skill and last_skill in all_skills and last_skill not in exclude:
            prediction_n = min(5, max(1, config.get("prediction_n", 5)))
            predicted = predict_next(last_skill, time_window, n=min(numeric_n, prediction_n))
            predicted_valid = [s for s in predicted if s in set(ranked_names)]
            if predicted_valid:
                predicted_set = set(predicted_valid)
                ranked_names = predicted_valid + [s for s in ranked_names if s not in predicted_set]

    # Pinned skills always appear first (if installed)
    ordered: list[tuple[str, int, bool]] = []  # (skill, rank, is_pinned)
    seen: set[str] = set()
    rank = 1
    for s in pinned:
        if s in all_skills and s not in seen:
            ordered.append((s, rank, True))
            seen.add(s)
            rank += 1

    for s in ranked_names:
        if s not in seen and len(ordered) - len(pinned) < top_n:
            ordered.append((s, rank, False))
            seen.add(s)
            rank += 1

    lock_fd = open(LOCK_FILE, "w")
    try:
        # Snapshot already taken above; lock only protects filesystem writes below.
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        _atomic_rebuild(prefix, ordered, all_skills, custom_desc, shortcut_mode, numeric_n)
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        lock_fd.close()


def _is_plugin_installed() -> bool:
    """Return True if skill-habit is installed via 'claude plugins install'."""
    installed = CLAUDE_DIR / "plugins" / "installed_plugins.json"
    if not installed.exists():
        return False
    try:
        data = json.loads(installed.read_text(encoding="utf-8"))
        return "skill-habit@skill-habit" in data.get("plugins", {})
    except Exception:
        return False


def _ensure_plugin_skills() -> None:
    """Create or refresh the skill-habit skills-dir plugin under ~/.claude/skills/skill-habit/.

    Called each rebuild so the plugin stays in sync when the user updates skill-habit.
    For plugin installs (claude plugins install), Claude Code manages skills directly
    from the cached repo — only the dynamic 'quick' skill is written here to avoid
    duplicate skill names (which would cause commands like /skill-habit:server to run twice).
    """
    plugin_installed = _is_plugin_installed()

    # When installed via plugin, omit static skills from the generated dir to prevent
    # duplicate registrations with the plugin cache copy.
    if plugin_installed:
        skills_list = ["./skills/quick"]
        # Clean up any previously written static skills
        for skill_name in _STATIC_SKILLS:
            stale = _PLUGIN_DIR / "skills" / skill_name
            if stale.exists():
                shutil.rmtree(stale)
    else:
        skills_list = ["./skills/quick"] + [f"./skills/{s}" for s in _STATIC_SKILLS]

    plugin_json_content = json.dumps({
        "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
        "name": "skill-habit",
        "version": "0.0.1",
        "description": "skill-habit management skills — quick info, web UI, version, rebuild",
        "author": {"name": "kiss4u"},
        "skills": skills_list,
    }, indent=2, ensure_ascii=False) + "\n"

    meta_dir = _PLUGIN_DIR / ".claude-plugin"
    meta_dir.mkdir(parents=True, exist_ok=True)
    plugin_json = meta_dir / "plugin.json"
    if not plugin_json.exists() or plugin_json.read_text(encoding="utf-8") != plugin_json_content:
        plugin_json.write_text(plugin_json_content, encoding="utf-8")

    if not plugin_installed:
        src_base = _REPO_ROOT / "skills"
        for skill_name in _STATIC_SKILLS:
            src = src_base / skill_name / "SKILL.md"
            if not src.exists():
                continue
            _write_skill_file(_PLUGIN_DIR / "skills" / skill_name, src.read_text(encoding="utf-8"))


def _atomic_rebuild(
    prefix: str,
    ordered: list[tuple[str, int, bool]],
    all_skills: dict[str, dict[str, str]],
    custom_desc: dict[str, str],
    shortcut_mode: str = "both",
    numeric_n: int = 5,
) -> None:
    CLAUDE_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    SKILL_HABIT_DIR.mkdir(parents=True, exist_ok=True)

    prev_generated: list[str] = []
    if GENERATED_MANIFEST.exists():
        try:
            prev_generated = json.loads(GENERATED_MANIFEST.read_text())
        except Exception:
            prev_generated = []

    new_generated: list[str] = []
    shortcut_map: dict[str, str] = {}  # shortcut_name -> real skill_name

    for skill_name, rank, is_pinned in ordered:
        info = all_skills[skill_name]
        desc = custom_desc.get(skill_name, info["description"])
        body = _body_after_frontmatter(info["content"])
        pin_prefix = "📌 " if is_pinned else ""
        display_desc = f"{pin_prefix}{desc or skill_name}"

        entries: list[tuple[str, str, str]] = []
        if shortcut_mode in ("command", "both"):
            sname = f"{prefix}-{skill_name}"
            entries.append((sname, display_desc, f"{prefix}-{_safe_dir_name(skill_name)}"))
        if shortcut_mode in ("numeric", "both") and rank <= numeric_n:
            # Repeat the rank digit N times: n1(2), n22(3), n333(4)...
            # Strictly increasing lengths guarantee dropdown order matches frequency rank.
            sname = f"{prefix}{str(rank) * rank}"
            pin_mid = "📌" if is_pinned else ""
            numeric_desc = f"/{skill_name} {pin_mid}📊" + (f" {desc}" if desc else "")
            entries.append((sname, numeric_desc, sname))

        for shortcut_name, display_desc, dir_name in entries:
            content = f"---\nname: {shortcut_name}\ndescription: {display_desc}\n---\n\n{body}\n"
            _atomic_write_skill(CLAUDE_SKILLS_DIR / dir_name, content)
            new_generated.append(dir_name)
            shortcut_map[dir_name] = skill_name

    # Ensure plugin skills are installed and up-to-date, then refresh the dynamic quick skill
    _ensure_plugin_skills()
    _write_skill_file(_QUICK_SKILL_DIR, _QUICK_SKILL_CONTENT)
    shortcut_map["_prefix"] = prefix  # stored so resolver can strip command shortcuts without reading config

    # Remove previously generated dirs that are no longer in this batch
    stale = set(prev_generated) - set(new_generated)
    for dir_name in stale:
        stale_dir = CLAUDE_SKILLS_DIR / dir_name
        if stale_dir.exists():
            shutil.rmtree(stale_dir)

    GENERATED_MANIFEST.write_text(json.dumps(new_generated, indent=2))

    # Write shortcut -> real skill mapping for use by the recorder
    SHORTCUT_MAP.write_text(json.dumps(shortcut_map, indent=2, ensure_ascii=False))

    # Accumulate all ever-generated names so stats can exclude historical shortcuts
    ever: list[str] = []
    if EVER_GENERATED_MANIFEST.exists():
        try:
            ever = json.loads(EVER_GENERATED_MANIFEST.read_text())
        except Exception:
            ever = []
    ever_set = set(ever) | set(new_generated)
    EVER_GENERATED_MANIFEST.write_text(json.dumps(sorted(ever_set), indent=2))


def clear() -> None:
    """Remove all generated shortcut skills and reset the manifest."""
    if GENERATED_MANIFEST.exists():
        dirs = json.loads(GENERATED_MANIFEST.read_text())
        for d in dirs:
            p = CLAUDE_SKILLS_DIR / d
            if p.exists():
                shutil.rmtree(p)
        GENERATED_MANIFEST.unlink()
    # Remove the static plugin skills dir unless it IS the repo (method-B install to ~/.claude/skills/)
    if _PLUGIN_DIR.exists() and _PLUGIN_DIR.resolve() != _REPO_ROOT.resolve():
        shutil.rmtree(_PLUGIN_DIR)


if __name__ == "__main__":
    import argparse as _ap
    _p = _ap.ArgumentParser()
    _p.add_argument("--clear", action="store_true", help="Remove all generated skills")
    _args = _p.parse_args()
    if _args.clear:
        cfg = load_config()
        clear()
    else:
        generate()
