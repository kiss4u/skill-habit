from __future__ import annotations
import json
import time
from typing import Any

from .config import CACHE_FILE, EVER_GENERATED_MANIFEST, GENERATED_MANIFEST, SKILL_HABIT_DIR
from . import analyzer


def generated_set() -> set[str]:
    """Return the union of current and ever-generated shortcut names."""
    result: set[str] = set()
    for mf in (GENERATED_MANIFEST, EVER_GENERATED_MANIFEST):
        if mf.exists():
            try:
                result |= set(json.loads(mf.read_text()))
            except Exception:
                pass
    return result


def build(config: dict[str, Any]) -> dict[str, Any]:
    time_window = config.get("time_window", "all")
    top_n = config.get("top_n", 10)
    top_skills_n = config.get("top_skills_n", 10)
    cards = config.get("analytics_cards", {})
    generated = generated_set()

    # Fetch extra beyond the target to ensure enough real skills remain after
    # filtering out generated shortcuts (some real skills share names with old shortcuts)
    fetch_n = max(top_n, top_skills_n) + len(generated) + 10
    report = analyzer.full_report(time_window, top_n=fetch_n)

    bl: set[str] = set(config.get("blacklist", []))
    # Filter top_skills to exclude generated shortcuts, blacklist, and skill-habit meta-skills
    filtered_top_skills = [
        item for item in report["top_skills"]
        if item["skill"] not in generated
        and item["skill"] not in bl
        and not item["skill"].startswith("skill-habit:")
    ][:top_skills_n]

    # Recompute total_stats excluding generated shortcuts and meta-skills
    stats = report["total_stats"].copy()
    stats["unique_skills"] = sum(
        1 for item in report["top_skills"]
        if item["skill"] not in generated
        and not item["skill"].startswith("skill-habit:")
    )

    cache: dict[str, Any] = {
        "built_at": int(time.time()),
        "time_window": time_window,
        "stats": stats,
    }

    if cards.get("top_skills", True):
        cache["top_skills"] = filtered_top_skills

    if cards.get("heatmap", True):
        cache["heatmap"] = report["heatmap"]

    if cards.get("transition_graph", True):
        cache["transition_matrix"] = report["transitions"]

    if cards.get("hourly_distribution", True):
        cache["hourly_distribution"] = report["hourly"]

    if cards.get("weekday_distribution", True):
        cache["weekday_distribution"] = report["weekday"]

    return cache


def save(cache: dict[str, Any]) -> None:
    SKILL_HABIT_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, ensure_ascii=False)


def load() -> dict[str, Any] | None:
    if not CACHE_FILE.exists():
        return None
    with open(CACHE_FILE) as f:
        return json.load(f)


def rebuild(config: dict[str, Any]) -> dict[str, Any]:
    cache = build(config)
    save(cache)
    return cache
