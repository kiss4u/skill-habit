#!/usr/bin/env python3
"""
skill-habit management UI server.
Starts on-demand, serves the UI, exits cleanly after the user closes the tab
or after IDLE_TIMEOUT seconds of no requests.
"""
from __future__ import annotations
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, Request
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import load as load_config, save as save_config, LOG_FILE
from core.cache import rebuild as rebuild_cache, load as load_cache
from core import analyzer
from adapters.claude_code.skill_generator import generate as generate_shortcuts

_REPO_ROOT = Path(__file__).parent.parent

# --- H-06: TTL cache for _check_update() ---
_update_cache: dict = {}
_update_cache_ts: float = 0.0
_UPDATE_TTL = 3600.0

# --- H-03: mtime-guarded cache for scan_all_skills() ---
_skills_cache: dict = {}
_skills_cache_mtime: float = 0.0


def _cached_scan_all_skills() -> dict:
    global _skills_cache, _skills_cache_mtime
    from adapters.claude_code.skill_generator import scan_all_skills
    skills_dir = Path.home() / ".claude" / "skills"
    try:
        mtime = skills_dir.stat().st_mtime if skills_dir.exists() else 0.0
    except OSError:
        mtime = 0.0
    if _skills_cache and mtime == _skills_cache_mtime:
        return _skills_cache
    _skills_cache = scan_all_skills()
    _skills_cache_mtime = mtime
    return _skills_cache


def _enrich_config(config: dict) -> dict:
    """Add runtime-computed exclusion sets before building cache."""
    if config.get("commands_generate_shortcuts", True):
        return config
    cmd_dir = str(Path.home() / ".claude" / "commands") + "/"
    cmd_skills = [
        name for name, info in _cached_scan_all_skills().items()
        if info.get("source_path", "").startswith(cmd_dir)
    ]
    return {**config, "_exclude_skills": cmd_skills}


def _get_command_groups() -> list:
    """Group ~/.claude/commands/ .md files by namespace."""
    all_skills = _cached_scan_all_skills()
    commands_base = Path.home() / ".claude" / "commands"
    commands_str = str(commands_base) + "/"
    groups: dict = {}
    for skill_name, info in all_skills.items():
        source_str = info.get("source_path", "")
        if not source_str or not source_str.startswith(commands_str):
            continue
        ns = skill_name.split(":")[0] if ":" in skill_name else "_root"
        group_id = f"commands:{ns}"
        if group_id not in groups:
            groups[group_id] = {
                "id": group_id,
                "name": ns if ns != "_root" else "(root)",
                "commands": [],
            }
        groups[group_id]["commands"].append({
            "name": skill_name,
            "description": info.get("description", ""),
        })
    for g in groups.values():
        g["commands"].sort(key=lambda c: c["name"])
    return sorted(groups.values(), key=lambda g: g["name"])


def _get_skill_groups() -> list:
    """Group installed skills by their source plugin/package."""
    all_skills = _cached_scan_all_skills()

    from core.config import GENERATED_MANIFEST
    generated: set = set()
    if GENERATED_MANIFEST.exists():
        try:
            generated |= set(json.loads(GENERATED_MANIFEST.read_text()))
        except Exception:
            pass

    plugin_cache_base = Path.home() / ".claude" / "plugins" / "cache"
    claude_skills_base = Path.home() / ".claude" / "skills"
    plugin_cache_str = str(plugin_cache_base) + "/"
    claude_skills_str = str(claude_skills_base) + "/"

    groups: dict = {}
    for skill_name, info in all_skills.items():
        if info.get("dir_slug", "") in generated:
            continue
        source_str = info.get("source_path", "")
        if not source_str:
            continue
        source = Path(source_str)
        skill_detail = {
            "name": skill_name,
            "description": info.get("description", ""),
            "skill_path": str(source.parent),
        }

        if source_str.startswith(plugin_cache_str):
            try:
                rel = source.relative_to(plugin_cache_base)
                parts = rel.parts
                if len(parts) >= 3:
                    publisher, plugin_name, version = parts[0], parts[1], parts[2]
                    group_id = f"{publisher}/{plugin_name}/{version}"
                    if group_id not in groups:
                        groups[group_id] = {
                            "id": group_id,
                            "name": f"{publisher}/{plugin_name}",
                            "version": version,
                            "type": "plugin",
                            "uninstall_path": str(plugin_cache_base / publisher / plugin_name / version),
                            "skills": [],
                        }
                    groups[group_id]["skills"].append(skill_detail)
            except ValueError:
                pass
        elif source_str.startswith(claude_skills_str):
            try:
                rel = source.relative_to(claude_skills_base)
                parts = rel.parts
                if len(parts) >= 4 and parts[1] == "skills":
                    group_dir = parts[0]
                    if group_dir == "skill-habit":
                        continue
                    group_id = f"local:{group_dir}"
                    if group_id not in groups:
                        groups[group_id] = {
                            "id": group_id,
                            "name": group_dir,
                            "version": "",
                            "type": "local",
                            "uninstall_path": str(claude_skills_base / group_dir),
                            "skills": [],
                        }
                    groups[group_id]["skills"].append(skill_detail)
                elif len(parts) == 2:
                    # Standalone skill: ~/.claude/skills/<skill-dir>/SKILL.md
                    skill_dir = parts[0]
                    group_id = f"standalone:{skill_dir}"
                    groups[group_id] = {
                        "id": group_id,
                        "name": skill_name,
                        "version": "",
                        "type": "skill",
                        "uninstall_path": str(claude_skills_base / skill_dir),
                        "skills": [skill_detail],
                    }
            except ValueError:
                pass

    return sorted(groups.values(), key=lambda g: (g["type"], g["name"]))


def _local_version() -> str:
    pyproject = _REPO_ROOT / "pyproject.toml"
    if pyproject.exists():
        for line in pyproject.read_text().splitlines():
            if line.strip().startswith("version"):
                return line.split("=", 1)[1].strip().strip('"\'')
    return "unknown"

def _parse_semver(v: str) -> tuple:
    """Parse 'X.Y.Z' into (X, Y, Z). Returns (0,0,0) on failure."""
    try:
        parts = v.strip().split(".")
        return (int(parts[0]), int(parts[1]), int(parts[2].split("-")[0]))
    except Exception:
        return (0, 0, 0)

def _parse_changelog_notes(content: str, version: str) -> str:
    """Extract the changelog section for a specific version."""
    lines = content.splitlines()
    in_section = False
    notes: list[str] = []
    for line in lines:
        if re.match(rf"^## \[{re.escape(version)}\]", line):
            in_section = True
            continue
        if in_section:
            if line.startswith("## ["):
                break
            notes.append(line)
    return "\n".join(notes).strip()


def _update_level(current: str, remote: str) -> str | None:
    """Return 'major' (强更), 'patch' (弱更), or None (no update)."""
    if not remote or remote == "unknown" or remote == current:
        return None
    lv, rv = _parse_semver(current), _parse_semver(remote)
    if rv <= lv:
        return None  # remote is not newer
    if rv[0] > lv[0] or rv[1] > lv[1]:
        return "major"  # major or minor bump → 强更
    return "patch"  # patch only → 弱更

def _check_update() -> dict:
    """Return {current, latest, has_update, update_level, commits_ahead, upgrade_cmd, error?}"""
    global _update_cache, _update_cache_ts
    if _update_cache and time.time() - _update_cache_ts < _UPDATE_TTL:
        return _update_cache
    current = _local_version()
    repo_dir = str(_REPO_ROOT)
    try:
        subprocess.run(["git", "-C", repo_dir, "fetch", "origin", "--quiet"],
                       capture_output=True, timeout=10)
        ahead_result = subprocess.run(
            ["git", "-C", repo_dir, "log", "HEAD..origin/main", "--oneline"],
            capture_output=True, text=True, timeout=5)
        ahead = [l for l in ahead_result.stdout.strip().splitlines() if l]
        remote_v = current
        notes = ""
        try:
            req = Request("https://raw.githubusercontent.com/kiss4u/skill-habit/main/pyproject.toml",
                          headers={"User-Agent": "skill-habit-updater"})
            raw = urlopen(req, timeout=8).read().decode()
            for line in raw.splitlines():
                if line.strip().startswith("version"):
                    remote_v = line.split("=", 1)[1].strip().strip('"\'')
                    break
        except Exception:
            pass
        if remote_v and remote_v != current:
            try:
                req = Request("https://raw.githubusercontent.com/kiss4u/skill-habit/main/CHANGELOG.md",
                              headers={"User-Agent": "skill-habit-updater"})
                changelog_raw = urlopen(req, timeout=8).read().decode()
                notes = _parse_changelog_notes(changelog_raw, remote_v)
            except Exception:
                pass
        level = _update_level(current, remote_v)
        is_git = (Path(repo_dir) / ".git").exists()
        if is_git:
            upgrade_cmd = f"git -C {repo_dir} pull && python3 {repo_dir}/adapters/claude_code/skill_generator.py"
        elif shutil.which("skill-habit"):
            upgrade_cmd = "skill-habit install"
        else:
            upgrade_cmd = "claude plugins update skill-habit@skill-habit"
        result = {"current": current, "latest": remote_v or current,
                  "has_update": level is not None, "update_level": level,
                  "commits_ahead": len(ahead), "upgrade_cmd": upgrade_cmd,
                  "notes": notes}
        _update_cache = result
        _update_cache_ts = time.time()
        return result
    except Exception as e:
        result = {"current": current, "latest": current,
                  "has_update": False, "update_level": None, "error": str(e), "notes": ""}
        _update_cache = result
        _update_cache_ts = time.time()
        return result

UI_DIR = Path(__file__).parent
PORT_FILE = Path.home() / ".skill-habit" / "ui.port"
IDLE_TIMEOUT = 300  # seconds — server exits if idle this long


# --- M-10: helper to safely parse integer query params ---
def _int_param(qs: dict, key: str, default: int) -> int:
    try:
        return int(qs.get(key, [str(default)])[0])
    except (ValueError, IndexError):
        raise ValueError(key)


class Handler(BaseHTTPRequestHandler):
    _last_request = time.time()  # safe under single-threaded HTTPServer; would need a lock with ThreadingMixIn
    _shutdown_event: threading.Event

    def do_GET(self) -> None:
        Handler._last_request = time.time()
        parsed = urlparse(self.path)

        if parsed.path == "/" or parsed.path == "/index.html":
            self._serve_file(UI_DIR / "index.html", "text/html")
        elif parsed.path.startswith("/api/"):
            self._handle_api_get(parsed)
        elif parsed.path == "/locales/bundle.js":
            self._serve_locale_bundle()
        elif parsed.path.startswith("/tabs/") or parsed.path.startswith("/cards/") or parsed.path.startswith("/locales/"):
            rel = parsed.path.lstrip("/")
            self._serve_file(UI_DIR / rel, "application/javascript")
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        Handler._last_request = time.time()
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        self._handle_api_post(parsed, data)

    def _handle_api_get(self, parsed: any) -> None:
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/api/config":
            self._json(load_config())
        elif path == "/api/cache":
            tw = qs.get("time_window", [None])[0]
            if tw:
                cached = load_cache()
                log_mtime = LOG_FILE.stat().st_mtime if LOG_FILE.exists() else 0
                if (cached and cached.get("time_window") == tw
                        and time.time() - cached.get("built_at", 0) < 60
                        and log_mtime <= cached.get("built_at", 0)):
                    self._json(cached)
                else:
                    config = load_config()
                    config["time_window"] = tw
                    cache = rebuild_cache(_enrich_config(config))
                    self._json(cache)
            else:
                cache = load_cache()
                if cache is None:
                    config = load_config()
                    cache = rebuild_cache(_enrich_config(config))
                self._json(cache)
        elif path == "/api/stats":
            tw = qs.get("time_window", ["all"])[0]
            from core.config import EVER_GENERATED_MANIFEST, GENERATED_MANIFEST
            generated: set[str] = set()
            for mf in (GENERATED_MANIFEST, EVER_GENERATED_MANIFEST):
                if mf.exists():
                    try:
                        generated |= set(json.loads(mf.read_text()))
                    except Exception:
                        pass
            _cfg = load_config()
            bl: set[str] = set(_cfg.get("blacklist", []))
            _excl_self = _cfg.get("exclude_self_tracking", True)
            self._json(analyzer.total_stats(tw, exclude_skills=generated | bl,
                                            exclude_prefix="skill-habit:" if _excl_self else None))
        elif path == "/api/blacklist":
            config = load_config()
            bl_list = config.get("blacklist", [])
            try:
                page     = _int_param(qs, "page",     1)
                per_page = _int_param(qs, "per_page", 20)
            except ValueError:
                self.send_error(400, "Invalid parameter")
                return
            all_skills = _cached_scan_all_skills()
            custom_desc = config.get("custom_descriptions", {})
            items = []
            for name in bl_list:
                info = all_skills.get(name, {})
                items.append({
                    "name": name,
                    "description": custom_desc.get(name, "") or info.get("description", ""),
                })
            total = len(items)
            start = (page - 1) * per_page
            self._json({"total": total, "page": page, "per_page": per_page,
                        "items": items[start:start + per_page]})
        elif path == "/api/top-skills":
            tw = qs.get("time_window", ["all"])[0]
            try:
                n = _int_param(qs, "n", 20)
            except ValueError:
                self.send_error(400, "Invalid parameter: n")
                return
            from core.config import EVER_GENERATED_MANIFEST, GENERATED_MANIFEST
            _generated: set[str] = set()
            for _mf in (GENERATED_MANIFEST, EVER_GENERATED_MANIFEST):
                if _mf.exists():
                    try:
                        _generated |= set(json.loads(_mf.read_text()))
                    except Exception:
                        pass
            _bl2: set[str] = set(load_config().get("blacklist", []))
            _excl_self2 = load_config().get("exclude_self_tracking", True)
            self._json(analyzer.top_skills(tw, n, exclude_skills=_generated | _bl2,
                                           exclude_prefix="skill-habit:" if _excl_self2 else None))
        elif path == "/api/heatmap":
            try:
                weeks = _int_param(qs, "weeks", 26)
            except ValueError:
                self.send_error(400, "Invalid parameter: weeks")
                return
            self._json(analyzer.heatmap_data(weeks))
        elif path == "/api/skills":
            try:
                page     = _int_param(qs, "page",     1)
            except ValueError:
                self.send_error(400, "Invalid parameter: page")
                return
            try:
                per_page = _int_param(qs, "per_page", 20)
            except ValueError:
                self.send_error(400, "Invalid parameter: per_page")
                return
            sort     = qs.get("sort", ["count"])[0]   # count | name | last_used
            q        = qs.get("q",    [""])[0].lower()

            config      = load_config()
            pinned      = config.get("pinned_skills", [])
            custom_desc = config.get("custom_descriptions", {})
            prefix      = config.get("prefix", "sh")
            exc_prefix  = f"{prefix}-"
            manage_name = f"{prefix}-manage"
            def _is_shortcut(s: str) -> bool:
                return s.startswith(exc_prefix) or (s.startswith(prefix) and s[len(prefix):][:1].isdigit())

            all_skills   = _cached_scan_all_skills()
            from core.config import EVER_GENERATED_MANIFEST, GENERATED_MANIFEST
            _generated: set[str] = set()
            for _mf in (GENERATED_MANIFEST, EVER_GENERATED_MANIFEST):
                if _mf.exists():
                    try:
                        _generated |= set(json.loads(_mf.read_text()))
                    except Exception:
                        pass
            _excl_self_s = config.get("exclude_self_tracking", True)
            stats_map    = {r["skill"]: r["count"] for r in analyzer.top_skills(
                                "all", n=9999,
                                exclude_prefix="skill-habit:" if _excl_self_s else None)
                            if r["skill"] not in _generated}
            last_used_map = analyzer.last_used_per_skill()

            skills_list = []
            for name, info in all_skills.items():
                if _is_shortcut(name) or name == prefix or name == manage_name:
                    continue
                orig_desc   = info["description"]
                custom      = custom_desc.get(name, "")
                desc        = custom or orig_desc
                if q and q not in name.lower() and q not in desc.lower():
                    continue
                src = info.get("source_path", "")
                try:
                    if src:
                        st = Path(src).stat()
                        install_time = getattr(st, 'st_birthtime', st.st_mtime)
                    else:
                        install_time = 0
                except OSError:
                    install_time = 0
                skills_list.append({
                    "name":                name,
                    "description":         desc,
                    "original_description": orig_desc,
                    "custom_description":  custom,
                    "count":               stats_map.get(name, 0),
                    "last_used":           last_used_map.get(name, 0),
                    "install_time":        install_time,
                    "is_pinned":           name in pinned,
                    "pin_order":           pinned.index(name) if name in pinned else -1,
                })

            sort_dir = qs.get("sort_dir", ["desc"])[0]
            rev = (sort_dir == "desc")

            pinned_items   = sorted([s for s in skills_list if s["is_pinned"]], key=lambda x: x["pin_order"])
            unpinned_items = [s for s in skills_list if not s["is_pinned"]]

            if sort == "name":
                unpinned_items.sort(key=lambda x: x["name"], reverse=rev)
            elif sort == "last_used":
                unpinned_items.sort(key=lambda x: (x["last_used"], x["name"]), reverse=rev)
            else:
                unpinned_items.sort(key=lambda x: (x["count"], x["name"]), reverse=rev)

            skills_list = pinned_items + unpinned_items

            total    = len(skills_list)
            start    = (page - 1) * per_page
            self._json({"total": total, "page": page, "per_page": per_page,
                        "skills": skills_list[start:start + per_page]})
        elif path == "/api/transitions":
            tw = qs.get("time_window", ["all"])[0]
            _excl_t = load_config().get("exclude_self_tracking", True)
            self._json(analyzer.transition_matrix(tw, exclude_prefix="skill-habit:" if _excl_t else None))
        elif path == "/api/hourly":
            tw = qs.get("time_window", ["all"])[0]
            self._json(analyzer.hourly_distribution(tw))
        elif path == "/api/weekday":
            tw = qs.get("time_window", ["all"])[0]
            self._json(analyzer.weekday_distribution(tw))
        elif path == "/api/version":
            self._json(_check_update())
        elif path == "/api/check-prefix":
            from core.config import get_all_command_names, suggest_prefix as _suggest
            new_prefix = qs.get("prefix", [""])[0].strip()
            if not new_prefix:
                self._json({"conflicts": [], "suggestions": []})
                return
            config = load_config()
            cur = config.get("prefix", "sh")
            all_cmds = get_all_command_names(cur_prefix=cur if new_prefix != cur else None)
            # Collect conflicts: commands that start with new_prefix (excluding own shortcuts)
            new_exc = f"{new_prefix}-"
            def _is_own_new(name: str) -> bool:
                return (
                    name.startswith(new_exc)
                    or (name.startswith(new_prefix) and len(name) > len(new_prefix) and name[len(new_prefix)].isdigit())
                    or name == new_prefix
                    or name == f"{new_prefix}-manage"
                    or name == f"{new_prefix}_manage"
                )
            conflict_details: list[dict] = []
            for src in ("builtin", "skill", "plugin", "plugin_skill"):
                for name in all_cmds.get(src, []):
                    if name.startswith(new_prefix) and not _is_own_new(name):
                        conflict_details.append({"name": name, "type": src})
            suggestions = _suggest(cur_prefix=new_prefix if not conflict_details else cur, n=5)
            self._json({
                "conflicts": [c["name"] for c in conflict_details],
                "conflict_details": conflict_details,
                "suggestions": suggestions,
            })
        elif path == "/api/prefix-suggestions":
            from core.config import suggest_prefix as _suggest
            config = load_config()
            cur = config.get("prefix", "sh")
            self._json({"suggestions": _suggest(cur_prefix=cur, n=8)})
        elif path == "/api/commands":
            self._json({"groups": _get_command_groups()})
        elif path == "/api/skill-groups":
            self._json({"groups": _get_skill_groups()})
        else:
            self.send_error(404)

    def _handle_api_post(self, parsed: any, data: dict) -> None:
        path = parsed.path

        if path == "/api/config":
            config = load_config()
            config.update(data)
            save_config(config)
            # Rebuild shortcuts immediately so current session reflects changes
            generate_shortcuts(config)
            rebuild_cache(_enrich_config(config))
            self._json({"ok": True})
        elif path == "/api/blacklist/add":
            name = data.get("skill", "").strip()
            if name:
                config = load_config()
                bl = list(config.get("blacklist", []))
                if name not in bl:
                    bl.append(name)
                    config["blacklist"] = bl
                    save_config(config)
                    generate_shortcuts(config)
            self._json({"ok": True})
        elif path == "/api/blacklist/remove":
            name = data.get("skill", "").strip()
            if name:
                config = load_config()
                bl = list(config.get("blacklist", []))
                if name in bl:
                    bl.remove(name)
                    config["blacklist"] = bl
                    save_config(config)
                    generate_shortcuts(config)
            self._json({"ok": True})
        elif path == "/api/config/reset":
            from core.config import DEFAULT_CONFIG, CONFIG_FILE
            import copy
            defaults = copy.deepcopy(DEFAULT_CONFIG)
            save_config(defaults)
            generate_shortcuts(defaults)
            rebuild_cache(_enrich_config(defaults))
            self._json(defaults)
        elif path == "/api/logs/clear":
            count = analyzer.clear_log()
            generate_shortcuts(load_config())  # re-rank shortcuts against empty log
            self._json({"ok": True, "removed": count})
        elif path == "/api/logs/trim":
            days = int(data.get("days", 30))
            count = analyzer.trim_log(days)
            generate_shortcuts(load_config())
            self._json({"ok": True, "removed": count})
        elif path == "/api/upgrade":
            cached = _update_cache
            cmd = cached.get("upgrade_cmd", "") if cached else ""
            if not cmd:
                self._json({"ok": False, "error": "No upgrade command available — check for updates first"})
                return
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    _update_cache.clear()  # force fresh check next /api/version call
                self._json({"ok": result.returncode == 0,
                            "stdout": result.stdout, "stderr": result.stderr})
            except subprocess.TimeoutExpired:
                self._json({"ok": False, "error": "Upgrade timed out after 120s"})
            except Exception as e:
                self._json({"ok": False, "error": str(e)})
        elif path == "/api/skill-groups/uninstall":
            uninstall_path = data.get("uninstall_path", "").strip()
            group_id = data.get("group_id", "").strip()
            skill_name_only = data.get("skill_name", "").strip()  # individual skill uninstall
            safe_prefixes = [
                str(Path.home() / ".claude" / "plugins" / "cache") + "/",
                str(Path.home() / ".claude" / "skills") + "/",
            ]
            if not uninstall_path:
                self._json({"ok": False, "error": "Missing uninstall_path"})
                return
            if not any(uninstall_path.startswith(p) for p in safe_prefixes):
                self._json({"ok": False, "error": "Path not in allowed directory"})
                return
            p = Path(uninstall_path)
            if not p.exists():
                self._json({"ok": False, "error": "Path does not exist"})
                return
            # Collect which skill names will be removed before deleting
            if skill_name_only:
                skills_to_remove: set = {skill_name_only}
            else:
                skills_to_remove = set()
                for g in _get_skill_groups():
                    if g["id"] == group_id or g["uninstall_path"] == uninstall_path:
                        for s in g["skills"]:
                            skills_to_remove.add(s["name"] if isinstance(s, dict) else s)
            try:
                shutil.rmtree(p)
                # Clean up config: remove uninstalled skills from pinned, blacklist, custom_descriptions
                if skills_to_remove:
                    config = load_config()
                    changed = False
                    pinned = config.get("pinned_skills", [])
                    new_pinned = [s for s in pinned if s not in skills_to_remove]
                    if new_pinned != pinned:
                        config["pinned_skills"] = new_pinned
                        changed = True
                    blacklist = config.get("blacklist", [])
                    new_blacklist = [s for s in blacklist if s not in skills_to_remove]
                    if new_blacklist != blacklist:
                        config["blacklist"] = new_blacklist
                        changed = True
                    custom_desc = config.get("custom_descriptions", {})
                    new_custom = {k: v for k, v in custom_desc.items() if k not in skills_to_remove}
                    if len(new_custom) != len(custom_desc):
                        config["custom_descriptions"] = new_custom
                        changed = True
                    if changed:
                        save_config(config)
                generate_shortcuts(load_config())
                rebuild_cache(_enrich_config(load_config()))
                self._json({"ok": True, "removed_skills": list(skills_to_remove)})
            except Exception as e:
                self._json({"ok": False, "error": str(e)})
        elif path == "/api/shutdown":
            self._json({"ok": True})
            threading.Thread(target=self._do_shutdown, daemon=True).start()
        else:
            self.send_error(404)

    def _do_shutdown(self) -> None:
        time.sleep(0.2)
        Handler._shutdown_event.set()

    def _serve_locale_bundle(self) -> None:
        locales_dir = UI_DIR / "locales"
        parts = []
        for f in sorted(locales_dir.glob("*.js")):
            try:
                parts.append(f.read_text(encoding="utf-8"))
            except OSError:
                pass
        body = "\n".join(parts).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/javascript")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self.send_error(404)
            return
        content = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _json(self, data: any) -> None:
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: any) -> None:
        pass  # suppress request logs


def _idle_watchdog(server: HTTPServer, shutdown_event: threading.Event) -> None:
    while not shutdown_event.is_set():
        time.sleep(10)
        if time.time() - Handler._last_request > IDLE_TIMEOUT:
            shutdown_event.set()
    server.shutdown()


def run(port: int = 0, open_browser: bool = True) -> None:
    shutdown_event = threading.Event()
    Handler._shutdown_event = shutdown_event

    try:
        server = HTTPServer(("127.0.0.1", port), Handler)
    except OSError:
        server = HTTPServer(("127.0.0.1", 0), Handler)
    actual_port = server.server_address[1]

    PORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    PORT_FILE.write_text(str(actual_port))

    rebuild_cache(_enrich_config(load_config()))

    print(f"skill-habit UI: http://127.0.0.1:{actual_port}")

    threading.Thread(target=_idle_watchdog, args=(server, shutdown_event), daemon=True).start()

    if open_browser:
        threading.Timer(0.3, lambda: webbrowser.open(f"http://127.0.0.1:{actual_port}")).start()

    try:
        server.serve_forever()
    finally:
        if PORT_FILE.exists():
            PORT_FILE.unlink()
        print("skill-habit UI closed.")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=0)
    p.add_argument("--no-browser", action="store_true")
    args = p.parse_args()
    run(port=args.port, open_browser=not args.no_browser)
