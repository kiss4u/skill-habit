<h1 align="center">skill-habit</h1>

<h3 align="center">你的习惯塑造你的工具。</h3>

<p align="center">
  追踪你的 AI 技能使用习惯，按频率对命令排序显示。<br>
  每次会话开始，用得最多的技能自动排在最前——不再扫描，不再猜测。<br>
  内置使用分析、活跃度热力图、关联预测、技能管理与 Web 管理界面。
</p>

<p align="center">
  <a href="../README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <a href="#-快速开始"><img src="https://img.shields.io/badge/快速开始-→-blueviolet?style=flat-square" alt="快速开始"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-✓-7c3aed?style=flat-square" alt="Claude Code">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/version-0.0.1-brightgreen?style=flat-square" alt="version">
  <a href="https://github.com/kiss4u/skill-habit/stargazers"><img src="https://img.shields.io/github/stars/kiss4u/skill-habit?style=flat-square&color=orange" alt="GitHub Stars"></a>
</p>

<!-- <p align="center">
  <img src="../assets/demo.gif" alt="skill-habit demo" width="700">
</p> -->

---

## 目录

- [问题所在](#问题所在)
- [解决方式](#解决方式)
- [✨ 功能特性](#功能特性)
- [🚀 快速开始](#快速开始)
  - [Claude Code](#claude-code)
  - [其他平台](#其他平台)
  - [打开管理界面](#打开管理界面)
- [⬆️ 升级](#升级)
- [🗂 技能管理](#技能管理)
- [📊 数据分析](#数据分析)
- [🛠 设置](#设置)
- [🔑 快捷前缀](#快捷前缀)
  - [skill-habit 内置技能](#skill-habit-内置技能)
  - [修改前缀](#修改前缀)
- [⚙️ 配置](#配置)
  - [🔮 关联推荐（智能排序）](#关联推荐智能排序)
  - [📐 数字快捷键的排序原理](#数字快捷键的排序原理)
- [🔒 隐私说明](#隐私说明)
- [🌐 平台支持](#平台支持)
- [🤝 参与贡献](#参与贡献)
- [📄 许可证](#许可证)

---

## 问题所在

你装了一堆技能。结果每次输入 `/`，都要把列表从头浏览一遍，才能找到想用的那个。

## 解决方式

skill-habit 追踪你的每次技能调用（只记元数据，从不记录提示词内容）。

每次会话启动时，它自动重建一个 `/sh-*` 快捷前缀，把你最常用的技能排在最前面，并用你偏好的语言显示描述。

你用得最多的技能变成 `/sh-<技能名>`，几周没碰的会沉在后面。

列表反映的是你最常用的，而不是无效的默认顺序。

---

## ✨ 功能特性

|     | 功能             | 说明                                                                                                                                               | 支持        |
| --- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| 📊  | **频率排序**     | 每次会话根据真实使用频率重排快捷技能                                                                                                               | Claude Code |
| 📌  | **手动置顶**     | 将任意技能固定在最前面，支持 ↑↓ 调整顺序                                                                                                           | Claude Code |
| 🔮  | **关联预测**     | 基于全量历史使用链路，预测你下一步最可能调用的技能                                                                                                 | Claude Code |
| 🌡   | **活跃度热力图** | GitHub 风格格子图，可按时间范围查看技能使用贡献                                                                                                    | Claude Code |
| 🕐  | **时间分布**     | 按小时/星期展示你的编程活跃规律                                                                                                                    | Claude Code |
| 📝  | **技能管理**     | 搜索、排序、编辑所有已安装技能的说明                                                                                                               | Claude Code |
| 🚀  | **升级检测**     | 界面打开时自动静默检查更新；按版本号区分重要更新与小版本更新；有更新时展示 changelog 内容，重要更新在页面顶部显示可忽略的红色 banner；支持一键升级 | Claude Code |
| 🚫  | **黑名单**       | 将特定技能排除在频率排序和快捷列表之外，在技能页底部管理                                                                                           | Claude Code |
| 🗂   | **数据管理**     | 自动裁剪过期记录（默认 30 天），支持按天数清理或一键清空                                                                                           | 通用        |
| 🌐  | **多语言支持**   | 管理界面自动检测语言，支持中文、英文、德文、法文、俄文、韩文和日文                                                                                 | 通用        |
| 🔒  | **隐私优先**     | 只记录技能名称、时间和会话 ID，从不记录提示词内容                                                                                                  | 通用        |
| 🔧  | **按需启动**     | 管理服务器按需启动，关闭标签页后 5 分钟自动退出                                                                                                    | 通用        |


---

## 🚀 快速开始

> **环境要求：** macOS 或 Linux · Python 3.9+ · git
>
> **Windows：** 暂不支持原生安装，可通过 [WSL](https://learn.microsoft.com/zh-cn/windows/wsl/) 使用。原生支持已在规划中。

### Claude Code

**方案 A — Claude Code 插件安装（推荐）**

```bash
claude plugins install github:kiss4u/skill-habit
```

安装完成后重启 Claude Code 即开始追踪。

**方案 B — 一行命令安装**

```bash
curl -sSL https://raw.githubusercontent.com/kiss4u/skill-habit/main/scripts/bootstrap.sh | bash
```

**方案 C — pipx / pip**

> 注意：此方式不会自动安装 `/skill-habit:quick`、`/skill-habit:server` 等内置技能，建议优先使用方案 A 或 B。

pipx（推荐，环境隔离更干净）：
```bash
pipx install git+https://github.com/kiss4u/skill-habit
skill-habit install
```

pip：
```bash
pip install git+https://github.com/kiss4u/skill-habit
skill-habit install
```

> 重新启动一个 Claude Code 会话，追踪即刻开始。

### 其他平台

Cursor、Codex CLI、Gemini CLI 等适配器正在规划中。贡献方式参见下方"参与贡献"章节。

### 打开管理界面

安装完成后，用以下任意一种方式打开管理后台：

**在 Claude Code 中输入**：
```bash
/skill-habit:server
```

> 不知道自己的前缀？输入 `/skill-habit:quick` 可快速查看。

**pipx / pip 安装方式**：
```bash
skill-habit server
```

**bootstrap / clone 安装方式**：
```bash
python3 ~/.local/share/skill-habit/ui/server.py
```

浏览器自动打开，5 分钟无操作后服务器自动退出。

---

## ⬆️ 升级

升级命令与安装完全对应，直接重新运行即可：

**方案 A — 一行命令（重新运行 bootstrap）**

```bash
curl -sSL https://raw.githubusercontent.com/kiss4u/skill-habit/main/scripts/bootstrap.sh | bash
```

在已有安装目录上重新运行时，bootstrap 会检测到 `.git` 目录，自动执行 `git pull` 而非重新克隆。

**方案 C — pipx / pip**

pipx：
```bash
pipx upgrade skill-habit
skill-habit install
```

pip：
```bash
pip install --upgrade git+https://github.com/kiss4u/skill-habit
skill-habit install
```

**方案 C — 手动 / clone 仓库**

```bash
bash scripts/upgrade.sh
```

也可在管理界面的 **设置 → 版本与升级** 面板中检查更新，支持一键升级或复制命令手动执行。

---

## 🗂 技能管理

<a href="../assets/screenshot-skills.png"><img src="../assets/screenshot-skills.png" width="800" alt="Skills tab"></a>

打开 **Skills** 标签页可以：

- **搜索与排序** — 按名称/说明过滤；按使用次数、最近使用时间或名称排序（再次点击同一按钮可切换正序/倒序）
- **编辑说明** — 双击说明文字即可原地编辑（也可悬停后点击 ✏️ 图标）；回车或点击其他地方保存，Esc 取消
- **置顶** — 将技能锁定在快捷列表最前面；用 ↑↓ 调整置顶顺序
- **黑名单** — 点击任意行的**加入黑名单**按钮，将该技能排除在频率排序和快捷列表之外；在标签页底部的黑名单折叠区域可查看、翻页、移除
- **使用历史** — 查看每个技能的调用次数和最近使用时间

> Skills 标签页只显示至少使用过一次的技能，数据来源为 `~/.claude/skills/` 及所有已安装插件。

---

## 📊 数据分析

<a href="../assets/screenshot-analytics.png"><img src="../assets/screenshot-analytics.png" width="800" alt="Analytics tab"></a>

**Analytics** 标签页包含：

- **活跃度热力图** — GitHub 风格格子图，每格代表当天技能调用次数，时间范围可切换
- **常用技能** — 所选时间范围内的使用频率柱状图
- **每小时分布** — 一天中哪个时间段你最常使用技能
- **每周分布** — 哪几天你编程最活跃
- **转移图** — 你习惯连续使用哪些技能（驱动关联预测模型）

每张卡片均可在设置中单独开关。

---

## 🛠 设置

<a href="../assets/screenshot-settings.png"><img src="../assets/screenshot-settings.png" width="800" alt="Settings tab"></a>

**Settings** 标签页分为三个功能卡片，修改立即生效：

**通用配置**

| 配置项           | 说明                                                                             |
| ---------------- | -------------------------------------------------------------------------------- |
| 快捷前缀         | 所有快捷技能的命名空间，默认 `sh`；实时检测冲突，提供无冲突推荐前缀              |
| 数据范围         | 统计使用频率的时间窗口：全部 / 近半年 / 本月 / 本周 / 今天                       |
| 快捷模式         | 启用哪些快捷方式类型：数字模式（`/sh1`）、名称模式（`/sh-name`）或两者           |
| 数字快捷数量     | 数字模式生成的快捷键数量上限（1–9）                                              |
| 名称快捷数量     | 名称模式生成的快捷技能数量上限                                                   |
| 常用技能图表条数 | Analytics 页常用技能柱状图显示的技能数                                           |
| 重排间隔         | 多少分钟未操作后自动重建快捷列表                                                 |
| 关联预测         | 根据历史使用链路预测下一个技能，提前排到靠前位置                                 |
| 预测深度         | 关联预测最多推荐几个技能（1–5）                                                  |
| 主题             | 亮色 / 暗色 / 跟随系统                                                           |
| 语言             | 界面语言：自动 / 中文 / English / Deutsch / Français / Русский / 한국어 / 日本語 |
| 分析卡片开关     | 单独开关热力图、常用技能、转移图、时段分布、星期分布                             |

**数据管理**

| 配置项       | 说明                                                                   |
| ------------ | ---------------------------------------------------------------------- |
| 记录保留天数 | 历史日志滚动保留窗口（0 = 永久保留）；支持按天数清理早期数据或一键清空 |

**版本与升级**

| 状态                    | 行为                                                               |
| ----------------------- | ------------------------------------------------------------------ |
| 无更新                  | 静默完成，无提示                                                   |
| 小版本更新（patch）     | 此卡片显示橙色提示，不弹 banner                                    |
| 重要更新（major/minor） | 页面顶部显示红色 banner，展示 changelog，支持一键升级或点击 × 忽略 |

---

## 🔑 快捷前缀

**快捷前缀**是 skill-habit 为你生成的所有快捷技能的命名空间，默认为 `sh`。根据所选模式，每次会话开始时自动生成以下快捷方式：

| 模式     | 格式               | 示例（前缀 `sh`）         | 说明                                                                                  |
| -------- | ------------------ | ------------------------- | ------------------------------------------------------------------------------------- |
| **数字** | `/<前缀><N×序号>`  | `/sh1`、`/sh22`、`/sh333` | 按频率自动排序，支持关联预测；`/sh1` 始终指向当前最高频技能，关联预测每次会话自动更新 |
| **名称** | `/<前缀>-<技能名>` | `/sh-git-smart`           | 按名称直接调用；菜单顺序由 Claude Code 按字母序固定，与频率排序无关                   |

### skill-habit 内置技能

以下管理技能以插件形式内置，无论前缀如何设置，始终可用：

| 技能                   | 说明                           | 使用场景                                                                                         |
| ---------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------ |
| `/skill-habit:quick`   | 快速显示当前前缀和数字快捷映射 | 忘了自己的前缀或数字快捷键对应哪个技能时，直接输入查看，输出示例：`前缀: sh`、`/sh1 → git-smart` |
| `/skill-habit:server`  | 在浏览器中打开 Web 管理界面    | 修改配置、查看分析图表、管理技能列表；浏览器自动打开，5 分钟无操作后服务器自动退出               |
| `/skill-habit:rebuild` | 立即重建快捷技能               | 手动编辑 `~/.skill-habit/config.json` 后使用；通过 Web UI 保存的设置会自动触发重建，无需手动执行 |
| `/skill-habit:version` | 显示当前安装版本               | 排查问题或报 bug 时确认版本号                                                                    |

### 修改前缀

在 **设置 → 通用设置 → 快捷前缀** 中输入新值并保存，快捷技能立即重建。设置界面会实时检测冲突，并在输入框下方列出无冲突的推荐前缀，点击即可应用。

**前缀格式要求：** 仅允许字母、数字、`-`、`_`；最长 5 个字符。

---

## ⚙️ 配置

`~/.skill-habit/config.json` — 可在管理界面中编辑，也可直接修改：

```jsonc
{
  "prefix": "sh",                      // 快捷前缀：/sh-*
  "top_n": 10,                         // 每次会话生成的命名快捷技能数量上限
  "numeric_n": 5,                      // 数字模式生成 sh1…shN 的数量上限
  "time_window": "all",                // 今天 today | 本周 week | 本月 month | 全部 all
  "shortcut_mode": "both",             // "numeric"(/sh1) | "command"(/sh-<名称>) | "both"
  "enable_sequence_prediction": true,  // 关联推荐：基于历史转移规律预测下一个技能（见下方说明）
  "prediction_n": 5,                   // 最多提升几个候选技能（1–5）
  "top_skills_n": 10,                  // 常用技能图表中显示的技能条数
  "pinned_skills": [],                 // 无论频率如何，始终排在最前面
  "log_retention_days": 30,            // 滚动保留窗口（自然天）；0 = 永久保留
  "theme": "system",                   // 亮色 light | 暗色 dark | 跟随系统 system
  "language": "auto",                  // zh | en | de | fr | ru | ko | ja | auto
  "analytics_cards": {                 // 在管理界面中单独开关各卡片
    "heatmap": true,                   // 活跃度格子图
    "top_skills": true,                // 使用频率柱状图
    "transition_graph": true,          // 技能连续调用规律
    "hourly_distribution": true,       // 一天中哪个时段最活跃
    "weekday_distribution": true       // 哪几天编程最活跃
  }
}
```

### 🔮 关联推荐（智能排序）

开启 `enable_sequence_prediction` 后，每次会话开始时系统会：

1. 读取上一次使用的技能
2. 查询历史转移矩阵，预测最可能的后续 3 个技能
3. 将这 3 个技能提到快捷列表最前面

**效果因快捷模式而异：**

| 模式                        | 效果                                                                      |
| --------------------------- | ------------------------------------------------------------------------- |
| **数字模式** (`/sh1 /sh2…`) | 推荐直接改变 `sh1`/`sh2` 对应的技能，打 `/sh1` 即得推荐结果，**完全生效** |
| **命令模式** (`/sh-<名称>`) | 菜单顺序由 Claude Code 按名称字母序固定，推荐**不影响菜单排序**           |

> 推荐准确率随数据积累提升，建议使用 20+ 个 session 后观察效果。

---

### 📐 数字快捷键的排序原理

Claude Code 的自动补全按**名称总长度**排序——名称越短，得分越高、越靠前显示。当多个名称长度相同时，顺序是未定义的，因此等长的快捷键会以任意顺序出现，编号大小不起作用。

skill-habit 让每个排名的快捷键名称长度**严格递增**，方式是将排名数字重复 N 次：

| 排名        | 快捷键    | 长度   |
| ----------- | --------- | ------ |
| 1（最常用） | `sh1`     | 2 字符 |
| 2           | `sh22`    | 3 字符 |
| 3           | `sh333`   | 4 字符 |
| 4           | `sh4444`  | 5 字符 |
| 5           | `sh55555` | 6 字符 |

这保证了下拉菜单按频率顺序展示快捷键。当你的使用习惯改变时，下次 session 启动时快捷键会自动重新分配——如果某个技能变成了最常用的，它就会接管 `sh1`。

输入方式：直接打 `/sh1`，或打 `/sh2`（模糊匹配 `sh22`）后按回车。描述列会显示 `/{技能名} — 说明`，方便确认每个编号对应的技能。

---

## 🔒 隐私说明

skill-habit **绝不记录**提示词内容、文件路径或项目名称。

日志条目格式（`~/.skill-habit/skill-usage.log`）：

```jsonc
{
  "v": 1,                    // schema 版本，保证向前兼容
  "ts": 1719360000,          // unix 时间戳
  "skill": "git-smart",      // 技能名称（不含你输入的任何内容）
  "platform": "claude_code", // 调用技能的 AI 工具
  "hour": 14,                // 小时（0–23）
  "weekday": 1,              // 0 = 周一
  "session_id": "abc123",    // 标识一次连续的编程会话
  "session_skill_seq": 3,    // 在本次会话中的调用序号（1、2、3…）
  "project_hash": "a3f2c1",  // 单向哈希，不可还原
  "args_len": 42             // 仅字符数，不含内容
}
```

超过 `log_retention_days`（默认 30 天）的记录会在每次会话启动时自动裁剪。也可在 **设置 → 数据管理** 中输入天数清理早期数据，或输入 0 清空全部记录。

---

## 🌐 平台支持

| 平台           | 状态      |
| -------------- | --------- |
| Claude Code    | ✅ v0.0.1 |
| Cursor         | 🔜 规划中 |
| Codex CLI      | 🔜 规划中 |
| Gemini CLI     | 🔜 规划中 |
| GitHub Copilot | 🔜 规划中 |
| OpenCode       | 🔜 规划中 |
| Windsurf       | 🔜 规划中 |

贡献适配器请参见下方"参与贡献"章节。

---

## 🤝 参与贡献

1. Fork 本仓库
2. 在 `adapters/` 中选择一个平台（或提议新平台）
3. 实现 `adapters/base.py` 中的三个抽象方法
4. 提交 PR

---

## 📄 许可证

MIT © [kiss4u](https://github.com/kiss4u)
