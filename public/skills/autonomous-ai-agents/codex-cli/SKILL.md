---
name: codex-cli
description: "Install, authenticate, and integrate OpenAI Codex CLI with Hermes Agent as an MCP server."
author: Hermes Agent (auto-generated)
version: 1.0.0
created_by: agent
metadata:
  hermes:
    tags: [codex, openai, mcp, coding-agent, setup, integration]
    related_skills: [hermes-agent]
---

# OpenAI Codex CLI — Setup & Hermes Integration

OpenAI Codex CLI is a terminal-based coding agent similar to Claude Code. This skill covers installing it, authenticating via device-code OAuth, and integrating it as an MCP server inside Hermes Agent so Hermes can delegate coding tasks to Codex.

## Installation

Codex requires Node.js/npm. Install it to a user-writable location to avoid EACCES:

```bash
npm install -g @openai/codex --prefix ~/.local
```

The binary lands at `~/.local/bin/codex`. Add it to PATH if not already there.

Verify:
```bash
~/.local/bin/codex --version
~/.local/bin/codex doctor
```

## Authentication (Device Code Flow)

Codex CLI uses OpenAI/ChatGPT auth via device-code OAuth. The `--device-auth` flag prints a URL + one-time code and then **polls** until the user completes the flow.

**Key pitfall:** if you run `codex login --device-auth` with a short timeout, the process exits before the polling completes and the user's browser auth is wasted. Always start the polling process in the **background** so it lives long enough:

```bash
# Step 1: Get a fresh URL + code (capture the output)
timeout 15 ~/.local/bin/codex login --device-auth 2>&1 || true

# Step 2: Give user the URL and code + instructions
#   URL: https://auth.openai.com/codex/device
#   Code: XXXXX-XXXXX  (15-minute expiry)

# Step 3: Start background polling process
terminal(
  command="~/.local/bin/codex login --device-auth",
  background=True,
  notify_on_complete=True,
  timeout=600
)
```

The user opens the URL, enters the code, signs in with Google/email, and the background process picks up the token and saves it.

Verify:
```bash
codex login status
# Expected: "Logged in using ChatGPT"
```

### Check auth

```bash
codex login status          # should say "Logged in using ChatGPT"
codex login --device-auth   # (if not logged in)
```

## Hermes MCP Integration

Codex CLI includes an MCP server mode (`codex mcp-server`) that exposes two tools:
- `codex` — start a Codex session
- `codex-reply` — continue an existing session by thread ID

### 1. Create a wrapper script

The `hermes mcp add` command passes command + args separately. Create a small wrapper to avoid quoting issues:

```bash
cat > ~/.local/bin/codex-mcp.sh << 'EOF'
#!/bin/bash
exec /home/ubuntu/.local/bin/codex mcp-server "$@"
EOF
chmod +x ~/.local/bin/codex-mcp.sh
```

### 2. Add the MCP server

Non-interactive (pipe "Y" to auto-confirm tool enablement):

```bash
echo "Y" | hermes mcp add codex \
  --command /home/ubuntu/.local/bin/codex-mcp.sh
```

### 3. Verify

```bash
hermes mcp list
# Should show: codex  ... all  ✓ enabled
```

### 4. Using the tools

The tools are injected into all platform toolsets **on next session start**. Run `/reset` in an active chat or start a fresh `hermes` session. The tools appear as:
- `mcp_codex_codex`
- `mcp_codex_codex_reply`

## Using Codex MCP Tools Directly (CRITICAL)

Once integrated, Codex MCP tools (`mcp_codex_codex`, `mcp_codex_codex_reply`) are available for research, coding, and web-searching tasks.

**IMPORTANT — use the MCP tools directly when the user asks for Codex.** Do not substitute `browser_navigate`, `delegate_task`, or web tools when the user says "use Codex to search" or "\u7528Codex\u5e2e\u6211\u641c\u7d22". Use `mcp_codex_codex` instead. Failing to use the user's specified tool is a workflow error, not a minor optimization.

### Effective prompt patterns

Codex MCP calls have a configurable timeout (default 120s). Raise it via `hermes config set mcp_servers.codex.timeout <seconds>` if tasks routinely exceed 120s.

| Pattern | Example | Why it works |
|---------|---------|-------------|
| **Concise prompt with specific sources** | `Search https://hermes-agent.docs and summarize X, Y, Z` | Gives Codex clear bounds; shorter prompts complete before timeout |
| **Narrow scope** | Instead of "search everything about X", say: `Search Hermes docs for: 1) profiles 2) kanban 3) skills system` | Avoids timeout from overbroad exploration |
| **Structured output** | `Return a table with columns: topic, key finding, source URL` | Keeps output focused, reduces token waste |

### Timeout handling

**Priority order — try these in order:**

1. **Increase MCP timeout via config (best for recurring tasks):**
   ```bash
   hermes config set mcp_servers.<name>.timeout <seconds>
   # Example: raise Codex MCP timeout from default 120s to 300s
   hermes config set mcp_servers.codex.timeout 300
   ```
   This is set in `~/.hermes/config.yaml` under `mcp_servers.<name>.timeout`. It's a per-MCP-server setting, so `codex`, `filesystem`, etc. each can have their own timeout. Restart the Hermes session for the change to take effect (run `/reset` or start a new session).

2. **Shorten the prompt** — remove vague instructions, be explicit about 2-3 sources
3. **Include specific URLs** instead of asking Codex to discover them
4. **Split one large query into 2-3 smaller ones**
5. **Retry with a more focused prompt**

**Long-running apt-get operations** (installing 5+ packages, downloading fonts, etc.) often hit the MCP timeout. Workaround:
  - Use `terminal()` directly instead of Codex for `apt-get install`
  - Or break into smaller commands (one package at a time with `timeout 30`)

For detailed usage transcript, see `references/mcp-research-workflow.md`.

## Hermes-as-Gateway / Codex-as-Executor Pattern

**This user operates a strict delegation model:** Hermes is only the interaction gateway (receives requests, delivers results). All actual task execution — coding, PDF generation, font installation, file operations, research — is delegated to Codex CLI via `mcp_codex_codex`.

### Why

- **Token cost optimization:** DeepSeek tokens are expensive for heavy tool calls. Codex (GPT-5.5) handles computation-heavy work, Hermes (DeepSeek) handles only orchestration.
- **Separation of concerns:** Hermes manages conversation flow and platform delivery; Codex handles execution without bloating Hermes's context window with tool output.

### Correct invocation sequence

```
User request → Hermes → mcp_codex_codex(prompt=..., sandbox="danger-full-access") → Codex executes → Hermes delivers result
```

### Prompt patterns that work well with this model

| Do | Don't |
|----|-------|
| Give Codex a self-contained task with all context | Make Codex re-read Hermes messages for context |
| Include file paths, exact commands, and server-specific details in the prompt | Leave paths ambiguous ("install fonts" without specifying which ones) |
| Set `cwd=/home/ubuntu` so relative paths resolve | Assume Codex knows the working directory |
| Use `sandbox=danger-full-access` for system-level tasks (apt-get, font config, etc.) | Use read-only sandbox for tasks that need to install packages |

### Pitfalls

| Pitfall | Fix |
|---------|-----|
| **MCP timeout (120s)** on apt-get or `sudo` operations | **First try:** `hermes config set mcp_servers.codex.timeout 300` to raise the limit. If that's not enough, break into smaller steps, or use `terminal()` directly for long-running operations. |
| **Duplicate sudo lock** when Hermes and Codex both try apt-get | Check `ps aux | grep apt` before starting a Codex task. Kill stale processes or wait for them. |
| **No context inheritance** | Codex sessions are fully independent. Include all needed paths, env vars, and state in the prompt. |
| **MCP timeout on research tasks** | **First try** raising timeout via config (`hermes config set mcp_servers.codex.timeout 300`). If already raised, shorten the prompt, include specific URLs, split 1 broad query into 2-3 focused ones |

## Quick Test

After auth, validate end-to-end in a git repo with sandbox access:

```bash
cd /tmp && mkdir -p codex-test && cd codex-test && git init
codex exec --sandbox danger-full-access --skip-git-repo-check \
  "用python写一个hello world脚本并运行"
```

## Known Pitfalls

| Pitfall | Fix |
|---------|-----|
| `EACCES: permission denied` on npm install | Use `--prefix ~/.local` (or sudo, but not recommended) |
| `Not inside a trusted directory` | Add `--skip-git-repo-check` or `git init` first |
| `bwrap: loopback: Failed RTM_NEWADDR` | Use `--sandbox danger-full-access` (or install bubblewrap) |
| Device code expired before user completed flow | Generate a fresh code and restart background polling |
| `npm install -g ...` would update a different install | Cosmetic — caused by `--prefix` mismatch. Ignore or fix PATH. |
| Interactive `hermes mcp add` prompt hangs/cancels | Pipe `echo "Y"` to auto-confirm |

## Token Usage

Query Codex's local SQLite DB for token consumption: see `references/token-usage-tracking.md`. For Hermes-side stats, use `hermes insights --days N`.
