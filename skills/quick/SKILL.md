---
name: quick
description: 快速显示当前快捷前缀和技能映射 / Show current prefix and shortcut mappings
---

Execute this to show your current skill-habit prefix and top shortcuts:

```bash
python3 -c "
import json, os

cfg = os.path.expanduser('~/.skill-habit/config.json')
smap = os.path.expanduser('~/.skill-habit/shortcut-map.json')

d = json.load(open(cfg)) if os.path.exists(cfg) else {}
prefix = d.get('prefix', 'sh')

print(f'Prefix   : {prefix}')
print(f'Manage   : /{prefix}-manage')
print(f'Server   : /skill-habit:server')

if os.path.exists(smap):
    sm = json.load(open(smap))
    nums = sorted(
        [(k, v) for k, v in sm.items()
         if k != '_prefix' and k[len(prefix):len(prefix)+1].isdigit()],
        key=lambda x: len(x[0])
    )
    if nums:
        print()
        for sh, skill in nums[:5]:
            print(f'  /{sh:<14} -> {skill}')
"
```
