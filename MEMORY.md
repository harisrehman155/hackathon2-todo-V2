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

### 2026-02-10 00:12 (local)
- Branch: 001-phase3-todo-ai-chatbot
- Feature folder: specs/001-phase3-todo-ai-chatbot/
- SDD step: Implement (US5 UI redesign addendum)
- Completed: Added governance exception + US5 scope in spec/tasks; generated persisted ui-ux-pro-max design system; redesigned `/tasks` into dark neon glass unified board with pending/completed columns, floating create-task modal, and in-page chat drawer; redirected `/chat` to `/tasks`.
- Evidence (files/tests/commands): specs/001-phase3-todo-ai-chatbot/spec.md; specs/001-phase3-todo-ai-chatbot/tasks.md; design-system/hackathon2-task+chat/MASTER.md; design-system/hackathon2-task+chat/pages/tasks.md; frontend/src/app/tasks/page.tsx; frontend/src/components/tasks/CreateTaskModal.tsx; frontend/src/components/chat/ChatDrawer.tsx; frontend/src/app/chat/page.tsx; `cd frontend && npm run test`; `cd frontend && npx next build`.
- Blockers: T048 manual UX checklist not yet executed in-browser.
- Next: Run manual UI checklist (375/768/1024/1440, modal flow, task toggle/delete, chat send/receive, refresh persistence), then close T048.

### 2026-02-10 10:08 (local)
- Branch: 001-phase3-todo-ai-chatbot
- Feature folder: specs/001-phase3-todo-ai-chatbot/
- SDD step: Implement bugfix validation
- Completed: Fixed `/api/chat` false-500 behavior when MCP stdio cleanup raises after a successful tool run; added regression test for cleanup-exception path.
- Evidence (files/tests/commands): `backend/src/services/chat_service.py`; `backend/tests/test_chat_service.py`; `cd backend && uv run pytest tests/test_chat_service.py tests/test_chat_api.py -q` (16 passed); `cd backend && uv run pytest tests/ -q` (32 passed).
- Blockers: Live environment still requires valid OpenAI key and manual in-browser retest for duplicate-add scenario confirmation.
- Next: Restart backend/frontend and retest chatbot command flow from `/tasks` using same account.

### 2026-02-10 10:19 (local)
- Branch: 001-phase3-todo-ai-chatbot
- Feature folder: specs/001-phase3-todo-ai-chatbot/
- SDD step: Implement observability enhancement
- Completed: Added clearly formatted chat observability logs (request id, model, latency, token usage, estimated cost, tool calls, outcome/error) for each `/api/chat` request; added test validating log block emission.
- Evidence (files/tests/commands): `backend/src/services/chat_service.py`; `backend/tests/test_chat_service.py`; `cd backend && uv run pytest tests/test_chat_service.py tests/test_chat_api.py -q` (17 passed); `cd backend && uv run pytest tests/ -q` (33 passed).
- Blockers: Token/cost fields depend on SDK usage payload availability at runtime; may display `N/A` when unavailable.
- Next: Run backend and send a real chat message to verify live terminal observability output.

### 2026-02-10 10:30 (local)
- Branch: 001-phase3-todo-ai-chatbot
- Feature folder: specs/001-phase3-todo-ai-chatbot/
- SDD step: Implement timeout/reliability fix
- Completed: Increased MCP stdio client timeout/retry settings in chat service (30s, 1 retry) and cached MCP server DB engine initialization to avoid repeated cold-start overhead per tool call.
- Evidence (files/tests/commands): `backend/src/services/chat_service.py`; `backend/src/mcp/server.py`; `cd backend && uv run pytest tests/test_chat_service.py tests/test_chat_api.py tests/test_mcp_tools.py -q` (18 passed); `cd backend && uv run pytest tests/ -q` (33 passed).
- Blockers: Live retest still required against real OpenAI API and Neon latency conditions.
- Next: Restart backend and verify that repeated add-task prompts no longer produce 5s MCP timeout errors.

### 2026-02-10 10:56 (local)
- Branch: 001-phase3-todo-ai-chatbot
- Feature folder: specs/001-phase3-todo-ai-chatbot/
- SDD step: Implement UX + logging refinement
- Completed: Added backend chat response action metadata (`tool_count`, `tool_names`); chat drawer now shows alert on model task action, auto-closes drawer, and triggers task-board refresh so changes appear immediately without manual refresh; reduced chat observability logs to minimal single-line metrics (`model`, tool count+names, input/output tokens, cost).
- Evidence (files/tests/commands): `backend/src/services/chat_service.py`; `backend/src/schemas/chat.py`; `backend/tests/test_chat_service.py`; `frontend/src/lib/api/chat.ts`; `frontend/src/components/chat/ChatDrawer.tsx`; `frontend/src/app/tasks/page.tsx`; `cd backend && uv run pytest tests/test_chat_service.py tests/test_chat_api.py -q` (17 passed); `cd frontend && npx vitest run` (6 passed); `cd frontend && npx next build` (pass).
- Blockers: Alert UX currently uses browser `window.alert` per request; may be replaced with toast if desired.
- Next: Run live `/tasks` chat flow and confirm desired alert + auto-close + immediate task refresh behavior.

### 2026-02-10 11:12 (local)
- Branch: 001-phase3-todo-ai-chatbot
- Feature folder: specs/001-phase3-todo-ai-chatbot/
- SDD step: Implement bugfix follow-up
- Completed: Fixed tool-name extraction logic for OpenAI Agents run items to avoid `unknown_tool` false positives; improved usage extraction fallback from `raw_responses[*].usage`; ensured minimal metrics log output contains only requested fields.
- Evidence (files/tests/commands): `backend/src/services/chat_service.py`; `backend/tests/test_chat_service.py`; `cd backend && uv run pytest tests/test_chat_service.py tests/test_chat_api.py -q` (18 passed); `cd backend && uv run pytest tests/ -q` (34 passed).
- Blockers: Live runtime still needed to verify provider actually returns usage for each response (otherwise tokens/cost remain `N/A`).
- Next: Re-run chatbot task actions in `/tasks` and confirm alerts now show concrete tool names.

### 2026-02-10 13:31 (local)
- Branch: 001-phase3-todo-ai-chatbot
- Feature folder: specs/001-phase3-todo-ai-chatbot/
- SDD step: Implement bugfix validation
- Completed: Strengthened agent instructions to require MCP tool-backed task mutations (including list-first flows for title-based complete/delete); added regression test asserting instruction policy; replaced blocking chat success dialog with `react-toastify`; task board now auto-refreshes after every successful chat response.
- Evidence (files/tests/commands): `backend/src/services/chat_service.py`; `backend/tests/test_chat_service.py`; `frontend/src/components/chat/ChatDrawer.tsx`; `frontend/src/app/tasks/page.tsx`; `frontend/src/app/layout.tsx`; `frontend/package.json`; `cd backend && uv run pytest tests/test_chat_service.py tests/test_mcp_tools.py tests/test_chat_api.py -q` (20 passed); `cd frontend && npm.cmd run test` (6 passed); `cd frontend && npx next build` (pass).
- Blockers: Live OpenAI behavior still depends on real runtime model/tool-call outputs; automated checks validate instruction contract and local integration.
- Next: Restart backend/frontend and run live `/tasks` chat prompts to confirm complete/delete behavior with your account data.

### 2026-02-10 16:17 (local)
- Branch: 001-phase3-todo-ai-chatbot
- Feature folder: specs/001-phase3-todo-ai-chatbot/
- SDD step: Implement reliability hardening
- Completed: Added dynamic tool-choice enforcement (`tool_choice='required'`) for task-command messages so agent cannot answer task actions without MCP tool calls; added tests for required-vs-auto tool choice behavior; executed live ChatService call against OpenAI showing real tool invocation and DB mutation for add-task flow.
- Evidence (files/tests/commands): `backend/src/services/chat_service.py`; `backend/tests/test_chat_service.py`; `cd backend && uv run pytest tests/test_chat_service.py tests/test_chat_api.py tests/test_mcp_tools.py -q` (22 passed); `cd backend && uv run pytest tests/ -q` (37 passed); live script output: `CHAT_RESPONSE Task 'buy groceries' has been created.` + `TOOL_COUNT 2` + `TOOL_NAMES ['add_task', 'unknown_tool']`.
- Blockers: Existing running backend process must be restarted to load new ChatService logic.
- Next: Restart backend, re-run user command set from `/tasks`, and verify logs no longer show `tools=0[none]` for task-action prompts.

### 2026-02-10 16:31 (local)
- Branch: 001-phase3-todo-ai-chatbot
- Feature folder: specs/001-phase3-todo-ai-chatbot/
- SDD step: Implement config/runtime update
- Completed: Added `OPENAI_API_KEY_TRACING` support in backend settings and chat runtime environment wiring; updated `backend/.env` with provided tracing key.
- Evidence (files/tests/commands): `backend/src/config.py`; `backend/src/services/chat_service.py`; `backend/.env`; `cd backend && uv run pytest tests/test_chat_service.py tests/test_chat_api.py -q` (21 passed).
- Blockers: Backend process restart required to load updated env/config values.
- Next: Restart backend and verify trace ingest calls continue successfully under the tracing key setup.

### 2026-02-10 16:41 (local)
- Branch: 001-phase3-todo-ai-chatbot
- Feature folder: specs/001-phase3-todo-ai-chatbot/
- SDD step: Implement tracing key fix
- Completed: Confirmed openai-agents 0.8.1 requires per-run tracing config (not custom env var alone); updated chat service to call `Runner.run(..., run_config=RunConfig(tracing={\"api_key\": OPENAI_API_KEY_TRACING}))`; added regression test to assert tracing key is forwarded.
- Evidence (files/tests/commands): `backend/src/services/chat_service.py`; `backend/tests/test_chat_service.py`; `cd backend && uv run pytest tests/test_chat_service.py tests/test_chat_api.py tests/test_mcp_tools.py -q` (23 passed); `cd backend && uv run pytest tests/ -q` (38 passed).
- Blockers: Must restart backend process; traces appear in project bound to the tracing key, which may differ from currently selected dashboard project.
- Next: Restart backend, send one `/api/chat` request, then verify Logs -> Traces in the tracing key’s project.
