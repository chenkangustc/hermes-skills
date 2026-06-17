# Codex CLI Device-Code Authentication — Detailed Flow

## Why this is tricky

`codex login --device-auth` does two things:
1. **Prints** the URL + one-time code to stdout (immediate)
2. **Polls** the OpenAI auth server in the foreground until the user completes the browser flow (blocking)

If the command times out or is killed between step 1 and step 2's completion, the auth is lost — the user already authenticated in their browser, but the CLI never received the token.

## Correct procedure

### Phase 1 — Present the URL + code

Run with a short foreground timeout just to capture the URL/code, then discard the process:

```python
# foreground — get the code for the user
terminal(
  command="timeout 15 ~/.local/bin/codex login --device-auth 2>&1 || true",
  timeout=20
)
```

This prints something like:
```
https://auth.openai.com/codex/device
S42G-M7BUW
```

### Phase 2 — Start background polling

Immediately start a long-running background process that will poll until the user completes the browser flow:

```python
terminal(
  command="~/.local/bin/codex login --device-auth",
  background=True,
  notify_on_complete=True,
  timeout=600  # 10 min — gives the user plenty of time
)
```

### Phase 3 — Give user instructions

Present the user with:
1. URL: `https://auth.openai.com/codex/device`
2. One-time code: `S42G-M7BUW` (expires in 15 min)
3. Sign-in options: "Continue with Google" recommended

### Phase 4 — Verify

After the user confirms they've completed the browser flow:

```bash
codex login status
# Expected: "Logged in using ChatGPT"
```

## Common failure modes

| Symptom | Root cause |
|---------|-----------|
| "Not logged in" after user says they see success | The polling process timed out before receiving the token. Restart from Phase 2. |
| Code expires mid-flow | The device code has a 15-minute TTL. If the user takes too long, generate a fresh code. |
| Background process exits with code 0 but still "Not logged in" | The process got the auth response but couldn't save the token (permissions?), or it was a stale/different process. |
