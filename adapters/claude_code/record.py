#!/usr/bin/env python3
"""Standalone skill recorder — called by shell hooks to avoid import overhead."""
from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.tracker import record


def main() -> None:
    p = argparse.ArgumentParser(description="Record a skill invocation")
    p.add_argument("--skill", required=True)
    p.add_argument("--session-id", default="unknown")
    p.add_argument("--session-seq", type=int, default=0)
    p.add_argument("--args-len", type=int, default=0)
    p.add_argument("--platform", default="claude_code")
    p.add_argument("--cwd", default=None)
    args = p.parse_args()

    record(
        args.skill,
        platform=args.platform,
        session_id=args.session_id,
        session_seq=args.session_seq,
        args_len=args.args_len,
        cwd=args.cwd or os.getcwd(),
    )


if __name__ == "__main__":
    main()
