# Contributing

Thank you for your interest in skill-habit!

## Adding a platform adapter

1. Fork this repo
2. Create a directory under `adapters/<platform>/`
3. Implement the three abstract methods in `adapters/base.py`:
   - `install(config)` — register hooks in the target tool
   - `uninstall(config)` — remove hooks
   - `generate_shortcuts(config)` — write shortcut skill files
4. Add a `README.md` in your adapter directory describing setup steps
5. Open a PR

## Running locally

```bash
git clone https://github.com/kiss4u/skill-habit.git
cd skill-habit
python3 ui/server.py
```

## Code style

- Python 3.7+
- No external dependencies beyond the standard library
- Privacy-first: never log prompt content, file paths, or project names
