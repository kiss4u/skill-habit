<h1 align="center">skill-habit</h1>

<h3 align="center">你的習慣塑造你的工具。</h3>

<p align="center">
  追蹤你的 AI 技能使用習慣，按頻率對指令排序顯示。<br>
  每次工作階段開始，用得最多的技能自動排在最前——不再掃描，不再猜測。<br>
  內建使用分析、活躍度熱力圖、關聯預測、技能管理與 Web 管理介面。
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
  <a href="#-快速開始"><img src="https://img.shields.io/badge/快速開始-→-blueviolet?style=flat-square" alt="快速開始"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-✓-7c3aed?style=flat-square" alt="Claude Code">
  <img src="https://img.shields.io/badge/Python-3.7%2B-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/version-0.0.1-brightgreen?style=flat-square" alt="version">
  <a href="https://github.com/kiss4u/skill-habit/stargazers"><img src="https://img.shields.io/github/stars/kiss4u/skill-habit?style=flat-square&color=orange" alt="GitHub Stars"></a>
</p>

---

## 目錄

- [🤔 問題所在](#-問題所在)
- [💡 解決方式](#-解決方式)
- [✨ 功能特性](#-功能特性)
  - [🔑 快捷前綴](#-快捷前綴)
  - [🔮 關聯推薦（智慧排序）](#-關聯推薦智慧排序)
  - [📐 數字快捷鍵的排序原理](#-數字快捷鍵的排序原理)
  - [🔒 隱私說明](#-隱私說明)
- [🚀 快速開始](#-快速開始)
  - [安裝](#安裝)
  - [升級](#升級)
  - [卸載](#卸載)
  - [配置](#配置)
- [內置技能](#內置技能)
- [🖥 管理平台](#-管理平台)
  - [🗂 技能管理](#-技能管理)
  - [📊 資料分析](#-資料分析)
  - [🛠 設定介面](#-設定介面)
- [🌐 平台支援](#-平台支援)
- [🤝 參與貢獻](#-參與貢獻)
- [📄 授權條款](#-授權條款)

---

## 🤔 問題所在

你裝了一堆技能。結果每次輸入 `/`，都要把列表從頭瀏覽一遍，才能找到想用的那個。

## 💡 解決方式

skill-habit 追蹤你的每次技能呼叫（只記元資料，從不記錄提示詞內容）。

每次工作階段啟動時，它自動重建一個 `/sh-*` 快捷前綴，把你最常用的技能排在最前面，並用你偏好的語言顯示描述。

你用得最多的技能變成 `/sh-<技能名>`，幾週沒碰的會沉在後面。

列表反映的是你最常用的，而不是無效的預設順序。

---

## ✨ 功能特性

|     | 功能             | 說明                                                                                                                                               | 支援        |
| --- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| 📊  | **頻率排序**     | 每次工作階段根據真實使用頻率重排快捷技能                                                                                                           | Claude Code |
| 📌  | **手動置頂**     | 將任意技能固定在最前面，支援 ↑↓ 調整順序                                                                                                           | Claude Code |
| 🔮  | **關聯預測**     | 基於全量歷史使用鏈路，預測你下一步最可能呼叫的技能                                                                                                 | Claude Code |
| 🌡   | **活躍度熱力圖** | GitHub 風格格子圖，可按時間範圍查看技能使用貢獻                                                                                                    | Claude Code |
| 🕐  | **時間分布**     | 按小時/星期展示你的程式設計活躍規律                                                                                                                | Claude Code |
| 📝  | **技能管理**     | 搜尋、排序、編輯所有已安裝技能的說明                                                                                                               | Claude Code |
| 🚀  | **升級偵測**     | 介面開啟時自動靜默檢查更新；按版本號區分重要更新與小版本更新；有更新時展示 changelog 內容，重要更新在頁面頂部顯示可忽略的紅色 banner；支援一鍵升級 | Claude Code |
| 🚫  | **黑名單**       | 將特定技能排除在頻率排序和快捷列表之外，在技能頁底部管理                                                                                           | Claude Code |
| 🗂   | **資料管理**     | 自動裁剪過期記錄（預設 30 天），支援按天數清理或一鍵清空                                                                                           | 通用        |
| 🌐  | **多語言支援**   | 管理介面自動偵測語言，支援中文、英文、德文、法文、俄文、韓文和日文                                                                                 | 通用        |
| 🔒  | **隱私優先**     | 只記錄技能名稱、時間和工作階段 ID，從不記錄提示詞內容                                                                                              | 通用        |
| 🔧  | **按需啟動**     | 管理伺服器按需啟動，關閉標籤頁後 5 分鐘自動退出                                                                                                    | 通用        |


### 🔑 快捷前綴

**快捷前綴**是 skill-habit 為你生成的所有快捷技能的命名空間，預設為 `sh`。根據所選模式，每次工作階段開始時自動生成以下快捷方式：

| 模式     | 格式               | 示例（前綴 `sh`）         | 說明                                                                                      |
| -------- | ------------------ | ------------------------- | ----------------------------------------------------------------------------------------- |
| **數字** | `/<前綴><N×序號>`  | `/sh1`、`/sh22`、`/sh333` | 按頻率自動排序，支援關聯預測；`/sh1` 始終指向當前最高頻技能，關聯預測每次工作階段自動更新 |
| **名稱** | `/<前綴>-<技能名>` | `/sh-git-smart`           | 按名稱直接呼叫；選單順序由 Claude Code 按字母序固定，與頻率排序無關                       |

在 **設定 → 通用設定 → 快捷前綴** 中輸入新值並儲存，快捷技能立即重建。設定介面會即時偵測衝突，並在輸入框下方列出無衝突的推薦前綴，點擊即可套用。

**前綴格式要求：** 僅允許字母、數字、`-`、`_`；最長 5 個字元。

### 🔮 關聯推薦（智慧排序）

開啟 `enable_sequence_prediction` 後，每次工作階段開始時系統會：

1. 讀取上一次使用的技能
2. 查詢歷史轉移矩陣，預測最可能的後續 3 個技能
3. 將這 3 個技能提到快捷清單最前面

效果因快捷模式而異：

| 模式                        | 效果                                                                         |
| --------------------------- | ---------------------------------------------------------------------------- |
| **數字模式** (`/sh1 /sh2…`) | 推薦直接改變 `sh1`/`sh2` 對應的技能，輸入 `/sh1` 即得推薦結果，**完全生效** |
| **命令模式** (`/sh-<名稱>`) | 選單順序由 Claude Code 按名稱字母序固定，推薦**不影響選單排序**              |

> 推薦準確率隨資料積累提升，建議使用 20+ 個工作階段後觀察效果。

### 📐 數字快捷鍵的排序原理

Claude Code 的自動補全按**名稱總長度**排序——名稱越短越靠前。skill-habit 讓每個排名的快捷鍵名稱長度**嚴格遞增**，方式是將排名數字重複 N 次：

| 排名        | 快捷鍵    | 長度   |
| ----------- | --------- | ------ |
| 1（最常用） | `sh1`     | 2 字元 |
| 2           | `sh22`    | 3 字元 |
| 3           | `sh333`   | 4 字元 |
| 4           | `sh4444`  | 5 字元 |
| 5           | `sh55555` | 6 字元 |

這保證了下拉選單按頻率順序展示快捷鍵。當你的使用習慣改變時，下次 session 啟動時快捷鍵會自動重新分配。

輸入方式：直接打 `/sh1`，或打 `/sh2`（模糊匹配 `sh22`）後按回車。

### 🔒 隱私說明

skill-habit **絕不記錄**提示詞內容、檔案路徑或專案名稱。

日誌條目格式（`~/.skill-habit/skill-usage.log`）：

```jsonc
{
  "v": 1,                    // schema 版本，保證向前相容
  "ts": 1719360000,          // unix 時間戳
  "skill": "git-smart",      // 技能名稱（不含你輸入的任何內容）
  "platform": "claude_code", // 呼叫技能的 AI 工具
  "hour": 14,                // 小時（0–23）
  "weekday": 1,              // 0 = 週一
  "session_id": "abc123",    // 標識一次連續的工作階段
  "session_skill_seq": 3,    // 在本次工作階段中的呼叫序號（1、2、3…）
  "project_hash": "a3f2c1",  // 單向雜湊，不可還原
  "args_len": 42             // 僅字元數，不含內容
}
```

超過 `log_retention_days`（預設 30 天）的記錄會在每次工作階段啟動時自動裁剪。也可在 **設定 → 資料管理** 中輸入天數清理早期資料，或輸入 0 清空全部。

---

## 🚀 快速開始

> **環境要求：** macOS 或 Linux · Python 3.7+ · git
>
> **Windows：** 暫不支援原生安裝，可透過 [WSL](https://learn.microsoft.com/zh-tw/windows/wsl/) 使用。原生支援已在規劃中。

### 安裝

**方案 A — Claude Code 外掛安裝（推薦）**

```bash
# 第一步：註冊 marketplace
claude plugins marketplace add kiss4u/skill-habit

# 第二步：安裝插件
claude plugins install skill-habit@skill-habit
```

安裝完成後重啟 Claude Code 即開始追蹤。

> **方案 A 遇到問題？** 可以直接使用下方的方案 B，效果完全一致。

**方案 B — 一行指令安裝**

```bash
curl -sSL https://raw.githubusercontent.com/kiss4u/skill-habit/main/scripts/bootstrap.sh | bash
```

> 默認安裝到 `~/.claude/skills/skill-habit`（目錄不存在時自動創建）。如需自定義路徑：`SKILL_HABIT_INSTALL_DIR=/your/path curl -sSL ... | bash`

**方案 C — pipx / pip**

> 注意：`skill-habit install` 運行時會自動同步內置技能，功能與方案 A/B 完全一致。

pipx（推薦，環境隔離更乾淨）：
```bash
pipx install git+https://github.com/kiss4u/skill-habit
skill-habit install
```

pip：
```bash
pip install git+https://github.com/kiss4u/skill-habit
skill-habit install
```

> 重新啟動一個 Claude Code 工作階段，追蹤即刻開始。

**其他平台**

Cursor、Codex CLI、Gemini CLI 等適配器正在規劃中。貢獻方式參見下方「參與貢獻」章節。

---

### 升級

升級指令與安裝完全對應，直接重新執行即可：

**方案 A — Claude Code 外掛**

```bash
claude plugins update skill-habit@skill-habit
```

**方案 B — 一行指令**

```bash
curl -sSL https://raw.githubusercontent.com/kiss4u/skill-habit/main/scripts/bootstrap.sh | bash
```

在已有安裝目錄上重新執行時，bootstrap 會偵測到 `.git` 目錄，自動執行 `git pull` 而非重新 clone。

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

也可在管理介面的 **設定 → 版本與升級** 面板中檢查更新，支援一鍵升級或複製指令手動執行。

---

### 卸載

**方案 A — Claude Code 插件**

```bash
/skill-habit:uninstall
```

**方案 B — 一行命令**

```bash
/skill-habit:uninstall
```

> 執行後會詢問是否同時刪除使用歷史和設定資料（`~/.skill-habit`），按需選擇即可。

**方案 C — pipx / pip**

pipx：
```bash
skill-habit uninstall
pipx uninstall skill-habit
```

pip：
```bash
skill-habit uninstall
pip uninstall skill-habit
```

---

### 配置

**打開管理介面**

安裝完成後，用以下任意一種方式打開管理後台：

在 Claude Code 中運行（方案 A / B）：
```bash
/skill-habit:server
```

命令行運行（方案 C — pipx / pip）：
```bash
skill-habit server
```


瀏覽器自動打開，5 分鐘無操作後伺服器自動退出。

**config.json**

`~/.skill-habit/config.json` — 可在管理介面中編輯，也可直接修改：

```jsonc
{
  "prefix": "sh",                      // 快捷前綴：/sh-*
  "top_n": 10,                         // 每次工作階段生成的命名快捷技能數量上限
  "numeric_n": 5,                      // 數字模式生成 sh1…shN 的數量上限
  "time_window": "all",                // 今天 today | 本週 week | 本月 month | 全部 all
  "shortcut_mode": "both",             // "numeric"(/sh1) | "command"(/sh-<名稱>) | "both"
  "enable_sequence_prediction": true,  // 關聯推薦：基於歷史轉移規律預測下一個技能（見下方說明）
  "prediction_n": 5,                   // 最多提升幾個候選技能（1–5）
  "top_skills_n": 10,                  // 常用技能圖表中顯示的技能條數
  "pinned_skills": [],                 // 無論頻率如何，始終排在最前面
  "log_retention_days": 30,            // 滾動保留窗口（自然天）；0 = 永久保留
  "theme": "system",                   // 亮色 light | 暗色 dark | 跟隨系統 system
  "language": "auto",                  // zh | en | de | fr | ru | ko | ja | auto
  "analytics_cards": {                 // 在管理介面中單獨開關各卡片
    "heatmap": true,                   // 活躍度格子圖
    "top_skills": true,                // 使用頻率柱狀圖
    "transition_graph": true,          // 技能連續呼叫規律
    "hourly_distribution": true,       // 一天中哪個時段最活躍
    "weekday_distribution": true       // 哪幾天編程最活躍
  }
}
```

---

## 內置技能

以下管理技能以插件形式內置，無論前綴如何設置，始終可用：

| 技能                   | 說明                           | 使用場景                                                                                         |
| ---------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------ |
| `/skill-habit:quick`   | 快速顯示當前前綴和數字快捷映射 | 忘記自己的前綴或數字快捷鍵對應哪個技能時，直接輸入查看，輸出範例：`前綴: sh`、`/sh1 → git-smart` |
| `/skill-habit:server`  | 在瀏覽器中開啟 Web 管理介面    | 修改設定、查看分析圖表、管理技能清單；瀏覽器自動開啟，5 分鐘無操作後伺服器自動退出。重複執行會自動重啟伺服器（不會多開），預設固定埠 5027，埠衝突時自動改用隨機埠               |
| `/skill-habit:rebuild` | 立即重建快捷技能               | 手動編輯 `~/.skill-habit/config.json` 後使用；透過 Web UI 儲存的設定會自動觸發重建，無需手動執行 |
| `/skill-habit:version` | 顯示目前安裝版本               | 排查問題或回報 bug 時確認版本號                                                                  |
| `/skill-habit:uninstall` | 卸載 skill-habit | 自動識別安裝方式，清理 hooks、快捷技能及插件資料；執行時會詢問是否同時刪除使用歷史和設定資料 |

---

## 🖥 管理平台

### 🗂 技能管理

<a href="../assets/screenshot-skills.png"><img src="../assets/screenshot-skills.png" width="800" alt="Skills tab"></a>

開啟 **Skills** 標籤頁可以：

- **搜尋與排序** — 按名稱/說明過濾；按使用次數、最近使用時間或名稱排序（再次點擊同一按鈕可切換正序/倒序）
- **編輯說明** — 雙擊說明文字即可原地編輯（也可懸停後點擊 ✏️ 圖示）；Enter 或點擊其他地方儲存，Esc 取消
- **置頂** — 將技能鎖定在快捷列表最前面；用 ↑↓ 調整置頂順序
- **黑名單** — 點擊任意行的**加入黑名單**按鈕，將該技能排除在頻率排序和快捷列表之外；在標籤頁底部的黑名單折疊區域可查看、翻頁、移除
- **使用歷史** — 查看每個技能的呼叫次數和最近使用時間

> Skills 標籤頁只顯示至少使用過一次的技能，資料來源為 `~/.claude/skills/`、所有已安裝插件，以及 `~/.claude/commands/` 下的自訂指令（按命名空間分組顯示在頁面底部的 Commands 區域）。

### 📊 資料分析

<a href="../assets/screenshot-analytics.png"><img src="../assets/screenshot-analytics.png" width="800" alt="Analytics tab"></a>

**Analytics** 標籤頁包含：

- **活躍度熱力圖** — GitHub 風格格子圖，每格代表當天技能呼叫次數，時間範圍可切換
- **常用技能** — 所選時間範圍內的使用頻率柱狀圖
- **每小時分布** — 一天中哪個時間段你最常使用技能
- **每週分布** — 哪幾天你程式設計最活躍
- **轉移圖** — 你習慣連續使用哪些技能（驅動關聯預測模型）

每張卡片均可在設定中單獨開關。

### 🛠 設定介面

<a href="../assets/screenshot-settings.png"><img src="../assets/screenshot-settings.png" width="800" alt="Settings tab"></a>

**Settings** 標籤頁分為三個功能卡片，修改立即生效：

**通用設定**

| 設定項           | 說明                                                                             |
| ---------------- | -------------------------------------------------------------------------------- |
| 快捷前綴         | 所有快捷技能的命名空間，預設 `sh`；即時偵測衝突，提供無衝突的推薦前綴            |
| 資料範圍         | 統計使用頻率的時間範圍：全部 / 近半年 / 本月 / 本週 / 今天                       |
| 快捷模式         | 啟用哪些快捷方式類型：數字模式（`/sh1`）、名稱模式（`/sh-name`）或兩者           |
| 數字快捷數量     | 數字模式產生的快捷鍵數量上限（1–9）                                              |
| 名稱快捷數量     | 名稱模式產生的快捷技能數量上限                                                   |
| 常用技能圖表條數 | Analytics 頁常用技能柱狀圖顯示的技能數                                           |
| 重排間隔         | 幾分鐘無操作後自動重建快捷列表                                                   |
| 關聯預測         | 根據歷史使用鏈路預測下一個技能，提前排到靠前位置                                 |
| 排除自身統計     | 開啟後，`skill-habit:*` 命令的呼叫不計入統計（預設開啟）                         |
| 預測深度         | 關聯預測最多推薦幾個技能（1–5）                                                  |
| 主題             | 亮色 / 暗色 / 跟隨系統                                                           |
| 語言             | 介面語言：自動 / 中文 / English / Deutsch / Français / Русский / 한국어 / 日本語 |
| 分析卡片開關     | 單獨開關熱力圖、常用技能、轉移圖、時段分布、星期分布                             |

**資料管理**

| 設定項       | 說明                                                                   |
| ------------ | ---------------------------------------------------------------------- |
| 記錄保留天數 | 歷史日誌滾動保留視窗（0 = 永久保留）；支援按天數清理早期資料或一鍵清空 |

**版本與升級**

| 狀態                    | 行為                                                               |
| ----------------------- | ------------------------------------------------------------------ |
| 無更新                  | 靜默完成，無提示                                                   |
| 小版本更新（patch）     | 此卡片顯示橙色提示，不彈 banner                                    |
| 重要更新（major/minor） | 頁面頂部顯示紅色 banner，展示 changelog，支援一鍵升級或點擊 × 忽略 |

---

## 🌐 平台支援

| 平台           | 狀態      |
| -------------- | --------- |
| Claude Code    | ✅ v0.0.1 |
| Cursor         | 🔜 規劃中 |
| Codex CLI      | 🔜 規劃中 |
| Gemini CLI     | 🔜 規劃中 |
| GitHub Copilot | 🔜 規劃中 |
| OpenCode       | 🔜 規劃中 |
| Windsurf       | 🔜 規劃中 |

貢獻適配器請參見下方「參與貢獻」章節。

---

## 🤝 參與貢獻

1. Fork 本儲存庫
2. 在 `adapters/` 中選擇一個平台（或提議新平台）
3. 實作 `adapters/base.py` 中的三個抽象方法
4. 提交 PR

---

## 📄 授權條款

MIT © [kiss4u](https://github.com/kiss4u)
