# skill-habit Code Review

**Reviewed:** 2026-06-27  
**Scope:** core/analyzer.py, core/cache.py, core/config.py, core/tracker.py,  
adapters/claude_code/skill_generator.py, adapters/claude_code/record.py,  
ui/server.py  
**Focus:** Performance (hot-path overhead, redundant I/O) and Maintainability

---

## HIGH Severity

---

### H-01: Hot path reads the full log file on every invocation (tracker.py + record.py)

**File:** `core/tracker.py:22-26` (called from `adapters/claude_code/record.py:24`)  
**Issue:** `_resolve_skill()` reads and parses `SHORTCUT_MAP` from disk on every single call to `record()`. Because `record.py` is executed as a subprocess on every prompt submission, this is unavoidable per-invocation I/O, but the file read happens before checking whether a lookup is even needed. For most invocations (non-shortcut skills) the map is loaded, fully parsed, and then never consulted.  
**Fix:** Check whether `skill` looks like it could be a shortcut before loading the map:
```python
def _resolve_skill(skill: str) -> str:
    # Fast-path: if skill contains ":" it is namespaced, never a shortcut
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
    if skill.startswith(prefix) and skill[len(prefix):].isdigit():
        return mapping.get(skill, skill)
    if skill.startswith(f"{prefix}-"):
        remainder = skill[len(prefix) + 1:]
        return skill if remainder == "manage" else remainder
    return skill
```
Move the `SHORTCUT_MAP.exists()` guard to the very top so disk access is skipped entirely when the file is absent.

---

### H-02: `cache.build()` reads the JSONL log file up to five times in one request

**File:** `core/cache.py:32-48`  
**Issue:** `build()` calls up to five separate `analyzer.*` functions, each of which independently calls `_load_entries()`, which opens and parses the full log file. On a log with tens of thousands of entries this is 5× redundant parsing in a single cache-rebuild triggered by a UI page load.  
**Fix:** Add a single-pass aggregation function in `analyzer.py` that computes all metrics in one read, and have `cache.build()` call it once:
```python
# analyzer.py
def full_report(time_window: str, top_n: int, exclude_skills: set | None = None) -> dict:
    entries = _load_entries(time_window)
    # derive top_skills, transition_matrix, hourly_distribution,
    # weekday_distribution, heatmap, total_stats from the single `entries` list
    ...
```

---

### H-03: `/api/skills` triggers two full log reads plus a full skill scan on every page load

**File:** `ui/server.py:167-169`  
**Issue:** The `/api/skills` handler calls both `analyzer.top_skills("all", n=9999)` and `analyzer.last_used_per_skill()`. Each independently re-reads the entire JSONL log. Additionally `scan_all_skills()` walks the filesystem for every request. None of these results are cached.  
**Fix:** Serve `/api/skills` from the existing cache object (add a `skills_index` key populated during `cache.build()`), or at minimum combine the two log reads into a single pass inside a new `analyzer.skills_stats()` helper. The `scan_all_skills()` result should be memoized for the lifetime of the server process (a module-level dict with an mtime guard on `~/.claude/skills/` is sufficient).

---

### H-04: `_atomic_rebuild` in `skill_generator.py` does `shutil.rmtree` + rename for every skill slot unconditionally

**File:** `adapters/claude_code/skill_generator.py:252-261`  
**Issue:** On every re-rank, every shortcut directory is deleted and recreated even when its content has not changed. With 10 command shortcuts + 5 numeric shortcuts that is up to 30 filesystem operations (15 rmtree + 15 rename) regardless of whether anything changed. This is the most expensive part of the hot path triggered by `generate()`.  
**Fix:** Before writing, compare the content that would be written against the existing `SKILL.md` content:
```python
existing = skill_dir / "SKILL.md"
if skill_dir.exists() and existing.exists() and existing.read_text(encoding="utf-8") == content:
    new_generated.append(dir_name)
    shortcut_map[dir_name] = skill_name
    continue   # skip the rmtree/rename cycle
```
This makes re-ranks with no frequency change into a no-op at the filesystem level.

---

### H-05: `_last_used_skill()` re-reads the entire log to get only the final entry

**File:** `adapters/claude_code/skill_generator.py:104-121`  
**Issue:** The function iterates every line of the JSONL log to find the last written skill. Because entries are appended in chronological order, only the last non-empty line matters. For large logs this is O(N) reads for a O(1) operation.  
**Fix:** Read the file in reverse without loading the whole thing, or store the last-used skill in a small sidecar file updated by `tracker.record()`:
```python
def _last_used_skill() -> str | None:
    if not LOG_FILE.exists():
        return None
    # Read last 4 KB — enough to contain at least one complete JSON line
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
```

---

### H-06: `_check_update()` makes an outbound HTTP request on every `/api/version` call with no caching

**File:** `ui/server.py:38-68`  
**Issue:** Every time the UI loads or the user navigates to the version section, `_check_update()` is called synchronously inside the request handler, which performs a `git fetch` subprocess AND a `urlopen` to GitHub. This blocks the single-threaded HTTPServer for the entire network round-trip (up to 8–10 seconds on slow connections), freezing all other UI requests.  
**Fix:** Cache the result at module level with a TTL, and run the check in a background thread:
```python
_update_cache: dict = {}
_update_cache_ts: float = 0.0
_UPDATE_TTL = 3600  # seconds

def _check_update() -> dict:
    global _update_cache, _update_cache_ts
    if time.time() - _update_cache_ts < _UPDATE_TTL and _update_cache:
        return _update_cache
    # run in thread to avoid blocking the server
    ...
```

---

### H-07: Double body read in `/api/logs/trim` POST handler

**File:** `ui/server.py:248`  
**Issue:** `do_POST` already reads the full request body at line 97 and passes it as `data` to `_handle_api_post`. Inside the `/api/logs/trim` branch, the handler then calls `self.rfile.read(...)` a second time (line 248). The second read returns an empty `bytes` object because the stream was already consumed, so `body` is always `b""` and `days` is always the fallback `30` regardless of what the caller sent.  
**Fix:** Use the already-parsed `data` dict that is passed as the second argument:
```python
elif path == "/api/logs/trim":
    days = int(data.get("days", 30))
    count = analyzer.trim_log(days)
    generate_shortcuts(load_config())
    self._json({"ok": True, "removed": count})
```

---

## MEDIUM Severity

---

### M-01: `_generated_set()` duplicated verbatim in `cache.py` and `server.py`

**Files:** `core/cache.py:10-19`, `ui/server.py:127-133`, `ui/server.py:159-166`  
**Issue:** The pattern of reading `GENERATED_MANIFEST` and `EVER_GENERATED_MANIFEST` and merging them into a set is copy-pasted three times. If the manifest logic changes (e.g., a new manifest file is added), all three sites must be updated in sync.  
**Fix:** `_generated_set()` already exists in `cache.py`; export it from there and import it in `server.py`:
```python
# cache.py — make it public
def generated_set() -> set[str]:
    ...

# server.py
from core.cache import generated_set
```

---

### M-02: `config.load()` reads from disk on every call — no in-process caching

**File:** `core/config.py:46-54`  
**Issue:** Every handler that calls `load_config()` triggers a disk read and a `_deep_merge`. In `server.py`, several handlers call it independently (`/api/config`, `/api/cache`, `/api/skills`, POST `/api/config`). The server is single-threaded and config changes are infrequent, so this is purely wasteful.  
**Fix:** Cache the loaded config at module level and invalidate it only when `save()` is called:
```python
_config_cache: dict | None = None

def load() -> dict:
    global _config_cache
    if _config_cache is not None:
        return _config_cache.copy()
    ...
    _config_cache = merged
    return merged.copy()

def save(config: dict) -> None:
    global _config_cache
    ...
    _config_cache = None
```

---

### M-03: `/api/cache` with an explicit `time_window` always fully rebuilds — no staleness check

**File:** `ui/server.py:113-117`  
**Issue:** Switching time windows in the UI triggers a complete cache rebuild every time, even if the user switches back to a window that was just computed. The cache object stores `time_window` in its `built_at` metadata but this is never checked before rebuilding.  
**Fix:** Store a per-window cache or check whether the requested window matches `cache["time_window"]` and `cache["built_at"]` is recent enough before triggering a rebuild.

---

### M-04: `transition_matrix` reads and sorts the full log per call with no reuse in `cache.build()`

**File:** `core/analyzer.py:65-82`  
**Issue:** `transition_matrix` calls `_load_entries()` independently. In `cache.build()` (cache.py:42), it is called after `top_skills`, `total_stats`, `heatmap_data`, `hourly_distribution`, and `weekday_distribution` have each already loaded the full log. This is a direct consequence of H-02 but worth noting as its own callout because the sort inside `transition_matrix` (line 78) is O(N log N) per session, and the function is also called from `predict_next` in `skill_generator.py`, triggering yet another full log read during `generate()`.  
**Fix:** As part of the H-02 fix (single-pass aggregation), compute the transition matrix in the same pass as other statistics.

---

### M-05: `heatmap_data()` ignores the caller-supplied `time_window` and always loads `"all"` entries, then filters in Python

**File:** `core/analyzer.py:94-102`  
**Issue:** `heatmap_data(weeks=26)` calls `_load_entries("all")` (line 96), loading every log entry regardless of age, then applies its own `cutoff` filter manually at line 99. This is inconsistent with every other function in the file and loads more data than needed.  
**Fix:**
```python
def heatmap_data(weeks: int = 26) -> list[dict[str, Any]]:
    cutoff = int(time.time()) - weeks * 7 * 86400
    # Pass cutoff window so _load_entries can skip old lines during parsing
    entries = _load_entries("all")   # keep as-is until _load_entries supports int cutoff
    ...
```
Or expose a `since_ts` parameter on `_load_entries` so the cutoff is applied during line iteration rather than after loading everything into memory.

---

### M-06: `clear_log()` leaves the file handle unclosed on the count line

**File:** `core/analyzer.py:149`  
**Issue:** `sum(1 for line in open(LOG_FILE) if line.strip())` opens the file without a context manager. If an exception occurs before `LOG_FILE.write_text(...)` the file descriptor leaks.  
**Fix:**
```python
def clear_log() -> int:
    if not LOG_FILE.exists():
        return 0
    with open(LOG_FILE) as f:
        count = sum(1 for line in f if line.strip())
    LOG_FILE.write_text("", encoding="utf-8")
    return count
```

---

### M-07: `_append_locked` does not close the lock file descriptor on the non-blocking error path

**File:** `core/tracker.py:91-103`  
**Issue:** When `fcntl.flock` raises `BlockingIOError` (lock busy), execution jumps to `finally`. The `finally` block calls `fcntl.flock(lock_fd, LOCK_UN)` before `lock_fd.close()`. Unlocking a file descriptor that was never successfully locked is harmless on Linux, but calling `close()` after an unlock that errors (the bare `except Exception: pass` at line 101) could still mask a real problem. More critically, if `open(LOCK_FILE, "w")` itself raises (e.g., permission denied), `lock_fd` is never assigned and the `finally` block will raise `UnboundLocalError`.  
**Fix:**
```python
def _append_locked(entry: dict[str, Any]) -> None:
    try:
        lock_fd = open(LOCK_FILE, "w")
    except OSError:
        return   # can't obtain lock file; drop silently
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except BlockingIOError:
        pass
    finally:
        lock_fd.close()   # flock is released automatically on close
```
Note: `fcntl.flock` is released implicitly when the file descriptor is closed, so the explicit `LOCK_UN` call is redundant and can be removed.

---

### M-08: `generate()` calls `trim_log()` inside the file-generation lock, holding the lock during a full log rewrite

**File:** `adapters/claude_code/skill_generator.py:128-130`, `183-189`  
**Issue:** `trim_log()` (called at line 130, before the lock at line 183) reads and rewrites the entire log file. This is intentional and happens before the lock. However, `top_skills()` and `predict_next()` (which call `_load_entries()`) are also called before the lock. If a concurrent `record()` call appends to the log between the `top_skills()` read and the `_atomic_rebuild()` write, the shortcut ordering may be one entry stale. This is an acceptable race for this use case, but the comment at line 183 implies the lock is meant to protect the whole operation — it does not.  
**Fix:** Document the intentional race explicitly with a comment, or move `top_skills()` / `predict_next()` calls inside the lock scope if strict consistency is required.

---

### M-09: `_write_manage_skill` embeds an absolute path to `server.py` in the generated SKILL.md content

**File:** `adapters/claude_code/skill_generator.py:193-200`  
**Issue:** The generated skill file contains the hardcoded absolute path `python3 /Users/.../skill-habit/ui/server.py`. If the repository is moved, renamed, or used by another user, the path in the already-generated skill becomes stale and the manage command silently fails at runtime.  
**Fix:** Either compute the path at invocation time (always fresh), or generate an invocation through a stable entry-point (e.g., `python3 -m skill_habit.ui` or a `pip`-installed console script) that does not depend on repository location.

---

### M-10: Input validation missing on integer query parameters in `server.py`

**File:** `ui/server.py:137`, `140`, `144`, `145`  
**Issue:** `int(qs.get("n", ["20"])[0])`, `int(qs.get("weeks", ["26"])[0])`, `int(qs.get("page", ...)[0])`, and `int(qs.get("per_page", ...)[0])` will raise `ValueError` if a non-integer string is supplied. Since `BaseHTTPRequestHandler` has no global exception handler for `do_GET`, an unhandled `ValueError` crashes the handler thread and returns a 500 with a Python traceback sent to the client (default HTTPServer behavior) instead of a clean 400 response.  
**Fix:** Wrap each conversion in a try/except and return 400:
```python
try:
    n = int(qs.get("n", ["20"])[0])
except ValueError:
    self.send_error(400, "Invalid parameter")
    return
```
Or add a small helper: `def _int_param(qs, key, default): ...`

---

## LOW Severity

---

### L-01: Magic numbers for time windows scattered across `analyzer.py`

**File:** `core/analyzer.py:38-40`  
**Issue:** `7 * 86400` and `30 * 86400` appear inline with no named constant. `86400` also appears in `heatmap_data` (line 95) and `trim_log` (line 122).  
**Fix:** Define `_SECONDS_PER_DAY = 86_400` at module level and use it throughout.

---

### L-02: `ADAPTER_VERSION` in `tracker.py` is a magic string disconnected from the project version

**File:** `core/tracker.py:13`  
**Issue:** `ADAPTER_VERSION = "0.1.0"` is hardcoded and will diverge from `pyproject.toml` as the project evolves. Log entries will carry the wrong adapter version after any release where this constant is not manually updated.  
**Fix:** Read the version from `pyproject.toml` or an `__version__` attribute at import time, or accept that the version is intentionally pinned to the log schema version rather than the package version (and add a comment saying so).

---

### L-03: `_parse_frontmatter` silently returns empty strings for malformed SKILL.md files

**File:** `adapters/claude_code/skill_generator.py:71-85`  
**Issue:** If a SKILL.md has an opening `---` but no closing `---`, the while loop runs to the end of the file and returns whatever partial `name`/`description` it found (potentially empty strings). The caller in `_scan_dir` uses `if name and name not in out` so a partially-parsed file with no `name:` line is silently discarded. This is probably the right behaviour, but there is no log or debug output to help diagnose why a skill is missing.  
**Fix:** At minimum, add an `# noqa`-style comment noting the silent-discard contract so future maintainers understand the intent.

---

### L-04: `Handler._last_request` is a class variable shared across all handler instances without a lock

**File:** `ui/server.py:76`  
**Issue:** `_last_request` is a class-level attribute updated by every `do_GET` and `do_POST`. Python's GIL makes the float assignment itself atomic, but the watchdog thread reads it concurrently. For a single-threaded HTTPServer this is fine in practice, but the pattern is fragile and would break immediately if `ThreadingMixIn` is ever added.  
**Fix:** Use `threading.Lock` or `threading.Event` to guard access, or document the single-threaded assumption explicitly.

---

### L-05: `clear()` in `skill_generator.py` accepts a `prefix` argument it does not use

**File:** `adapters/claude_code/skill_generator.py:300-308`  
**Issue:** The function signature is `def clear(prefix: str | None = None)` but `prefix` is never referenced in the function body. The manifest-based cleanup at line 303 does not filter by prefix.  
**Fix:** Remove the unused `prefix` parameter, or implement the prefix-scoped clear if that was the intended behaviour.

---

_Reviewed by: manual adversarial review_  
_Depth: standard + cross-file_
