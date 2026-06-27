from __future__ import annotations
import fcntl
import hashlib
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import LOCK_FILE, LOG_FILE, SCHEMA_VERSION, SHORTCUT_MAP, SKILL_HABIT_DIR

def _read_project_version() -> str:
    try:
        pyproject = Path(__file__).parent.parent / "pyproject.toml"
        for line in pyproject.read_text().splitlines():
            if line.strip().startswith("version"):
                return line.split("=", 1)[1].strip().strip("\"'")
    except Exception:
        pass
    return "unknown"

ADAPTER_VERSION = _read_project_version()


def _resolve_skill(skill: str) -> str:
    """Resolve a generated shortcut to the underlying real skill name.

    Command shortcuts (sh-git-smart): strip prefix directly — no map needed.
    Numeric shortcuts (sh-1): look up the shortcut map.
    """
    # Fast-path: namespaced skills (contain ":") are never shortcuts
    if ":" in skill:
        return skill
    if not SHORTCUT_MAP.exists():
        return skill
    try:
        mapping = json.loads(SHORTCUT_MAP.read_text())
    except Exception:
        return skill
    prefix = mapping.get("_prefix", "")
    if not prefix:
        return skill
    # Numeric shortcut: sh1-name, sh2-name, … (legacy plain sh1/sh2 also matched)
    if skill.startswith(prefix) and skill[len(prefix):][:1].isdigit():
        return mapping.get(skill, skill)
    # Command shortcut: sh-git-smart → git-smart; sh-manage stays as-is
    if skill.startswith(f"{prefix}-"):
        remainder = skill[len(prefix) + 1:]
        return mapping.get(skill, skill) if remainder != "manage" else skill
    return skill


def record(
    skill: str,
    *,
    platform: str,
    session_id: str,
    session_seq: int,
    args_len: int = 0,
    invoke_by: str = "user",
    cwd: str | None = None,
) -> None:
    """Append one skill invocation to the log. Non-blocking: drops silently if lock busy."""
    SKILL_HABIT_DIR.mkdir(parents=True, exist_ok=True)
    skill = _resolve_skill(skill)
    entry = _build_entry(skill, platform, session_id, session_seq, args_len, invoke_by, cwd)
    _append_locked(entry)


def _build_entry(
    skill: str,
    platform: str,
    session_id: str,
    session_seq: int,
    args_len: int,
    invoke_by: str,
    cwd: str | None,
) -> dict[str, Any]:
    ns = skill.split(":")[0] if ":" in skill else skill
    now = datetime.now()
    return {
        "v": SCHEMA_VERSION,
        "ts": int(time.time()),
        "skill": skill,
        "ns": ns,
        "platform": platform,
        "invoke_by": invoke_by,
        "hour": now.hour,
        "weekday": now.weekday(),
        "session_id": session_id,
        "session_skill_seq": session_seq,
        "project_hash": _project_hash(cwd),
        "args_len": args_len,
        "adapter_version": ADAPTER_VERSION,
    }


def _append_locked(entry: dict[str, Any]) -> None:
    try:
        lock_fd = open(LOCK_FILE, "w")
    except OSError:
        return  # can't obtain lock file; drop silently
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)  # blocking: wait instead of dropping
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass
    finally:
        lock_fd.close()  # flock released implicitly on close


def _project_hash(cwd: str | None) -> str:
    path = cwd or os.getcwd()
    return hashlib.md5(path.encode()).hexdigest()[:6]


def migrate(dry_run: bool = False) -> int:
    """
    Backfill missing fields in old log entries using schema-version defaults.
    Writes to a new file then atomically replaces the original.
    Returns number of entries migrated.
    """
    if not LOG_FILE.exists():
        return 0

    defaults_by_version: dict[int, dict[str, Any]] = {
        1: {
            "v": 1,
            "invoke_by": "user",
            "hour": 0,
            "weekday": 0,
            "session_skill_seq": 0,
            "project_hash": "unknown",
            "args_len": 0,
            "adapter_version": "0.0.0",
        }
    }

    migrated = 0
    out_lines: list[str] = []

    with open(LOG_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                out_lines.append(line)
                continue

            v = entry.get("v", 1)
            defaults = defaults_by_version.get(v, {})
            changed = False
            for key, default in defaults.items():
                if key not in entry:
                    entry[key] = default
                    changed = True
            if changed:
                migrated += 1
            out_lines.append(json.dumps(entry, ensure_ascii=False))

    if not dry_run and migrated > 0:
        tmp = LOG_FILE.with_suffix(".log.migrate_tmp")
        tmp.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        tmp.replace(LOG_FILE)

    return migrated
