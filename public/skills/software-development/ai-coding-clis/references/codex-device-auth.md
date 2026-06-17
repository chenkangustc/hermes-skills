# Codex CLI Device Auth — Session Transcript

## The Problem

`codex login --device-auth` outputs a URL + device code, then **blocks polling** for the user to complete the browser flow. If the process exits (timeout, kill, user Ctrl+C) before the user finishes, the auth succeeds in the browser but the CLI **never receives the token** — `codex login status` still shows "Not logged in".

## The Fix

Run the auth command in **background mode** so it keeps polling:

```python
terminal(
  command="~/.local/bin/codex login --device-auth",
  background=True,
  notify_on_complete=True,
  timeout=600
)
```

Then wait ~5s for the output to appear, read it via `process(action="log", session_id=...)`, extract the URL and code, and give them to the user.

## Full Transcript

```
User: 帮我配置一下Codex
User: 你先帮我下载一个Codex，然后用我的谷歌账号

→ npm install -g @openai/codex --prefix ~/.local
→ Codex CLI v0.140.0 installed at ~/.local/bin/codex

→ codex login status → "Not logged in"

→ codex login --device-auth (foreground, timeout 15s)
→ Works but command times out before user can auth

→ codex login --device-auth (background + notify_on_complete + timeout 600)
→ Output captured:
   "Welcome to Codex [v0.140.0]
    Follow these steps to sign in with ChatGPT using device code authorization:
    1. Open this link: https://auth.openai.com/codex/device
    2. Enter this one-time code: S42G-M7BUW

→ User opens URL, enters code, authenticates with Google SSO ("Continue with Google")
→ Background process receives token, saves it locally
→ Process completes, notify_on_complete fires

→ codex login status → "Logged in"
```

## Key Lessons

1. **Auth URL:** `https://auth.openai.com/codex/device` (NOT GitHub)
2. **Auth method:** ChatGPT/OpenAI account — supports Google SSO
3. **The blocking-poll trap:** device-code auth CLIs need the process alive to receive the token
4. **Token location:** stored locally, per-machine
5. **Code expiry:** ~15 minutes, need a fresh one if timed out
