# MEMORY.md

## Purpose
Persistent cross-run project memory for Codex workflow continuity.
Read this file at the start of each run and update it after meaningful progress.

## Current Snapshot
- Date: 2026-02-09
- Repository: `d:\Haris\hackathons\hackathon2`
- Active branch: `001-phase3-todo-ai-chatbot` (expected from open spec context)
- Active feature folder: `specs/001-phase3-todo-ai-chatbot/`
- Current SDD step: `Plan/Tasks complete; Implement pending`

## Last Completed Work
1. Synced Codex skill with Claude skill:
   - Copied `.claude/skills/hackathon2-sdd-phase-workflow/references/phase-2.md`
     to `.codex/skills/hackathon2-sdd-phase-workflow/references/phase-2.md`.
2. Merged rules and operational changes from `CLAUDE.md` into `AGENTS.md`.
3. Added mandatory memory workflow and source-of-truth reference to `AGENTS.md`.

## Open Risks / Notes
- `AGENTS.md` now includes CLAUDE-derived operational constraints and Phase III context.
- Keep `CLAUDE.md` and `AGENTS.md` aligned when new durable rules are added.

## Next Actions
1. When starting implementation, follow `Specify -> Plan -> Tasks -> Implement`.
2. Execute `/sp.implement` scope for `specs/001-phase3-todo-ai-chatbot/`.
3. After implementation, ask:
   `Should we move on to the next feature/phase?`

## Update Template
Use this structure for each new entry:

### YYYY-MM-DD HH:MM (local)
- Branch:
- Feature folder:
- SDD step:
- Completed:
- Evidence (files/tests/commands):
- Blockers:
- Next:

### 2026-02-09 23:08 (local)
- Branch: 001-phase3-todo-ai-chatbot
- Feature folder: specs/001-phase3-todo-ai-chatbot/
- SDD step: Implement (completed) / validation complete
- Completed: Implemented Phase III backend (MCP + chat API/service + models/schemas/tests) and frontend (ChatKit proxy/page/nav), marked T001-T036 [X], created PHR 0005.
- Evidence (files/tests/commands): backend uv run pytest tests/ -v (31 passed), frontend npm run build (pass), history/prompts/001-phase3-todo-ai-chatbot/0005-phase3-chatbot-implementation.green.prompt.md.
- Blockers: None current; manual live OpenAI key smoke still optional.
- Next: Ask user whether to move on to next feature/phase as required by AGENTS.md.

### 2026-02-09 23:21 (local)
- Branch: 001-phase3-todo-ai-chatbot
- Feature folder: specs/001-phase3-todo-ai-chatbot/
- SDD step: Implement verification
- Completed: Re-tested backend chatbot suite and frontend build; fixed MCP subprocess module path in chat_service (uv run -m src.mcp.server); live /api/chat smoke now returns controlled 500 service_error without import crash.
- Evidence (files/tests/commands): backend/src/services/chat_service.py; uv run pytest tests/test_chat_service.py tests/test_chat_api.py -q (15 passed); live TestClient POST /api/chat result.
- Blockers: OPENAI_API_KEY placeholder prevents successful assistant response.
- Next: User to provide real OPENAI_API_KEY (and optional prod ChatKit key) for full live E2E success.
