<h1 align="center">skill-habit</h1>

<h3 align="center">Your habits shape your tools.</h3>

<p align="center">
  Track your AI skill usage habits — commands ranked by frequency, your most-used ones always first.<br>
  Every session, the right skill is one keystroke away — no scanning, no guessing.<br>
  Comes with usage analytics, activity heatmap, sequence prediction, skill management, and a web dashboard.
</p>

<p align="center">
  <a href="README.en.md">English</a> |
  <a href="../README.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick%20Start-→-blueviolet?style=flat-square" alt="Quick Start"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-✓-7c3aed?style=flat-square" alt="Claude Code">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/version-0.0.1-brightgreen?style=flat-square" alt="version">
  <a href="https://github.com/kiss4u/skill-habit/stargazers"><img src="https://img.shields.io/github/stars/kiss4u/skill-habit?style=flat-square&color=orange" alt="GitHub Stars"></a>
</p>

---

## Table of Contents

- [The problem](#the-problem)
- [The solution](#the-solution)
- [✨ Features](#-features)
- [🔒 Privacy](#-privacy)
- [🚀 Quick Start](#-quick-start)
  - [Installation](#installation)
  - [Upgrading](#upgrading)
  - [Configuration](#configuration)
- [🖥 Management Platform](#-management-platform)
  - [🗂 Skills Management](#-skills-management)
  - [📊 Analytics](#-analytics)
  - [🛠 Settings](#-settings)
- [🌐 Platform Support](#-platform-support)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## The problem

You installed a bunch of skills. Now every time you type `/`, you scroll through the whole list before you can use any of them.

## The solution

skill-habit tracks every skill you invoke (metadata only — never prompt content).

Each time a session starts, it rebuilds a `/sh-*` shortcut prefix with your top skills at the front, labelled in whatever language you prefer.

Your most-used skill becomes `/sh-<your-skill>`, the one you haven't touched in weeks sinks toward the bottom.

The list reflects your most-used skills, not a meaningless default order.

---

## ✨ Features

|     | Feature                    | Description                                                                                                                                                                                 | Supported on |
| --- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| 📊  | **Frequency ranking**      | Shortcuts reordered every session based on real usage                                                                                                                                       | Claude Code  |
| 📌  | **Pin to top**             | Force any skill to always appear first, reorder with ↑↓                                                                                                                                     | Claude Code  |
| 🔮  | **Association prediction** | Surfaces the skills you typically chain next, powered by your full usage history                                                                                                            | Claude Code  |
| 🌡   | **Activity heatmap**       | GitHub-style activity grid showing skill usage; time range is adjustable                                                                                                                    | Claude Code  |
| 🕐  | **Time patterns**          | Hourly and weekday breakdown of when you code most                                                                                                                                          | Claude Code  |
| 📝  | **Skill management**       | Search, sort, and edit descriptions for all installed skills                                                                                                                                | Claude Code  |
| 🚀  | **Upgrade check**          | Auto-checks every time the UI opens; distinguishes breaking vs patch releases; shows changelog notes inline and a persistent red banner for important updates; one-click upgrade or dismiss | Claude Code  |
| 🚫  | **Blacklist**              | Exclude specific skills from frequency ranking and shortcuts; manage from the Skills tab                                                                                                    | Claude Code  |
| 🗂   | **Log management**         | Auto-trim old records (default 30 days); clean up by N days or wipe all from the UI                                                                                                         | All          |
| 🌐  | **Multilingual UI**        | Management dashboard in Chinese, English, German, French, Russian, Korean and Japanese, auto-detected                                                                                       | All          |
| 🔒  | **Privacy-first**          | Logs skill name, time, and session ID only — never your prompt content                                                                                                                      | All          |
| 🔧  | **On-demand server**       | Management UI starts when you need it, exits when you close the tab                                                                                                                         | All          |

---

## 🔒 Privacy

skill-habit **never logs** prompt content, file paths, or project names.

Log entries look like this (`~/.skill-habit/skill-usage.log`):

```jsonc
{
  "v": 1,                    // schema version
  "ts": 1719360000,          // unix timestamp
  "skill": "git-smart",      // name only — not what you typed after it
  "platform": "claude_code", // which AI tool invoked the skill
  "hour": 14,                // hour of day (0–23)
  "weekday": 1,              // 0 = Monday
  "session_id": "abc123",    // identifies one continuous coding session
  "session_skill_seq": 3,    // position within the session (1, 2, 3…)
  "project_hash": "a3f2c1",  // one-way hash, not reversible
  "args_len": 42             // character count only, never content
}
```

Log entries older than `log_retention_days` (default: 30) are automatically trimmed each session. You can also clean up by entering a number of days (0 = wipe all) from **Settings → Data Management**.

---

## 🚀 Quick Start

> **Requirements:** macOS or Linux · Python 3.9+ · git
>
> **Windows:** Not yet supported natively. Use [WSL](https://learn.microsoft.com/windows/wsl/) as a workaround.

### Installation

**Option A — Claude Code plugin install (recommended)**

```bash
claude plugins install github:kiss4u/skill-habit
```

Restart Claude Code after install — tracking begins immediately.

**Option B — one-line install**

```bash
curl -sSL https://raw.githubusercontent.com/kiss4u/skill-habit/main/scripts/bootstrap.sh | bash
```

**Option C — pipx / pip**

> Note: this method does not install built-in skills (`/skill-habit:quick`, `/skill-habit:server`, etc.). Option A or B is recommended.

pipx (recommended — keeps it isolated):
```bash
pipx install git+https://github.com/kiss4u/skill-habit
skill-habit install
```

pip:
```bash
pip install git+https://github.com/kiss4u/skill-habit
skill-habit install
```

> Start a new Claude Code session — tracking begins immediately.

**Other platforms**

Cursor, Codex CLI, Gemini CLI, and more are planned. See the Contributing section to add an adapter.

**Opening the management UI**

After installing, open the dashboard with any of these:

In Claude Code:
```bash
/skill-habit:server
```

pip / pipx install:
```bash
skill-habit server
```

bootstrap / clone install:
```bash
python3 ~/.local/share/skill-habit/ui/server.py
```

The browser opens automatically. The server exits after 5 minutes of inactivity.

---

### Upgrading

Use the same command as install — each method handles upgrades automatically:

**Option A — Claude Code plugin**

```bash
claude plugins update skill-habit
```

**Option B — one-line**

```bash
curl -sSL https://raw.githubusercontent.com/kiss4u/skill-habit/main/scripts/bootstrap.sh | bash
```

Running bootstrap again on an existing install detects the `.git` directory and runs `git pull` instead of re-cloning.

**Option C — pipx / pip**

pipx:
```bash
pipx upgrade skill-habit
skill-habit install
```

pip:
```bash
pip install --upgrade git+https://github.com/kiss4u/skill-habit
skill-habit install
```

You can also check for updates and upgrade with one click directly from the **Settings → Version & Upgrade** panel in the management UI.

---

### Configuration

**Shortcut Prefix**

The **shortcut prefix** is the namespace for all shortcuts skill-habit generates — default is `sh`. Each session, shortcuts are built in one or both of these modes (configurable):

| Mode        | Format                   | Example (prefix `sh`)     | Notes                                                                                                       |
| ----------- | ------------------------ | ------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Numeric** | `/<prefix><N×rank>`      | `/sh1`, `/sh22`, `/sh333` | Frequency-sorted; `/sh1` always maps to the current top skill; association prediction updates every session |
| **Command** | `/<prefix>-<skill-name>` | `/sh-git-smart`           | Call skills by name directly; menu order is fixed alphabetically by Claude Code, unaffected by frequency    |

Go to **Settings → General → Shortcut prefix**, enter a new value, and save — shortcuts rebuild immediately. The UI detects conflicts in real time and shows conflict-free alternatives below the input for you to click and apply.

**Format rules:** letters, digits, `-`, `_` only; max 5 characters.

**Built-in Skills**

The following management skills are built into skill-habit as a plugin and are always available regardless of your prefix:

| Skill                  | Description                                       | When to use                                                                                                           |
| ---------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `/skill-habit:quick`   | Show current prefix and numeric shortcut mappings | Forgotten your prefix or which number maps to which skill? Run this to see, e.g. `Prefix: sh`, `/sh1 → git-smart`     |
| `/skill-habit:server`  | Open the web management UI in your browser        | Change settings, view analytics, manage skills; browser opens automatically, server exits after 5 minutes idle        |
| `/skill-habit:rebuild` | Rebuild shortcut skills immediately               | Use after manually editing `~/.skill-habit/config.json`; changes saved via the Web UI trigger a rebuild automatically |
| `/skill-habit:version` | Show the installed version                        | Confirm version when troubleshooting or filing a bug report                                                           |

**config.json**

`~/.skill-habit/config.json` — editable in the UI or directly:

```jsonc
{
  "prefix": "sh",                      // shortcut prefix: /sh-*
  "top_n": 10,                         // max command shortcuts generated per session
  "numeric_n": 5,                      // max numeric shortcuts generated (sh1…shN)
  "time_window": "all",                // "today" | "week" | "month" | "all"
  "shortcut_mode": "both",             // "numeric" (/sh1) | "command" (/sh-<name>) | "both"
  "enable_sequence_prediction": true,  // association prediction — see note below
  "prediction_n": 5,                   // max candidates to boost via prediction (1–5)
  "top_skills_n": 10,                  // rows shown in the Top Skills chart
  "pinned_skills": [],                 // always first, regardless of frequency
  "log_retention_days": 30,            // rolling window; 0 = keep forever
  "theme": "system",                   // "light" | "dark" | "system"
  "language": "auto",                  // "zh" | "en" | "de" | "fr" | "ru" | "ko" | "ja" | "auto"
  "analytics_cards": {                 // toggle individual cards in the UI
    "heatmap": true,                   // activity grid
    "top_skills": true,                // usage frequency bar chart
    "transition_graph": true,          // skill-chaining patterns
    "hourly_distribution": true,       // when during the day you code most
    "weekday_distribution": true       // which days you code hardest
  }
}
```

**🔮 Association Prediction (Smart Ordering)**

When `enable_sequence_prediction` is on, at each session start the system:

1. Reads the last skill you used
2. Queries the historical transition matrix to predict the 3 most likely next skills
3. Boosts those 3 skills to the top of the shortcut list

Effectiveness depends on shortcut mode:

| Mode                       | Effect                                                                                                                              |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Numeric** (`/sh1 /sh2…`) | Prediction directly changes which skill occupies `sh1`/`sh2`. Typing `/sh1` always runs the recommended skill. **Fully effective.** |
| **Command** (`/sh-<name>`) | Menu order is fixed alphabetically by Claude Code — prediction **has no effect on menu ordering**.                                  |

> Accuracy improves as data accumulates. Results are meaningful after 20+ sessions.

**📐 Numeric Shortcut Ordering**

Claude Code's autocomplete ranks suggestions primarily by **total name length** — shorter names score higher and appear first. skill-habit generates numeric shortcuts with **strictly increasing name lengths** by repeating each rank digit N times:

| Rank          | Shortcut  | Length  |
| ------------- | --------- | ------- |
| 1 (most used) | `sh1`     | 2 chars |
| 2             | `sh22`    | 3 chars |
| 3             | `sh333`   | 4 chars |
| 4             | `sh4444`  | 5 chars |
| 5             | `sh55555` | 6 chars |

This guarantees the dropdown shows shortcuts in frequency order. When your usage patterns shift, shortcut assignments update automatically at the next session start.

To invoke: type `/sh1` directly, or `/sh2` (fuzzy-matches `sh22`) and press Enter.

---

## 🖥 Management Platform

### 🗂 Skills Management

<a href="../assets/screenshot-skills.png"><img src="../assets/screenshot-skills.png" width="800" alt="Skills tab"></a>

Open the **Skills** tab to:

- **Search & sort** — filter by name/description; sort by usage count, last used, or name (click the same button again to reverse)
- **Edit descriptions** — double-click the description to edit inline (or click the ✏️ icon on hover); Enter or click elsewhere to save, Esc to cancel
- **Pin skills** — pin a skill to lock it at the top of your shortcuts; use ↑↓ to reorder pinned skills
- **Blacklist skills** — click **Block** on any row to exclude a skill from frequency ranking and shortcuts; manage the blacklist (view, paginate, unblock) in the collapsible Blacklist section at the bottom of the tab
- **Usage history** — see how many times you've used each skill and when you last used it

> The Skills tab only shows skills you've used at least once. Skills are sourced from `~/.claude/skills/` and all installed plugins.

### 📊 Analytics

<a href="../assets/screenshot-analytics.png"><img src="../assets/screenshot-analytics.png" width="800" alt="Analytics tab"></a>

The **Analytics** tab includes:

- **Activity heatmap** — GitHub-style grid; each cell = skill invocations that day; time range is adjustable
- **Top skills** — bar chart for the selected time window (today / week / month / all time)
- **Hourly distribution** — when during the day you reach for skills
- **Weekday distribution** — which days you code hardest
- **Transition graph** — which skills you chain together (feeds the prediction model)

Every card can be toggled individually in Settings.

### 🛠 Settings

<a href="../assets/screenshot-settings.png"><img src="../assets/screenshot-settings.png" width="800" alt="Settings tab"></a>

The **Settings** tab covers three cards, changes take effect immediately:

**General**

| Setting                | Description                                                                                                             |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Shortcut prefix        | Namespace for all shortcut skills, default `sh`; detects conflicts in real time and suggests conflict-free alternatives |
| Time window            | Time range for frequency ranking: All / Last 6 months / This month / This week / Today                                  |
| Shortcut mode          | Which shortcut types to enable: numeric (`/sh1`), named (`/sh-name`), or both                                           |
| Numeric shortcut count | Maximum number of numeric shortcuts to generate (1–9)                                                                   |
| Named shortcut count   | Maximum number of named shortcuts to generate                                                                           |
| Top skills chart rows  | Number of skills shown in the Analytics top-skills bar chart                                                            |
| Rebuild interval       | Minutes of inactivity before the shortcut list auto-rebuilds                                                            |
| Sequence prediction    | Predicts the next likely skill from usage history and boosts it upward                                                  |
| Prediction depth       | How many skills sequence prediction may promote (1–5)                                                                   |
| Theme                  | Light / Dark / System                                                                                                   |
| Language               | UI language: Auto / 中文 / English / Deutsch / Français / Русский / 한국어 / 日本語                                     |
| Analytics card toggles | Individually show/hide heatmap, top skills, transition graph, hourly and weekday distributions                          |

**Data Management**

| Setting            | Description                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------ |
| Log retention days | Rolling history window (0 = keep forever); supports cleaning by days or wiping all records |

**Version & Upgrade**

| Status             | Behavior                                                                  |
| ------------------ | ------------------------------------------------------------------------- |
| No update          | Silent check, no notification                                             |
| Patch update       | Amber notice in this card only — no banner                                |
| Major/minor update | Red banner at top of page showing changelog; one-click upgrade or dismiss |

---

## 🌐 Platform Support

| Platform       | Status     |
| -------------- | ---------- |
| Claude Code    | ✅ v0.0.1  |
| Cursor         | 🔜 planned |
| Codex CLI      | 🔜 planned |
| Gemini CLI     | 🔜 planned |
| GitHub Copilot | 🔜 planned |
| OpenCode       | 🔜 planned |
| Windsurf       | 🔜 planned |

---

## 🤝 Contributing

1. Fork this repo
2. Pick a platform in `adapters/` (or propose a new one)
3. Implement the three methods in `adapters/base.py`
4. Open a PR

---

## 📄 License

MIT © [kiss4u](https://github.com/kiss4u)
