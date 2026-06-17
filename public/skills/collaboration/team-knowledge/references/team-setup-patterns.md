# Team Setup Patterns — Session Notes

Captured from a conversation with a Chinese-speaking team using Feishu (Lark), exploring how to share Hermes knowledge across team members.

## Context

- Platform: Feishu (飞书) group chat
- Language: Chinese (simplified)
- Goal: "沉淀大家的智慧" — accumulate collective team wisdom
- Question: One bot or multiple bots? How to share/consolidate skills?

## Key Takeaways

1. **Typical team setup: 1 bot per group chat.** The bot runs on a VPS (cloud VM), connected via gateway to Feishu/Telegram/Discord. Members interact with it in the group. Accumulates skills over time.

2. **Knowledge has 3 layers:**
   - Skills (workflows) → Git-based sharing (Profile Distributions)
   - Memory (preferences) → Per-profile, manual transfer
   - Profile (full agent) → Packaged as git repo, installable with one command

3. **Skill consolidation workflow for teams:**
   - Multiple people write skills for the same topic
   - Team GitHub PR process merges the best parts
   - Single canonical SKILL.md emerges
   - `hermes profile update` syncs changes

4. **External Skill Directories** are a simpler alternative for teams without git: point Hermes at a shared NAS/git-cloned directory.

## User Preferences

- Native Chinese speaker, prefers clear structured answers
- Likes practical, actionable advice with comparison tables
- Wants tools integrated together (Codex → Hermes via MCP) rather than standalone

## Relevant Commands

```bash
# Install a distribution
hermes profile install team-agent git@github.com:org/team-knowledge.git

# Update a distribution
hermes profile update team-agent

# Check profile
hermes profile show team-agent

# External skill directories
# Add to config.yaml:
# external_skill_dirs:
#   - /mnt/team-share/hermes-skills/
