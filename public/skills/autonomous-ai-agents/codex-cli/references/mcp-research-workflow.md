# Codex MCP Research Workflow — Session Transcript

## Context

The user asked "你用这个Codex帮我搜索一下" (use Codex to search for information about team deployment patterns for Hermes).

## First Attempt (Failed)

Used `delegate_task` with `web` + `browser` toolsets instead of `mcp_codex_codex` — wrong approach. The subagent hit max_iterations without producing a result. The user later expressed frustration about not following their instruction to use Codex directly.

## Second Attempt (Used Codex MCP — Timed Out)

```
mcp_codex_codex(
  approval-policy="never",
  prompt="Search... [very long prompt covering 5+ questions across multiple docs sites]",
  sandbox="read-only"
)
```

Result: `TimeoutError: MCP call timed out after 120.0s`

Root cause: prompt was too broad, covering too many topics and source URLs in a single call.

## Third Attempt (Succeeded — Focused Prompt)

```
mcp_codex_codex(
  approval-policy="never",
  prompt="Search https://hermes-agent.nousresearch.com/docs/ and summarize... [2-3 specific questions, concise wording]",
  sandbox="read-only"
)
```

Result: returned a comprehensive structured answer covering all 5 sub-topics with source links.

## Key Lessons

1. **Use the right tool from the start** — when user says "use Codex", use `mcp_codex_codex`, not alternative tools
2. **Keep prompts concise** — long prompts with many sources cause 120s timeout
3. **Include specific URLs** — help Codex focus instead of broadly searching
4. **Split large queries** — one focused prompt per 2-3 questions, rather than 5+ in one call
5. **Structured output requests** — asking for tables or bulleted lists makes output more useable
6. **Config-based timeout fix** — for recurring timeout issues, raise the limit via `hermes config set mcp_servers.codex.timeout 300`. This is better than repeatedly shortening prompts if the task genuinely needs longer.
