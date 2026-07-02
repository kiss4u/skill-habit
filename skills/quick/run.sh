#!/usr/bin/env bash
set -euo pipefail
python3 - <<'EOF'
import json, os, locale

cfg = os.path.expanduser("~/.skill-habit/config.json")
smap = os.path.expanduser("~/.skill-habit/shortcut-map.json")

d = json.load(open(cfg)) if os.path.exists(cfg) else {}
prefix = d.get("prefix", "sh")
lang = d.get("language", "auto")
if lang == "auto":
    sys_lang = (locale.getdefaultlocale()[0] or "").lower()
    lang = "zh" if sys_lang.startswith("zh") else "en"

L = {
    "zh": ("前缀", "管理界面", "快捷键", "技能"),
    "de": ("Präfix", "Web-UI", "Kürzel", "Skill"),
    "fr": ("Préfixe", "Interface web", "Raccourci", "Skill"),
    "ru": ("Префикс", "Веб-интерфейс", "Ярлык", "Навык"),
    "ko": ("접두사", "관리 UI", "단축키", "스킬"),
    "ja": ("プレフィックス", "管理UI", "ショートカット", "スキル"),
}.get(lang, ("Prefix", "Web UI", "Shortcut", "Skill"))
lbl_prefix, lbl_webui, lbl_shortcut, lbl_skill = L

print(f"{lbl_prefix}: {prefix}")
print(f"{lbl_webui}: /skill-habit:server")

if os.path.exists(smap):
    sm = json.load(open(smap))
    nums = sorted(
        [(k, v) for k, v in sm.items()
         if k != "_prefix" and k.startswith(prefix) and k[len(prefix):len(prefix)+1].isdigit()],
        key=lambda x: len(x[0])
    )
    if nums:
        print()
        print(f"  {lbl_shortcut:<16}{lbl_skill}")
        print(f"  {'-' * 16}{'-' * 20}")
        for sh, skill in nums[:5]:
            print(f"  /{sh:<15} {skill}")
EOF
