<h1 align="center">skill-habit</h1>

<h3 align="center">당신의 습관이 도구를 만듭니다.</h3>

<p align="center">
  AI 스킬 사용 습관을 추적합니다 — 명령어를 빈도순으로 정렬하고, 가장 많이 쓰는 것을 항상 맨 앞에 표시합니다.<br>
  매 세션마다 필요한 스킬은 키 하나면 충분합니다 — 스크롤도, 추측도 필요 없습니다.<br>
  사용 통계, 활동 히트맵, 시퀀스 예측, 스킬 관리, 그리고 웹 대시보드를 제공합니다.
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
  <a href="#-빠른-시작"><img src="https://img.shields.io/badge/Quick%20Start-→-blueviolet?style=flat-square" alt="Quick Start"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-✓-7c3aed?style=flat-square" alt="Claude Code">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/version-0.0.1-brightgreen?style=flat-square" alt="version">
  <a href="https://github.com/kiss4u/skill-habit/stargazers"><img src="https://img.shields.io/github/stars/kiss4u/skill-habit?style=flat-square&color=orange" alt="GitHub Stars"></a>
</p>

---

## 목차

- [문제점](#문제점)
- [해결책](#해결책)
- [✨ 기능](#-기능)
- [🔒 개인정보 보호](#-개인정보-보호)
- [🚀 빠른 시작](#-빠른-시작)
  - [설치](#설치)
  - [업그레이드](#업그레이드)
  - [설정](#설정)
- [🖥 관리 플랫폼](#-관리-플랫폼)
  - [🗂 스킬 관리](#-스킬-관리)
  - [📊 통계](#-통계)
  - [🛠 설정 메뉴](#-설정-메뉴)
- [🌐 플랫폼 지원](#-플랫폼-지원)
- [🤝 기여하기](#-기여하기)
- [📄 라이선스](#-라이선스)

---

## 문제점

수많은 스킬을 설치했지만, `/`를 입력할 때마다 전체 목록을 스크롤해야 원하는 것을 사용할 수 있습니다.

## 해결책

skill-habit은 호출하는 모든 스킬을 추적합니다 (메타데이터만 — 프롬프트 내용은 절대 저장하지 않습니다).

세션이 시작될 때마다 자주 사용하는 스킬을 앞에 배치하여 `/sh-*` 단축키 프리픽스를 재구성하고, 원하는 언어로 레이블을 표시합니다.

가장 많이 사용한 스킬은 `/sh-<your-skill>`이 되고, 몇 주 동안 건드리지 않은 스킬은 아래로 내려갑니다.

목록은 의미 없는 기본 순서가 아니라 실제 사용 빈도를 반영합니다.

---

## ✨ 기능

|     | 기능                | 설명                                                                                                                                                                                         | 지원 플랫폼 |
| --- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| 📊  | **빈도 순위**       | 실제 사용량을 기반으로 매 세션마다 단축키 순서 재정렬                                                                                                                                        | Claude Code |
| 📌  | **상단 고정**       | 특정 스킬을 항상 맨 앞에 고정; ↑↓로 순서 변경 가능                                                                                                                                           | Claude Code |
| 🔮  | **연관 예측**       | 전체 사용 이력을 기반으로 다음에 사용할 스킬을 예측하여 표시                                                                                                                                 | Claude Code |
| 🌡   | **활동 히트맵**     | GitHub 스타일 그리드로 스킬 사용 현황 시각화; 기간 전환 가능                                                                                                                                 | Claude Code |
| 🕐  | **시간 패턴**       | 코딩을 가장 많이 하는 시간대와 요일별 분석                                                                                                                                                   | Claude Code |
| 📝  | **스킬 관리**       | 설치된 모든 스킬을 검색, 정렬, 설명 편집                                                                                                                                                     | Claude Code |
| 🚀  | **업그레이드 확인** | UI가 열릴 때마다 자동으로 업데이트를 확인; 브레이킹 변경과 패치 릴리스를 구분; 변경 내역을 인라인으로 표시하고 중요 업데이트 시 상단에 빨간 배너 표시; 원클릭으로 업그레이드하거나 닫기 가능 | Claude Code |
| 🚫  | **블랙리스트**      | 특정 스킬을 빈도 순위 및 단축키에서 제외; 스킬 탭에서 관리                                                                                                                                   | Claude Code |
| 🗂   | **로그 관리**       | 오래된 기록 자동 정리 (기본 30일); UI에서 N일 단위 정리 또는 전체 삭제                                                                                                                       | 전체        |
| 🌐  | **다국어 UI**       | 중국어, 영어, 독일어, 프랑스어, 러시아어, 한국어, 일본어 대시보드, 자동 감지                                                                                                                 | 전체        |
| 🔒  | **개인정보 우선**   | 스킬 이름, 시간, 세션 ID만 기록 — 프롬프트 내용은 절대 저장하지 않음                                                                                                                         | 전체        |
| 🔧  | **온디맨드 서버**   | 필요할 때 관리 UI를 시작하고, 탭을 닫으면 종료                                                                                                                                               | 전체        |

---

## 🔒 개인정보 보호

skill-habit은 프롬프트 내용, 파일 경로, 프로젝트 이름을 **절대 기록하지 않습니다**.

로그 항목은 다음과 같습니다 (`~/.skill-habit/skill-usage.log`):

```jsonc
{
  "v": 1,                    // 스키마 버전
  "ts": 1719360000,          // Unix 타임스탬프
  "skill": "git-smart",      // 이름만 — 그 뒤에 입력한 내용 제외
  "platform": "claude_code", // 스킬을 호출한 AI 도구
  "hour": 14,                // 시간대 (0–23)
  "weekday": 1,              // 0 = 월요일
  "session_id": "abc123",    // 연속적인 코딩 세션 식별자
  "session_skill_seq": 3,    // 세션 내 위치 (1, 2, 3…)
  "project_hash": "a3f2c1",  // 단방향 해시, 역추적 불가
  "args_len": 42             // 문자 수만, 내용은 저장 안 함
}
```

`log_retention_days`(기본값: 30)보다 오래된 로그 항목은 매 세션마다 자동으로 정리됩니다. **설정 → 데이터 관리**에서 일수를 입력(0 = 전체 삭제)하여 직접 정리할 수도 있습니다.

---

## 🚀 빠른 시작

> **요구 사항:** macOS 또는 Linux · Python 3.9+ · git
>
> **Windows:** 아직 네이티브 지원이 없습니다. [WSL](https://learn.microsoft.com/windows/wsl/)을 임시 방편으로 사용하세요.

### 설치

**옵션 A — Claude Code 플러그인 설치 (권장)**

```bash
claude plugins install github:kiss4u/skill-habit
```

설치 후 Claude Code를 재시작하면 즉시 추적이 시작됩니다.

**옵션 B — 한 줄 설치**

```bash
curl -sSL https://raw.githubusercontent.com/kiss4u/skill-habit/main/scripts/bootstrap.sh | bash
```

**옵션 C — pipx / pip**

> 참고: 이 방법은 내장 스킬(`/skill-habit:quick`, `/skill-habit:server` 등)을 자동으로 설치하지 않습니다. 옵션 A 또는 B를 권장합니다.

pipx (권장 — 격리된 환경 유지):
```bash
pipx install git+https://github.com/kiss4u/skill-habit
skill-habit install
```

pip:
```bash
pip install git+https://github.com/kiss4u/skill-habit
skill-habit install
```

> 새 Claude Code 세션을 시작하면 즉시 추적이 시작됩니다.

**다른 플랫폼**

Cursor, Codex CLI, Gemini CLI 등이 계획 중입니다. 어댑터 추가는 기여 섹션을 참고하세요.

**관리 UI 열기**

설치 후 아래 방법 중 하나로 대시보드를 열 수 있습니다:

Claude Code에서:
```bash
/skill-habit:server
```

pip / pipx 설치 시:
```bash
skill-habit server
```

bootstrap / 클론 설치 시:
```bash
python3 ~/.local/share/skill-habit/ui/server.py
```

브라우저가 자동으로 열립니다. 서버는 5분 동안 활동이 없으면 자동 종료됩니다.

---

### 업그레이드

설치와 동일한 명령어를 사용하세요 — 각 방법은 업그레이드를 자동으로 처리합니다:

**옵션 A — Claude Code 플러그인**

```bash
claude plugins update skill-habit
```

**옵션 B — 한 줄**

```bash
curl -sSL https://raw.githubusercontent.com/kiss4u/skill-habit/main/scripts/bootstrap.sh | bash
```

기존 설치에서 bootstrap을 다시 실행하면 `.git` 디렉토리를 감지하여 재클론 대신 `git pull`을 실행합니다.

**옵션 C — pipx / pip**

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

관리 UI의 **설정 → 버전 및 업그레이드** 패널에서 업데이트를 확인하고 원클릭으로 업그레이드할 수도 있습니다.

---

### 설정

**단축키 접두사**

**단축키 접두사**는 skill-habit이 생성하는 모든 단축키의 네임스페이스로, 기본값은 `sh`입니다. 매 세션마다 단축키는 다음 두 가지 모드 중 하나 또는 모두로 구성됩니다 (설정 가능):

| 모드       | 형식                    | 예시 (접두사 `sh`)        | 비고                                                                                          |
| ---------- | ----------------------- | ------------------------- | --------------------------------------------------------------------------------------------- |
| **숫자**   | `/<접두사><N×순위>`     | `/sh1`, `/sh22`, `/sh333` | 빈도순 정렬; `/sh1`은 항상 현재 최상위 스킬에 매핑; 연관 예측이 매 세션마다 최신 상태로 유지  |
| **명령어** | `/<접두사>-<스킬-이름>` | `/sh-git-smart`           | 이름으로 스킬을 직접 호출; Claude Code가 알파벳순으로 정렬하므로 빈도 순위는 위치에 영향 없음 |

**설정 → 일반 → 단축키 접두사**로 이동하여 새 값을 입력하고 저장하면 단축키가 즉시 재구성됩니다. UI에서 충돌을 실시간으로 감지하며, 입력창 아래에 충돌 없는 대안을 표시하여 클릭하여 적용할 수 있습니다.

**형식 규칙:** 영문자, 숫자, `-`, `_`만 사용 가능; 최대 5자.

**내장 스킬**

다음 관리 스킬은 플러그인으로 내장되어 있으며 접두사에 관계없이 항상 사용 가능합니다:

| 스킬                   | 설명                                | 사용 시점                                                                             |
| ---------------------- | ----------------------------------- | ------------------------------------------------------------------------------------- |
| `/skill-habit:quick`   | 현재 접두사와 숫자 단축키 매핑 표시 | 접두사나 숫자 단축키를 잊었을 때 확인. 출력 예: `접두사: sh`, `/sh1 → git-smart`      |
| `/skill-habit:server`  | 브라우저에서 웹 관리 UI 열기        | 설정 변경, 분석 조회, 스킬 관리; 브라우저 자동 열림, 5분 비활성 후 서버 자동 종료     |
| `/skill-habit:rebuild` | 즉시 단축키 재생성                  | `~/.skill-habit/config.json` 직접 편집 후 사용; Web UI에서 저장하면 자동으로 재생성됨 |
| `/skill-habit:version` | 설치된 버전 표시                    | 문제 해결이나 버그 신고 시 버전 확인                                                  |

**config.json**

`~/.skill-habit/config.json` — UI에서 편집하거나 직접 수정:

```jsonc
{
  "prefix": "sh",                      // 단축키 접두사: /sh-*
  "top_n": 10,                         // 세션당 생성되는 이름 단축키 최대 수
  "numeric_n": 5,                      // 숫자 단축키 최대 수 (sh1…shN)
  "time_window": "all",                // "today" | "week" | "month" | "all"
  "shortcut_mode": "both",             // "numeric" (/sh1) | "command" (/sh-<name>) | "both"
  "enable_sequence_prediction": true,  // 연관 예측
  "prediction_n": 5,                   // 최대 승격 후보 수 (1–5)
  "top_skills_n": 10,                  // 상위 스킬 차트 행 수
  "pinned_skills": [],                 // 빈도에 관계없이 항상 최상단
  "log_retention_days": 30,            // 롤링 보관 기간; 0 = 영구 보관
  "theme": "system",                   // "light" | "dark" | "system"
  "language": "auto",                  // "zh" | "en" | "de" | "fr" | "ru" | "ko" | "ja" | "auto"
  "analytics_cards": {
    "heatmap": true,                   // 활동 그리드
    "top_skills": true,                // 빈도 막대 차트
    "transition_graph": true,          // 연속 사용 패턴
    "hourly_distribution": true,       // 시간대별 활동
    "weekday_distribution": true       // 요일별 활동
  }
}
```

**🔮 연관 예측 (스마트 정렬)**

`enable_sequence_prediction`이 켜져 있으면, 각 세션 시작 시 시스템이:

1. 마지막으로 사용한 스킬을 읽습니다
2. 이력 전환 행렬을 조회하여 다음에 가장 많이 사용할 스킬 3개를 예측합니다
3. 해당 3개 스킬을 단축키 목록 상단으로 올립니다

효과는 단축키 모드에 따라 달라집니다:

| 모드                      | 효과                                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **숫자** (`/sh1 /sh2…`)   | 예측이 `sh1`/`sh2`에 어떤 스킬이 배치되는지 직접 변경합니다. `/sh1`을 입력하면 항상 추천 스킬이 실행됩니다. **완전히 효과적.** |
| **명령어** (`/sh-<name>`) | 메뉴 순서는 Claude Code에서 알파벳순으로 고정됨 — 예측은 **메뉴 순서에 영향을 주지 않습니다**.                                  |

> 데이터가 쌓일수록 정확도가 향상됩니다. 20회 이상 세션 후 의미 있는 결과를 얻을 수 있습니다.

**📐 숫자 단축키 순서**

Claude Code의 자동완성은 주로 **이름의 총 길이**로 제안을 정렬합니다 — 이름이 짧을수록 점수가 높고 먼저 표시됩니다. skill-habit은 각 순위 숫자를 N번 반복하여 **엄격하게 증가하는 이름 길이**를 가진 숫자 단축키를 생성합니다:

| 순위               | 단축키    | 길이 |
| ------------------ | --------- | ---- |
| 1 (가장 많이 사용) | `sh1`     | 2자  |
| 2                  | `sh22`    | 3자  |
| 3                  | `sh333`   | 4자  |
| 4                  | `sh4444`  | 5자  |
| 5                  | `sh55555` | 6자  |

이를 통해 드롭다운이 빈도 순서로 단축키를 표시하는 것이 보장됩니다. 사용 패턴이 변경되면 다음 세션 시작 시 단축키 할당이 자동으로 업데이트됩니다.

호출 방법: `/sh1`을 직접 입력하거나, `/sh2`(퍼지 매칭으로 `sh22` 선택)를 입력하고 Enter를 누릅니다.

---

## 🖥 관리 플랫폼

### 🗂 스킬 관리

<a href="../assets/screenshot-skills.png"><img src="../assets/screenshot-skills.png" width="800" alt="Skills tab"></a>

**스킬** 탭을 열면:

- **검색 및 정렬** — 이름/설명으로 필터링; 사용 횟수, 최근 사용일, 이름으로 정렬 (같은 버튼을 다시 클릭하면 역순)
- **설명 편집** — 설명을 더블클릭하여 인라인 편집（또는 마우스를 올리면 나타나는 ✏️ 아이콘 클릭）; Enter 또는 다른 곳 클릭 시 저장, Esc로 취소
- **스킬 고정** — 스킬을 고정하여 단축키 목록 최상단에 배치; ↑↓로 고정된 스킬 순서 변경
- **스킬 블랙리스트** — 행의 **차단** 버튼을 클릭하여 빈도 순위 및 단축키에서 제외; 탭 하단의 접을 수 있는 블랙리스트 섹션에서 목록 관리 (보기, 페이지 이동, 차단 해제)
- **사용 이력** — 각 스킬의 사용 횟수와 마지막 사용 시간 확인

> 스킬 탭에는 한 번 이상 사용한 스킬만 표시됩니다. 스킬은 `~/.claude/skills/`와 모든 설치된 플러그인에서 가져옵니다.

### 📊 통계

<a href="../assets/screenshot-analytics.png"><img src="../assets/screenshot-analytics.png" width="800" alt="Analytics tab"></a>

**통계** 탭에는 다음이 포함됩니다:

- **활동 히트맵** — GitHub 스타일 그리드; 각 셀 = 해당 날의 스킬 호출 횟수; 기간 전환 가능
- **상위 스킬** — 선택한 기간(오늘 / 주 / 월 / 전체)의 바 차트
- **시간대 분포** — 하루 중 스킬을 사용하는 시간대
- **요일 분포** — 가장 열심히 코딩하는 요일
- **전환 그래프** — 어떤 스킬을 연속으로 사용하는지 (예측 모델에 활용)

모든 카드는 설정에서 개별적으로 켜고 끌 수 있습니다.

### 🛠 설정 메뉴

<a href="../assets/screenshot-settings.png"><img src="../assets/screenshot-settings.png" width="800" alt="Settings tab"></a>

**설정** 탭에는 세 가지 카드가 있으며, 변경 사항은 즉시 적용됩니다:

**일반**

| 설정                 | 설명                                                                                |
| -------------------- | ----------------------------------------------------------------------------------- |
| 단축키 프리픽스      | 모든 단축 스킬의 네임스페이스, 기본값 `sh`; 실시간 충돌 감지 및 충돌 없는 대안 제안 |
| 기간                 | 빈도 순위 기준 기간: 전체 / 최근 6개월 / 이번 달 / 이번 주 / 오늘                   |
| 단축키 모드          | 활성화할 단축키 유형: 숫자형（`/sh1`）, 이름형（`/sh-name`）또는 둘 다              |
| 숫자 단축키 수       | 생성되는 숫자 단축키의 최대 수량 (1–9)                                              |
| 이름 단축키 수       | 생성되는 이름 단축키의 최대 수량                                                    |
| 상위 스킬 차트 행 수 | Analytics 상위 스킬 막대 차트에 표시되는 스킬 수                                    |
| 재구성 간격          | 자동 단축키 재구성까지의 비활성 시간 (분)                                           |
| 시퀀스 예측          | 사용 이력을 기반으로 다음 스킬을 예측하고 상위로 이동                               |
| 예측 깊이            | 시퀀스 예측이 올릴 수 있는 스킬 수 (1–5)                                            |
| 테마                 | 라이트 / 다크 / 시스템                                                              |
| 언어                 | UI 언어: 자동 / 中文 / English / Deutsch / Français / Русский / 한국어 / 日本語     |
| 분석 카드 토글       | 히트맵, 상위 스킬, 전이 그래프, 시간별·요일별 분포를 개별 켜기/끄기                 |

**데이터 관리**

| 설정           | 설명                                                                        |
| -------------- | --------------------------------------------------------------------------- |
| 로그 보관 일수 | 롤링 보관 기간 (0 = 영구 보관); 일수 입력으로 이전 기록 정리 또는 전체 삭제 |

**버전 및 업그레이드**

| 상태                   | 동작                                                                  |
| ---------------------- | --------------------------------------------------------------------- |
| 업데이트 없음          | 조용히 확인, 알림 없음                                                |
| 패치 업데이트          | 이 카드에만 황색 알림 — 배너 없음                                     |
| 메이저/마이너 업데이트 | 페이지 상단에 변경 내역이 담긴 빨간 배너; 원클릭 업그레이드 또는 닫기 |

---

## 🌐 플랫폼 지원

| 플랫폼         | 상태      |
| -------------- | --------- |
| Claude Code    | ✅ v0.0.1 |
| Cursor         | 🔜 예정   |
| Codex CLI      | 🔜 예정   |
| Gemini CLI     | 🔜 예정   |
| GitHub Copilot | 🔜 예정   |
| OpenCode       | 🔜 예정   |
| Windsurf       | 🔜 예정   |

---

## 🤝 기여하기

1. 이 저장소를 포크하세요
2. `adapters/`에서 플랫폼을 선택하세요 (또는 새로운 플랫폼을 제안하세요)
3. `adapters/base.py`의 세 가지 메서드를 구현하세요
4. PR을 열어주세요

---

## 📄 라이선스

MIT © [kiss4u](https://github.com/kiss4u)
