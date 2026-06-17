---
name: team-knowledge
description: "Share, consolidate, and version-control Hermes skills, memory, and profiles across a team or organization — covering Profile Distributions, External Skill Directories, multi-profile Kanban workflows, and skill-collaboration patterns for collective wisdom."
author: Hermes Agent
version: 1.1.0
created_by: agent
platforms: [linux, macos]
metadata:
  hermes:
    tags: [team, collaboration, knowledge-sharing, profiles, distributions, kanban, skills, collective-wisdom]
    related_skills: [hermes-agent, codex-cli, ai-coding-clis]
---

# Team Knowledge Management for Hermes

How to run Hermes in a team/group setting, share knowledge between members, and consolidate multiple people's skills into collective wisdom.

## Overview

Hermes has three layers of knowledge that can be shared across a team:

| Layer | What | Sharing mechanism | Cross-machine migration |
|-------|------|-------------------|------------------------|
| **Skills** | Reusable workflows (SKILL.md) | Git repo, External Skill Dirs, Skills Hub | `tar czf` → copy → extract at `~/.hermes/skills/` |
| **Memory** | User preferences + environment facts | File copy (per-profile) | Copy `MEMORY.md` + `USER.md` files directly |
| **Profile** | Full agent (config + skills + personality + MCP + cron) | Profile Distribution (git) | `hermes profile export` → copy → `hermes profile import` |
| **Kanban** | Multi-agent task board | Shared SQLite DB + dispatcher | Copy the `.kanban/` directory |

## Pattern 0: Cross-Machine Migration (Before Joining a Team)

When moving a personal Hermes agent to a new machine or onboarding a teammate's existing skills/memory:

### Skills: File-Level Copy

```bash
# Source machine: package all local skills (skip bundled builtins)
tar czf my-skills.tar.gz -C ~/.hermes skills/

# Target machine: extract (will merge with any existing skills)
tar xzf my-skills.tar.gz -C ~/.hermes/

# Or selectively copy a single skill folder
cp -r old-machine-skills/my-deploy-skill ~/.hermes/skills/
```

⚠️ **Only copy your own custom skills** (those with `source: local` or `created_by: agent`). Bundled builtins (source: `builtin`) are already on every Hermes install — overwriting them with an old copy causes conflicts on `hermes update`.

### Memory: Direct File Copy

```bash
# Source machine
scp user@old-machine:~/.hermes/MEMORY.md /tmp/hermes-memory/
scp user@old-machine:~/.hermes/USER.md /tmp/hermes-memory/

# Target machine
cp /tmp/hermes-memory/MEMORY.md ~/.hermes/
cp /tmp/hermes-memory/USER.md ~/.hermes/
```

For named profiles, the files are at `~/.hermes/profiles/<name>/MEMORY.md` and `USER.md`.

### Profile: Full Export/Import (Config + Skills + MCP + Cron)

```bash
# Source
hermes profile export default -o hermes-full-profile.tar.gz

# Copy archive to target, then:
hermes profile import hermes-full-profile.tar.gz
```

**Note:** `.env` credentials (API keys) are NOT included in the export. Copy `.env` separately or re-run `hermes model` / `hermes auth add` on the target machine.

## Feishu (Lark) Group Deployment — Configuration & Pitfalls

When running Hermes in a **Feishu group** (the most common Chinese team setup), these settings in `.env` control authorization and group behavior:

| Env Variable | Values | Effect |
|---|---|---|
| `FEISHU_ALLOW_ALL_USERS` | `true` / `false` (default) | `true` = anyone in the group can talk to the bot; `false` = only users in `FEISHU_ALLOWED_USERS` |
| `FEISHU_ALLOWED_USERS` | Comma-separated Feishu user IDs (`ou_xxx`) | Whitelist of authorized users when `ALLOW_ALL_USERS=false` |
| `FEISHU_GROUP_POLICY` | `open` / `closed` | `open` = bot responds in group chats; `closed` = DM only |
| `FEISHU_HOME_CHANNEL` | Feishu user or chat ID | The "home" channel where shutdown notifications etc. are sent |

### Group vs DM Session Isolation (Critical Pitfall)

**Skills created in a DM session are NOT visible to an ongoing group session.** This is the most common cause of user frustration — the user tells the group bot "use the skill I just created in DM," but the group session started before the skill existed and doesn't reload.

**How to resolve it:**

1. **Best approach:** Handle the task from the DM session directly, then `send_message` the result to the group — bypasses the isolation issue entirely.
2. **In the group:** Send a fresh message on a new topic thread → creates a new session that sees all installed skills.
3. **Gateway restart** forces all sessions to reset:
   ```bash
   systemctl --user restart hermes-gateway
   ```
4. **For CLI:** `/reload-skills` re-scans the skills directory mid-session.

### Gateway Restart After Config Changes

After modifying `.env` (Feishu settings, API keys, etc.) the gateway must be restarted — config is read at startup:

```bash
systemctl --user restart hermes-gateway
```

The gateway uses `Restart=on-failure` in systemd, so crashes during restart are self-healing.

### Authorization Flow

The gateway checks authorization in this order:
1. Is `FEISHU_ALLOW_ALL_USERS=true`? → Allow.
2. Is the sender's Feishu user ID in `FEISHU_ALLOWED_USERS`? → Allow.
3. Otherwise → Silently ignore the message (no response).

### Standard Feishu Setup

Feishu WebSocket mode (no callback URL needed):

```env
FEISHU_APP_ID=cli_xxxxxxxxxxxx
FEISHU_APP_SECRET=...
FEISHU_DOMAIN=feishu                       # "feishu" for feishu.cn, "lark" for larksuite.com
FEISHU_CONNECTION_MODE=websocket           # preferred — simpler than webhook
FEISHU_GROUP_POLICY=open                   # enable group chat responses
FEISHU_ALLOW_ALL_USERS=true                # open to all group members
```

## Pattern 1: One Bot, One Group (Simplest)

The most common setup for teams:

```
1 server running Hermes Gateway
  └── connected to Feishu / Telegram / Discord / Slack
  └── all team members interact in the same group
  └── bot accumulates skills over time as the team uses it
```

The bot's skills file (`~/.hermes/skills/`) grows organically. When the agent solves a complex problem, it saves it as a skill. Future sessions load it automatically (progressive disclosure).

**Best for:** Small teams, single-purpose assistants.

## Pattern 2: Profile Distributions (Git-Based Sharing — Recommended)

The official way to package a complete Hermes agent for sharing. A **profile distribution** is a git repository containing config, skills, personality, MCP connections, and cron jobs — everything except secrets and session data.

### Team repo structure

```
team-knowledge/
├── distribution.yaml        # manifest: name, version, env-var requirements
├── SOUL.md                  # team personality / system prompt
├── .env.EXAMPLE             # template for required env vars
├── config.yaml              # hermes config (no secrets)
├── skills/
│   ├── deploy-service/      # deployment skill
│   │   └── SKILL.md
│   ├── code-review/         # code review skill
│   │   ├── SKILL.md
│   │   └── references/      # support files
│   └── api-design/
│       └── SKILL.md
├── mcp_servers/             # MCP server scripts
└── cron/                    # scheduled job definitions
```

### Install flow

```bash
# Team member installs the shared agent
hermes profile install team-agent git@github.com:org/team-knowledge.git

# Now they have a new profile:
team-agent chat                  # talk to the shared agent
team-agent --profile team-agent  # use it in commands

# When the team updates skills:
hermes profile update team-agent
# → pulls latest skills + config (personal memories/sessions stay untouched)
```

### Collaboration workflow

```
小王改进 deploy-skill → git add → commit → push → PR
小李 review → approve → merge to main
小张: hermes profile update team-agent → 自动同步
```

**Benefits:**
- ✅ Version history (git)
- ✅ Code review on skill changes
- ✅ Easy rollback
- ✅ Personal memories/sessions isolated from shared skills

## Pattern 3: External Skill Directories (No-Git Alternative)

Point Hermes at a shared network directory to scan for skills:

```yaml
# config.yaml
external_skill_dirs:
  - /mnt/team-share/hermes-skills/   # NAS / shared drive
  - /home/ubuntu/shared-skills/      # git clone of team repo
```

Hermes scans these directories at startup for SKILL.md files and loads them alongside local skills.

**Best for:** Teams without git experience, or read-only consumption.

## Pattern 4: Kanban Multi-Agent Board (Task Routing)

For teams running multiple specialized Hermes profiles, the Kanban board provides durable task routing:

```
                         ┌────────────────┐
                         │  Kanban Board  │
                         │  kanban.db     │
                         └───────┬────────┘
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │ worker-coder     │ │ worker-research  │ │ worker-ops      │
    │ profile: coder   │ │ profile: search  │ │ profile: ops    │
    │ skills: code     │ │ skills: arxiv    │ │ skills: deploy  │
    │ gateway: discord │ │ gateway: cli     │ │ gateway: slack  │
    └─────────────────┘ └─────────────────┘ └─────────────────┘
```

- Each profile has a `--description` (e.g. "Python backend developer") so the orchestrator knows what to route
- Workers claim tasks atomically via `kanban_claim`
- Tasks have `max_retries` to prevent infinite failure loops

See `hermes profile create` and `hermes profile describe` for worker setup.

## Consolidating Multiple People's Skills

When different team members write skills for the same topic (e.g. "deployment"):

### Option A: Multiple co-existing skills

```
~/.hermes/skills/
├── deploy-wang/       # Wang's deployment approach
│   └── SKILL.md
├── deploy-li/         # Li's deployment approach
│   └── SKILL.md
└── deploy-v3/         # Team-consolidated version
    └── SKILL.md
```

Hermes loads the most relevant one based on context. The **Curator** (auto-maintenance) tracks usage and marks stale duplicates for archival.

### Option B: Merge into one canonical skill (Recommended)

```
1. Create a shared team repo
2. Each person contributes their approach
3. Team discusses → merges the best parts
4. Single canonical skill emerges (SKILL.md with references/)
5. Others delete their personal versions
```

The standard SKILL.md format (YAML frontmatter + markdown body) is designed for PR-style collaboration — diffs are meaningful and reviewable.

### Option C: Version tags via distribution

```
distribution.yaml
  version: 2.1.0         # semantic versioning
  skills:
    deploy: 2.1.0        # per-skill versioning
    review: 1.3.0
```

`hermes profile update` only pulls changed skills.

## Pitfalls

| Pitfall | Solution |
|---------|----------|
| Memory is per-profile, not shared | Memory only exists in `MEMORY.md`/`USER.md` — copy these manually between machines |
| `.env` contains secrets — don't commit | Use `.env.EXAMPLE` in the repo; each member copies and fills their own |
| Skills grow stale if nobody maintains them | Enable the Curator (`hermes curator run`). It auto-archives unused skills |
| Kanban dispatcher needs a running gateway | Set `kanban.dispatch_in_gateway: true` in config |
| `hermes profile install` vs `hermes profile create` confusion | `install` = from a distribution repo; `create` = blank or clone local |
| Device-code auth must keep polling | Use background process with `notify_on_complete=true` (see `ai-coding-clis` skill) |
| Overwriting bundled builtins on migration | Only tar/copy skills with `source: local` or `created_by: agent` provenance. Bundled skills (`source: builtin`) are restored by Hermes on every update — overwriting them causes merge conflicts. Run `hermes skills list` to check provenance. |
| `.env` not exported with `hermes profile export` | Export excludes secrets by design. Copy `.env` manually or re-authenticate on the target machine. |

## Related Skills

- `hermes-agent` — full Hermes CLI reference, MCP setup, profiles
- `codex-cli` / `ai-coding-clis` — installing and authenticating third-party coding tools

## Reference Files

- `references/team-setup-patterns.md` — Session notes from Chinese-speaking team setup conversations (Feishu context, skill consolidation preferences)
- `references/skill-examples-catalog.md` — Catalog of what skills teams typically build, organized by category with Chinese team notes
