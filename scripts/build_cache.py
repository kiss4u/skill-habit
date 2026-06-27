#!/usr/bin/env python3
"""Pre-compute analytics cache at session start."""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import load as load_config
from core.cache import rebuild

if __name__ == "__main__":
    config = load_config()
    rebuild(config)
