"""skill-habit CLI — entry point when installed via pip/pipx."""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

# When installed via pip/pipx the repo root sits next to skill_habit/
_ROOT = Path(__file__).parent.parent


def _run(script: str, *args: str) -> int:
    return subprocess.call([sys.executable, str(_ROOT / script), *args])


def cmd_install(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        prog="skill-habit install",
        description="Register skill-habit hooks in Claude Code settings.json",
    )
    p.add_argument("--uninstall", action="store_true", help="Remove hooks and generated skills")
    opts = p.parse_args(argv)
    flag = ["--uninstall"] if opts.uninstall else []
    return subprocess.call(["bash", str(_ROOT / "scripts" / "install.sh"), *flag])


def cmd_server(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        prog="skill-habit server",
        description="Open the management UI in your browser",
    )
    p.add_argument("--port", type=int, default=0)
    p.add_argument("--no-browser", action="store_true")
    opts = p.parse_args(argv)
    args = ["--port", str(opts.port)]
    if opts.no_browser:
        args.append("--no-browser")
    return _run("ui/server.py", *args)


def cmd_rebuild(argv: list[str]) -> int:
    """Force-rebuild shortcut skills and analytics cache right now."""
    _run("adapters/claude_code/skill_generator.py")
    return _run("scripts/build_cache.py")


def cmd_migrate(argv: list[str]) -> int:
    """Backfill missing fields in historical log entries."""
    p = argparse.ArgumentParser(
        prog="skill-habit migrate",
        description="Backfill default values for missing fields in skill-usage.log",
    )
    p.add_argument("--dry-run", action="store_true", help="Show count without modifying the log")
    opts = p.parse_args(argv)
    sys.path.insert(0, str(_ROOT))
    from core.tracker import migrate
    count = migrate(dry_run=opts.dry_run)
    action = "Would migrate" if opts.dry_run else "Migrated"
    print(f"{action} {count} log entries.")
    return 0


def cmd_version(argv: list[str]) -> int:
    from skill_habit import __version__
    print(f"skill-habit {__version__}")
    return 0


_COMMANDS = {
    "install": cmd_install,
    "server": cmd_server,
    "rebuild": cmd_rebuild,
    "migrate": cmd_migrate,
    "version": cmd_version,
}

_USAGE = """\
usage: skill-habit <command> [options]

Commands:
  install    Register hooks in Claude Code settings.json
  server     Open the management UI in your browser
  rebuild    Force-rebuild /sh:* shortcuts and analytics cache
  migrate    Backfill missing fields in historical log entries
  version    Print version and exit

Run `skill-habit <command> --help` for command-specific help.
"""


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(_USAGE)
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd not in _COMMANDS:
        print(f"Unknown command: {cmd}\n")
        print(_USAGE)
        sys.exit(1)

    sys.exit(_COMMANDS[cmd](sys.argv[2:]))
