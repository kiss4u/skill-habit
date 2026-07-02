from __future__ import annotations
import json
import os
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import LOG_FILE

_SECONDS_PER_DAY = 86_400


def _load_entries(time_window: str = "all", since_ts: float = 0) -> list[dict[str, Any]]:
    if not LOG_FILE.exists():
        return []
    cutoff = _cutoff_ts(time_window)
    effective_cutoff = max(cutoff or 0, since_ts)
    entries: list[dict[str, Any]] = []
    with open(LOG_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if effective_cutoff == 0 or entry.get("ts", 0) >= effective_cutoff:
                entries.append(entry)
    return entries


def _cutoff_ts(time_window: str) -> int | None:
    now = time.time()
    if time_window == "today":
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return int(today.timestamp())
    if time_window == "week":
        return int(now - 7 * _SECONDS_PER_DAY)
    if time_window == "month":
        return int(now - 30 * _SECONDS_PER_DAY)
    if time_window == "halfyear":
        return int(now - 180 * _SECONDS_PER_DAY)
    return None


def top_skills(time_window: str = "all", n: int = 10, exclude_skills: set | None = None, exclude_prefix: str | None = None) -> list[dict[str, Any]]:
    entries = _load_entries(time_window)
    counts: Counter[str] = Counter(
        e["skill"] for e in entries
        if "skill" in e
        and not (exclude_skills and e["skill"] in exclude_skills)
        and not (exclude_prefix and e["skill"].startswith(exclude_prefix))
    )
    return [{"skill": s, "count": c} for s, c in counts.most_common(n)]


def last_used_per_skill() -> dict[str, int]:
    """Return {skill: latest_timestamp} for every skill ever logged."""
    entries = _load_entries("all")
    last: dict[str, int] = {}
    for e in entries:
        skill = e.get("skill")
        ts = e.get("ts", 0)
        if skill and ts > last.get(skill, 0):
            last[skill] = ts
    return last


def transition_matrix(time_window: str = "all", exclude_prefix: str | None = None) -> dict[str, dict[str, int]]:
    """Build a Markov chain: {skill_a: {skill_b: count}} from session sequences."""
    entries = _load_entries(time_window)
    sessions: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for e in entries:
        sid = e.get("session_id", "")
        seq = e.get("session_skill_seq", 0)
        skill = e.get("skill", "")
        if skill and not (exclude_prefix and skill.startswith(exclude_prefix)):
            sessions[sid].append((seq, skill))

    matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for seq_list in sessions.values():
        ordered = [skill for _, skill in sorted(seq_list)]
        for i in range(len(ordered) - 1):
            matrix[ordered[i]][ordered[i + 1]] += 1

    return {k: dict(v) for k, v in matrix.items()}


def predict_next(current_skill: str, time_window: str = "all", n: int = 3) -> list[str]:
    """Return up to n most likely next skills after current_skill."""
    matrix = transition_matrix(time_window)
    transitions = matrix.get(current_skill, {})
    if not transitions:
        return []
    return [s for s, _ in sorted(transitions.items(), key=lambda x: -x[1])[:n]]


def heatmap_data(weeks: int = 26) -> list[dict[str, Any]]:
    cutoff = int(time.time()) - weeks * 7 * _SECONDS_PER_DAY
    entries = _load_entries("all", since_ts=cutoff)
    day_counts: Counter[str] = Counter()
    for e in entries:
        date_str = datetime.fromtimestamp(e["ts"]).strftime("%Y-%m-%d")
        day_counts[date_str] += 1
    return [{"date": d, "count": c} for d, c in sorted(day_counts.items())]


def hourly_distribution(time_window: str = "all") -> list[dict[str, Any]]:
    entries = _load_entries(time_window)
    hour_counts: Counter[int] = Counter(e.get("hour", 0) for e in entries)
    return [{"hour": h, "count": hour_counts.get(h, 0)} for h in range(24)]


def weekday_distribution(time_window: str = "all") -> list[dict[str, Any]]:
    entries = _load_entries(time_window)
    day_counts: Counter[int] = Counter(e.get("weekday", 0) for e in entries)
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return [{"day": day_names[d], "weekday": d, "count": day_counts.get(d, 0)} for d in range(7)]


def trim_log(retention_days: int) -> int:
    """Delete log entries older than retention_days. Returns number of entries removed."""
    if retention_days <= 0 or not LOG_FILE.exists():
        return 0
    cutoff = time.time() - retention_days * _SECONDS_PER_DAY
    kept: list[str] = []
    removed = 0
    with open(LOG_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get("ts", 0) >= cutoff:
                    kept.append(line)
                else:
                    removed += 1
            except Exception:
                kept.append(line)
    if removed:
        tmp = Path(str(LOG_FILE) + ".tmp")
        tmp.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
        os.replace(tmp, LOG_FILE)
    return removed


def clear_log() -> int:
    """Delete all log entries. Returns number of entries removed."""
    if not LOG_FILE.exists():
        return 0
    with open(LOG_FILE) as f:
        count = sum(1 for line in f if line.strip())
    LOG_FILE.write_text("", encoding="utf-8")
    return count


def total_stats(time_window: str = "all", exclude_skills: set | None = None, exclude_prefix: str | None = None) -> dict[str, Any]:
    entries = _load_entries(time_window)
    skills: set[str] = set()
    sessions: set[str] = set()
    total_inv = 0
    for e in entries:
        skill = e.get("skill", "")
        if skill and not (exclude_skills and skill in exclude_skills) and not (exclude_prefix and skill.startswith(exclude_prefix)):
            skills.add(skill)
            total_inv += 1
        if "session_id" in e:
            sessions.add(e["session_id"])
    return {
        "total_invocations": total_inv,
        "unique_skills": len(skills),
        "unique_sessions": len(sessions),
    }


def full_report(time_window: str = "all", top_n: int = 50,
                exclude_prefix: str | None = None,
                exclude_skills: set[str] | None = None) -> dict[str, Any]:
    """Load entries once and compute all analytics in a single pass.

    Returns a dict with keys: top_skills, last_used, total_stats, hourly,
    weekday, transitions, heatmap.
    """
    entries = _load_entries(time_window)

    counts: Counter[str] = Counter()
    last_used: dict[str, float] = {}
    skills_set: set[str] = set()
    sessions_set: set[str] = set()
    hourly: list[int] = [0] * 24
    weekday: list[int] = [0] * 7
    transitions_raw: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    sessions_map: dict[str, list[tuple[int, str]]] = defaultdict(list)

    heatmap_cutoff = int(time.time()) - 52 * 7 * _SECONDS_PER_DAY
    day_counts: Counter[str] = Counter()

    def _excluded(s: str) -> bool:
        if exclude_prefix and s.startswith(exclude_prefix):
            return True
        if exclude_skills and s in exclude_skills:
            return True
        return False

    for e in entries:
        skill = e.get("skill", "")
        ts = e.get("ts", 0)

        if skill and not _excluded(skill):
            counts[skill] += 1
            skills_set.add(skill)
            if ts > last_used.get(skill, 0):
                last_used[skill] = ts

        sid = e.get("session_id", "")
        if sid:
            sessions_set.add(sid)
            if skill and not _excluded(skill):
                sessions_map[sid].append((e.get("session_skill_seq", 0), skill))

        hourly[e.get("hour", 0) % 24] += 1
        weekday[e.get("weekday", 0) % 7] += 1

        if ts >= heatmap_cutoff:
            date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            day_counts[date_str] += 1

    # Build transition matrix from session sequences
    for seq_list in sessions_map.values():
        ordered = [s for _, s in sorted(seq_list)]
        for i in range(len(ordered) - 1):
            transitions_raw[ordered[i]][ordered[i + 1]] += 1

    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    return {
        "top_skills": [{"skill": s, "count": c} for s, c in counts.most_common(top_n)],
        "last_used": last_used,
        "total_stats": {
            "total_invocations": len(entries),
            "unique_skills": len(skills_set),
            "unique_sessions": len(sessions_set),
        },
        "hourly": [{"hour": h, "count": hourly[h]} for h in range(24)],
        "weekday": [{"day": day_names[d], "weekday": d, "count": weekday[d]} for d in range(7)],
        "transitions": {k: dict(v) for k, v in transitions_raw.items()},
        "heatmap": [{"date": d, "count": c} for d, c in sorted(day_counts.items())],
    }
