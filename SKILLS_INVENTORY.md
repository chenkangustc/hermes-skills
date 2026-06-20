# Hermes Agent 技能知识库清单 📋

> 仓库：`chenkangustc/hermes-skills`
> 最后更新：2026-06-20
> 已重命名：知识库 → 技能库

---

## 目录结构

```
hermes-skills/
├── public/          # 📖 公用技能库 — Hermes 默认技能
│   └── skills/     #    技能文件（按分类组织）
│       ├── autonomous-ai-agents/
│       ├── collaboration/
│       ├── creative/
│       ├── data-science/
│       ├── dogfood/
│       ├── email/
│       ├── github/
│       ├── media/
│       ├── mlops/
│       ├── note-taking/
│       ├── productivity/
│       ├── research/
│       ├── smart-home/
│       ├── social-media/
│       └── software-development/
├── private/         # 🔒 专用技能库 — 个人开发的技能
│   └── productivity/
├── SKILLS_INVENTORY.md  # 本文 — 技能清单
└── README.md             # 仓库总说明
```

---

## 🗂️ 技能总览（按分类）

### 1️⃣ autonomous-ai-agents — 自主 AI 智能体

> Skills for spawning and orchestrating autonomous AI coding agents and multi-agent workflows — running independent agent processes, delegating tasks, and coordinating parallel workstreams.

| 技能名 | 说明 | 版本 | 路径 |
|--------|------|------|------|
| **codex-cli** | Install, authenticate, and integrate OpenAI Codex CLI with Hermes Agent as an MCP server. | — | `public/skills/autonomous-ai-agents/codex-cli/` |
| **hermes-agent** | Configure, extend, or contribute to Hermes Agent. | v2.1.0 | `public/skills/autonomous-ai-agents/hermes-agent/` |

---

### 2️⃣ collaboration — 团队协作

> Share, consolidate, and version-control Hermes skills, memory, and profiles across a team or organization — covering Profile Distributions, External Skill Directories, multi-profile Kanban workflows, and skill-collaboration patterns for collective wisdom.

| 技能名 | 说明 | 版本 | 路径 |
|--------|------|------|------|
| **team-knowledge** | Share, consolidate, and version-control Hermes skills, memory, and profiles across a team. | — | `public/skills/collaboration/team-knowledge/` |

---

### 3️⃣ creative — 创意创作

> Creative content generation — ASCII art, hand-drawn style diagrams, and visual design tools.

| 技能名 | 说明 | 版本 | 路径 |
|--------|------|------|------|
| **architecture-diagram** | Dark-themed SVG architecture/cloud/infra diagrams as HTML. | — | `public/skills/creative/architecture-diagram/` |
| **humanizer** | Humanize text: strip AI-isms and add real voice. | — | `public/skills/creative/humanizer/` |

---

### 4️⃣ dogfood — 内测 QA

> Exploratory QA of web apps: find bugs, evidence, reports.

| 技能名 | 说明 | 版本 | 路径 |
|--------|------|------|------|
| **dogfood** | Exploratory QA of web apps: find bugs, evidence, reports. | — | `public/skills/dogfood/` |

---

### 5️⃣ github — GitHub 工作流

> GitHub workflow skills for managing repositories, pull requests, code reviews, issues, and CI/CD pipelines using the gh CLI and git via terminal.

| 技能名 | 说明 | 版本 | 路径 |
|--------|------|------|------|
| **codebase-inspection** | Inspect codebases w/ pygount: LOC, languages, ratios. | — | `public/skills/github/codebase-inspection/` |

---

### 6️⃣ productivity — 效率工具

> Skills for document creation, presentations, spreadsheets, and other productivity workflows.

| 技能名 | 说明 | 版本 | 路径 |
|--------|------|------|------|
| **gongwen-paiban** | 中国公文排版规范（7条铁律）：字体、字号、页面设置、行距、页边距等全套规范。 | — | `private/productivity/gongwen-paiban/` |
| **official-document-layout-designer** | Format, clean up, and visually QA Chinese official-document-style Word files and report drafts. | — | `private/productivity/official-document-layout-designer/` |
| **maps** | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. | — | `public/skills/productivity/maps/` |
| **nano-pdf** | Edit PDF text/typos/titles via nano-pdf CLI (NL prompts). | — | `public/skills/productivity/nano-pdf/` |
| **ocr-and-documents** | Extract text from PDFs/scans (pymupdf, marker-pdf). | — | `public/skills/productivity/ocr-and-documents/` |
| **powerpoint** | Create, read, edit .pptx decks, slides, notes, templates. | — | `public/skills/productivity/powerpoint/` |

---

### 7️⃣ research — 学术研究

> Skills for academic research, paper discovery, literature review, domain reconnaissance, market data, content monitoring, and scientific knowledge retrieval.

| 技能名 | 说明 | 版本 | 路径 |
|--------|------|------|------|
| **arxiv** | Search arXiv papers by keyword, author, category, or ID. | — | `public/skills/research/arxiv/` |

---

### 8️⃣ software-development — 软件开发

> Core development skills for planning, debugging, testing, code review, AI CLI integration, and skill authoring.

| 技能名 | 说明 | 版本 | 路径 |
|--------|------|------|------|
| **ai-coding-clis** | Install, authenticate, and configure third-party AI coding CLI tools (Codex, Claude Code, OpenCode, etc.). | — | `public/skills/software-development/ai-coding-clis/` |
| **hermes-agent-skill-authoring** | Author in-repo SKILL.md: frontmatter, validator, structure. | — | `public/skills/software-development/hermes-agent-skill-authoring/` |
| **node-inspect-debugger** | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. | — | `public/skills/software-development/node-inspect-debugger/` |
| **plan** | Plan mode: write an actionable markdown plan to .hermes/plans/, no execution. | — | `public/skills/software-development/plan/` |
| **python-debugpy** | Debug Python: pdb REPL + debugpy remote (DAP). | — | `public/skills/software-development/python-debugpy/` |
| **requesting-code-review** | Pre-commit review: security scan, quality gates, auto-fix. | — | `public/skills/software-development/requesting-code-review/` |
| **spike** | Throwaway experiments to validate an idea before build. | — | `public/skills/software-development/spike/` |
| **systematic-debugging** | 4-phase root cause debugging: understand bugs before fixing. | — | `public/skills/software-development/systematic-debugging/` |
| **test-driven-development** | TDD: enforce RED-GREEN-REFACTOR, tests before code. | — | `public/skills/software-development/test-driven-development/` |

---

### 9️⃣ 其他分类（暂未包含技能，仅有分类目录）

以下分类目录已存在，可作为知识库骨架，待后续填充技能：

| 分类 | 说明 |
|------|------|
| **apple** | Apple / macOS skills — tools that interact with the Mac desktop (Finder, native apps) or system features. |
| **data-science** | Skills for data science workflows — interactive exploration, Jupyter notebooks, data analysis, and visualization. |
| **email** | Skills for sending, receiving, searching, and managing email from the terminal. |
| **media** | Skills for working with media content — YouTube transcripts, GIF search, music generation, and audio visualization. |
| **mlops** | Knowledge and Tools for Machine Learning Operations — training, fine-tuning, deploying, and optimizing ML/AI models. |
| **note-taking** | Note taking skills, to save information, assist with research, and collab on multi-session planning. |
| **smart-home** | Skills for controlling smart home devices — lights, switches, sensors, and home automation systems. |
| **social-media** | Skills for interacting with social platforms — posting, reading, monitoring, and account operations. |

---

## 📊 统计

| 指标 | 数值 |
|------|------|
| 总技能数 | **23** |
| 有技能的分类 | 8 |
| 空分类（骨架） | 8 |
| 公用技能库 📖 | `public/skills/` — 21 个技能已就位 |
| 专用技能库 🔒 | `private/` — 2 个技能 (gongwen-paiban, official-document-layout-designer) |

---

## 🚀 使用方式

### 在 Hermes 中引用公用技能
```yaml
# 方式 1：通过 External Skill Directory 配置
skill_directories:
  - https://raw.githubusercontent.com/chenkangustc/hermes-skills/main/public/skills/

# 方式 2：手动下载到本地
cd ~/.hermes/skills/
git clone https://github.com/chenkangustc/hermes-skills.git repo-skills
ln -s repo-skills/public/skills/* ./
```

### 添加专用技能
1. 在 `private/` 目录下按分类创建技能文件夹
2. 每个技能包含 `SKILL.md`（YAML frontmatter + 说明）
3. 可选：`references/`、`templates/`、`scripts/` 等辅助目录
4. 提交 PR 或直接 push
