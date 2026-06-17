---
name: ai-coding-clis
description: "Install, authenticate, and configure third-party AI coding CLI tools (Codex, Claude Code, OpenCode, etc.) — covering npm/pip global installs, device-code OAuth flows, and background process management for blocking auth workflows."
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos]
metadata:
  created_by: agent
  tags: [codex, claude-code, opencode, ai-cli, npm, device-auth, oauth]
---

# AI Coding CLIs

Installation and authentication patterns for third-party AI coding command-line tools that run alongside or integrate with Hermes Agent.

## Common Patterns

### npm Global Install (EACCES Fix)

Most AI coding CLIs (Codex, etc.) are distributed via npm. A bare `npm install -g` usually fails with **EACCES** because `/usr/lib/node_modules/` is root-owned. Fix:

```bash
npm install -g <package> --prefix ~/.local
```

This puts binaries at `~/.local/bin/<name>`. Ensure `~/.local/bin` is in `$PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### pip Global Install (PEP 668)

For Python-distributed CLIs, use a venv or uv to bypass PEP 668 protections. See the `hermes-agent` skill for the Hermes venv setup pattern.

### Device-Code OAuth Flow

Many AI coding CLIs use device-code OAuth (you get a URL + one-time code, authenticate in browser, CLI polls for the token).

**Critical pitfall:** the CLI process **must stay running** to receive the token after you auth in the browser. If you run it with a short timeout or let it exit, the auth succeeds in the browser but the CLI never saves the token.

**Correct pattern — run in background with notify:**

```bash
# Start the auth flow in background so it keeps polling
terminal(
  command="<cli> login --device-auth",
  background=true,
  notify_on_complete=true,
  timeout=600
)

# Wait a few seconds, then read the output for the URL and code
terminal(command="sleep 5")
process(action="log", session_id="<proc_id>")
# → Shows: "1. Open https://...  2. Enter this code: XXXXX-XXXXX"

# Give the URL + code to the user
# User opens the URL in their browser, enters the code, signs in
# Background process receives the token and exits — notify_on_complete fires
```

**Why it works:** the background process keeps polling the auth server. When the user completes the flow in the browser, the server responds with the token, the CLI saves it locally, and exits.

### Pitfall: process(action="log") Returns Empty Output (PTY/Buffering)

Some CLIs (e.g. `gh auth login`) write the device code to a buffered stream that `process(action="log")` can't capture. The output preview stays empty even though the CLI printed the code.

**Workaround — redirect output to a file:**

```bash
# Instead of bare background:
# terminal(command="<cli> login --device-auth", background=true, ...)

# Use file redirect:
terminal(
  command="rm -f /tmp/auth_output.txt; <cli> login --device-auth &>/tmp/auth_output.txt",
  background=true,
  notify_on_complete=true,
  timeout=300
)

# Read the file for the URL + code
terminal(command="sleep 3 && cat /tmp/auth_output.txt")

# Give URL + code to the user
# Background process continues polling in the background
# When user completes browser flow → notify_on_complete fires
```

This reliably captures the device code regardless of PTY or buffering behavior.

### Getting the code without starting a long-lived process

If you only need the device code (not the polling), you can use a short foreground timeout:

```bash
timeout 8 <cli> login --device-auth 2>&1 || true
# → Outputs the URL + one-time code, then exits
```

But this does NOT keep the polling alive — the device code you got is already invalidated because the polling process exited. Use only for quick previews; for real auth, use the background + file-redirect pattern above.

### Verify Auth Status

```bash
<cli> login status
# → "Logged in" (exit 0) or "Not logged in" (exit 1)
```

---

## Specific Tools

### Codex CLI (OpenAI)

| Property | Value |
|----------|-------|
| Package | `@openai/codex` |
| Install | `npm install -g @openai/codex --prefix ~/.local` |
| Binary | `~/.local/bin/codex` |
| Auth | `codex login --device-auth` |
| Auth URL | `https://auth.openai.com/codex/device` |
| Auth method | ChatGPT/OpenAI account (**supports Google SSO** via "Continue with Google") |
| Version check | `codex --version` |

#### Full Setup

```bash
# 1. Install
npm install -g @openai/codex --prefix ~/.local

# 2. Verify
~/.local/bin/codex --version

# 3. Auth (must stay running — use background)
# Give user: URL + device code
# User opens URL, enters code, authenticates with Google SSO
# Background process receives token

# 4. Verify auth
~/.local/bin/codex login status
```

#### Device Auth Reference

See `references/codex-device-auth.md` for the full device-code OAuth transacript and pitfalls.

---

## Troubleshooting

### "Not logged in" after browser showed success

The CLI process that printed the device code exited before the user completed auth. **The CLI needs to be running continuously to poll for the auth result.** Restart the `--device-auth` flow in the background.

### EACCES on npm install -g

Use `--prefix ~/.local` as shown above. Do NOT use `sudo npm install -g` — it creates permission and security issues.

### CLI not found after install

If installed with `--prefix`, the binary won't be in the default PATH. Add `~/.local/bin` to PATH or use the full path.

---

## Pitfalls

- **Device-auth timeout:** device codes expire in ~15 minutes. If the user doesn't complete the flow in time, you need a fresh code.
- **Background process lifecycle:** the background process doing the auth polling must survive until the user completes the browser flow. Use `notify_on_complete=true` and a generous timeout.
- **No PTY needed for device auth:** device-code CLI auth works fine without PTY mode. The URL and code are written to stdout, then the process polls the auth server.
- **Auth is per-machine:** the saved token is stored locally (~/.codex/ or similar). A different machine needs a fresh auth.
