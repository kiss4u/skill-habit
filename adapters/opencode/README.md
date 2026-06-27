# Cursor Adapter (planned)

This adapter will integrate skill-habit with Cursor IDE.

## Status

Not yet implemented. Contributions welcome — see `adapters/base.py` for the interface.

## How to implement

1. Create `adapter.py` inheriting from `AdapterBase`
2. Implement `detect_installed()` — check for Cursor's config directory
3. Implement `install()` / `uninstall()` — register Cursor-specific hooks
4. Implement `generate_shortcuts()` — write shortcuts in Cursor's slash-command format
