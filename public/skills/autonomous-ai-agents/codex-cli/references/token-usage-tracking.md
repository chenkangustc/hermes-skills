# Codex Token Usage Tracking

Codex stores session metadata in a local SQLite database. Usage data is available even without an OpenAI dashboard.

## Query total usage

```bash
sqlite3 ~/.codex/state_5.sqlite "
SELECT 
  COUNT(*) as sessions,
  SUM(tokens_used) as total_tokens,
  SUM(CASE WHEN datetime(created_at_ms/1000,'unixepoch') >= date('now') THEN tokens_used ELSE 0 END) as today_tokens
FROM threads;
"
```

## List recent sessions with token counts

```bash
sqlite3 ~/.codex/state_5.sqlite "
SELECT 
  datetime(created_at_ms/1000,'unixepoch') as created,
  substr(title,1,60) as task,
  model,
  tokens_used
FROM threads 
ORDER BY created_at_ms DESC
LIMIT 20;
"
```

## Compare with Hermes usage

```bash
# Hermes consumption
hermes insights --days 1
```

Codex state DB schema (`~/.codex/state_5.sqlite`, table `threads`):

| Column | Type | Description |
|--------|------|-------------|
| `tokens_used` | INTEGER | Total tokens consumed in the session |
| `model` | TEXT | Model used (e.g. `gpt-5.5`) |
| `model_provider` | TEXT | Provider (e.g. `openai`) |
| `created_at_ms` | INTEGER | Session start as unix epoch ms |
| `title` | TEXT | Session title (first user message) |
| `sandbox_policy` | TEXT | `read-only`, `workspace-write`, or `danger-full-access` |
