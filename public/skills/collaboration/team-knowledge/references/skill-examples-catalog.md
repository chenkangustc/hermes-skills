# Team Skill Examples Catalog

What skills teams actually build on Hermes — organized by category. Use this as inspiration when deciding what to save as a skill for your team.

## 1. Software Development Skills (Most Popular)

| Skill | When it applies | Typical team adoption |
|-------|----------------|-----------------------|
| **Plan** / **Spike** | Starting any non-trivial feature | High — teams standardise on one of these for RFCs |
| **Test-Driven Development** | Python/Node backend work | Medium — teams that already practice TDD |
| **Systematic Debugging** | Root-causing production incidents | High — especially on-call teams |
| **Code Review** | Pre-merge PR checks (security scan + quality gates) | High — integrated into CI |
| **Deployment** | Custom deploy to specific infra (k8s, Docker, serverless) | Medium — very team-specific |
| **API Design** | REST/gRPC contract-first development | Medium — useful for standardization |

## 2. Productivity & Document Skills

| Skill | When it applies | Notes |
|-------|----------------|-------|
| **nano-pdf** | Fixing typos/titles in PDFs before release | Quick win — one-liner |
| **ocr-and-documents** | Extracting text from scanned contracts/receipts | Common in Chinese teams using Feishu |
| **powerpoint** | Auto-generating slide decks from meeting notes | Growing adoption |
| **architecture-diagram** | Drawing SVG infra diagrams for docs | Medium adoption |

## 3. Research & Knowledge Skills

| Skill | When it applies | Notes |
|-------|----------------|-------|
| **arxiv** | Paper discovery by keyword/author | Academic teams |
| **market-research** | Competitor analysis, trend monitoring | Teams that pair with cron jobs |
| **tech-radar** | Tracking internal tech decisions over time | Growing |

## 4. Team & Collaboration Skills

| Skill | When it applies | Notes |
|-------|----------------|-------|
| **team-knowledge** | Onboarding new members, sharing profiles | Foundational — every team should have this |
| **standup-summary** | Auto-summarizing daily standups from chat | Popular in chat-heavy teams (Feishu/Discord) |
| **retro-notes** | Structuring sprint retrospectives | Medium |

## 5. Operations & Automation Skills

| Skill | When it applies | Notes |
|-------|----------------|-------|
| **cron-monitor** | Watchdog for disk/memory/GPU thresholds | Pairs with `no_agent=True` cron scripts |
| **log-digest** | Summarising error logs into daily briefings | Used by SRE teams |
| **pr-summary** | Auto-generating PR descriptions from diff | Medium adoption |
| **release-notes** | Compiling changelog from merged PRs | Medium |

## 6. Domain-Specific Skills (Chinese Teams)

Chinese teams using Hermes via Feishu/WeCom/DingTalk often build:

- **飞书日报** — Auto-generate daily team reports from Feishu messages
- **审批提醒** — Monitor and notify on pending approval workflows
- **竞品监控** — Cron-based competitor website/content monitoring
- **代码审查标准** — Team-specific coding standards enforced at PR time (PEP 8, ESLint configs)
- **中间件管理** — Custom skills for Redis / MySQL / Kafka health checks (team-internal tooling)
- **API Key 轮换** — Rotating credentials on a schedule

## How Teams Decide What to Skill-ify

1. **Repetition heuristic** — if someone asks "how do we do X" more than twice, save it
2. **Correction heuristic** — every time you fix a mistake in a workflow, the fix belongs in a skill
3. **Onboarding heuristic** — everything a new team member needs to ask about → skill
4. **Script risk heuristic** — any ad-hoc script that's critical when it breaks → skill with test/verify steps
