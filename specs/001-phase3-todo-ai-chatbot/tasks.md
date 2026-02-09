# Tasks: Phase III Todo AI Chatbot

**Input**: Design documents from `/specs/001-phase3-todo-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Validation tasks are REQUIRED. Each user story MUST include at least one
automated test or scripted acceptance check mapped to the story. Python scope MUST use
`pytest` and follow Red-Green-Refactor.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Backend tests: `backend/tests/`
- Existing models: `backend/src/db/models/`
- Existing services: `backend/src/services/`
- Existing routes: `backend/src/api/routes/`
- Existing schemas: `backend/src/schemas/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install new dependencies and configure environment variables for Phase III

- [X] T001 Install backend dependencies: run `cd backend && uv add openai-agents "mcp[cli]"` to add OpenAI Agents SDK and MCP SDK to `backend/pyproject.toml`
- [X] T002 Add `OPENAI_API_KEY` entry to `backend/.env` (placeholder value, read from env var in config)
- [X] T003 [P] Add `openai_api_key` field to Settings dataclass in `backend/src/config.py` reading from `OPENAI_API_KEY` env var
- [X] T004 [P] Install frontend dependency: run `cd frontend && npm install @openai/chatkit-react --legacy-peer-deps` to add ChatKit React package
- [X] T005 [P] Add `NEXT_PUBLIC_CHATKIT_API_DOMAIN_KEY=domain_pk_localhost_dev` to `frontend/.env.local`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create data models and schemas that ALL user stories depend on. These MUST be complete before any user story work begins.

**CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundation (Red)

- [X] T006 [P] Write `pytest` test for Conversation model CRUD in `backend/tests/test_conversation_model.py` — test create conversation with UUID PK, owner_user_id, created_at default; test query by owner_user_id; verify auto-creation via SQLModel metadata
- [X] T007 [P] Write `pytest` test for Message model CRUD in `backend/tests/test_message_model.py` — test create message with conversation_id FK, role validation ("user"/"assistant"), content, created_at default; test ordering by created_at

### Implementation for Foundation (Green)

- [X] T008 [P] Create Conversation SQLModel in `backend/src/db/models/conversation.py` — fields: `id` (str, UUID4 PK), `owner_user_id` (str, indexed), `created_at` (datetime, default utcnow) per data-model.md
- [X] T009 [P] Create Message SQLModel in `backend/src/db/models/message.py` — fields: `id` (Optional[int], PK), `conversation_id` (str, FK to conversation.id, indexed), `role` (str, max_length=10), `content` (str), `created_at` (datetime, default utcnow) per data-model.md
- [X] T010 Update `backend/src/db/models/__init__.py` to import Conversation and Message models so `SQLModel.metadata.create_all()` auto-creates the new tables on startup
- [X] T011 [P] Create chat request/response schemas in `backend/src/schemas/chat.py` — `ChatRequest` (message: str 1-2000 chars, conversation_id: Optional[str] UUID), `ChatResponse` (response: str, conversation_id: str), `ChatErrorResponse` (error: str, code: str, conversation_id: Optional[str]) per contracts/chat-api.md

**Checkpoint**: Foundation ready — new tables auto-created on startup, schemas available for route/service

---

## Phase 3: User Story 1 — Manage Tasks in Natural Language (Priority: P1) MVP

**Goal**: Users manage their todo list by chatting in plain language. The agent processes natural language, invokes MCP tools, and returns confirmations.

**Independent Test**: Send natural language task commands via `POST /api/chat` and confirm corresponding task updates in the database.

### Tests for User Story 1 (Red)

- [X] T012 [P] [US1] Write `pytest` tests for MCP tool functions in `backend/tests/test_mcp_tools.py` — test `add_task` creates task in DB, `list_tasks` returns formatted list, `complete_task` marks task done, `delete_task` removes task, `update_task` modifies fields; test user isolation (user A cannot access user B tasks); use SQLite test DB
- [X] T013 [P] [US1] Write `pytest` contract test for `POST /api/chat` in `backend/tests/test_chat_api.py` — test 200 with valid message, test 400 for empty/oversized message, test 401 without JWT, test 403 for wrong user conversation, test 500 error handling; mock agent runner

### Implementation for User Story 1

- [X] T014 [P] [US1] Create MCP `__init__.py` at `backend/src/mcp/__init__.py` (empty module init)
- [X] T015 [US1] Create MCP server in `backend/src/mcp/server.py` — implement `FastMCP("Todo Tools")` with 5 `@mcp.tool()` functions: `add_task(user_id, title, description?)`, `list_tasks(user_id, status?)`, `complete_task(user_id, task_id)`, `delete_task(user_id, task_id)`, `update_task(user_id, task_id, title?, description?)`; each tool creates its own SQLModel Session using DATABASE_URL from env; enforce user isolation; `mcp.run()` for stdio transport per research.md
- [X] T016 [US1] Create chat service in `backend/src/services/chat_service.py` — implement `ChatService` class with `async process_message(user_id, message, conversation_id?, session)` method; create/load conversation; store user message; create `MCPServerStdio` with `{"command": "uv", "args": ["run", "src/mcp/server.py"]}`; create `Agent(name="Todo Assistant", instructions=..., mcp_servers=[server], model="gpt-4o-mini")`; run `Runner.run(agent, messages)`; store assistant response; return response + conversation_id; handle OpenAI API errors gracefully per plan.md component #2
- [X] T017 [US1] Create chat route in `backend/src/api/routes/chat.py` — implement `POST /api/chat` with `ChatRequest` body; validate message length 1-2000 chars; validate conversation ownership if `conversation_id` provided; inject `CurrentUser` via existing `get_current_user` dependency; delegate to `ChatService`; return `ChatResponse` per contracts/chat-api.md
- [X] T018 [US1] Register chat router in `backend/src/main.py` — import and `app.include_router(chat_router)`, update app title to "Phase III Todo AI Chatbot", version to "0.3.0"

### Run Tests (Green)

- [X] T019 [US1] Run `cd backend && uv run pytest tests/test_mcp_tools.py tests/test_chat_api.py -v` — all US1 tests must pass; fix any failures

**Checkpoint**: User Story 1 complete — natural language task management works end-to-end via API

---

## Phase 4: User Story 2 — Continue Conversations Across Requests (Priority: P1)

**Goal**: Users continue the same conversation over multiple requests and after service restarts without losing chat history.

**Independent Test**: Send multiple turns in one conversation, verify context carries over; restart service, send another turn that still uses prior context.

### Tests for User Story 2 (Red)

- [X] T020 [P] [US2] Write `pytest` tests for conversation persistence in `backend/tests/test_chat_service.py` — test new conversation created when no conversation_id; test existing conversation loaded when conversation_id provided; test message history reconstructed from DB; test conversation persists across simulated restart (new service instance, same DB); test conversation ownership check rejects wrong user

### Implementation for User Story 2

- [X] T021 [US2] Enhance `ChatService.process_message()` in `backend/src/services/chat_service.py` — ensure conversation history (all prior messages) is loaded from DB and passed to `Runner.run()` as message context; verify user message stored before agent call; verify assistant response stored after; ensure conversation_id returned on every response (new or existing)

### Run Tests (Green)

- [X] T022 [US2] Run `cd backend && uv run pytest tests/test_chat_service.py -v` — all US2 tests must pass; fix any failures

**Checkpoint**: User Story 2 complete — conversations persist across requests and restarts

---

## Phase 5: User Story 3 — Receive Safe and Clear Assistant Feedback (Priority: P2)

**Goal**: Users receive clear confirmations for successful actions and understandable feedback when an action cannot be completed.

**Independent Test**: Trigger valid and invalid commands and verify response clarity, correctness, and safety.

### Tests for User Story 3 (Red)

- [X] T023 [P] [US3] Write `pytest` tests for agent behavior in `backend/tests/test_chat_service.py` (append to existing) — test that successful task actions include confirmation text; test that referencing non-existent task returns helpful error; test that OpenAI API failure returns user-friendly error and persists user message; test that agent instructions include user_id context

### Implementation for User Story 3

- [X] T024 [US3] Refine agent instructions in `backend/src/services/chat_service.py` — update Agent instructions to include: clear confirmation format ("Task 'X' has been created/completed/deleted/updated"), error explanation format, clarifying question behavior for ambiguous commands, user_id injection pattern per research.md decision #5
- [X] T025 [US3] Add error handling for edge cases in `backend/src/api/routes/chat.py` and `backend/src/services/chat_service.py` — handle empty/whitespace messages, oversized messages (>2000 chars), invalid conversation_id format, OpenAI API timeout/failure (persist user msg, return 500 with conversation_id per contracts/chat-api.md)

### Run Tests (Green)

- [X] T026 [US3] Run `cd backend && uv run pytest tests/test_chat_service.py tests/test_chat_api.py -v` — all US3 tests must pass; fix any failures

**Checkpoint**: User Story 3 complete — clear confirmations and error handling working

---

## Phase 6: User Story 4 — Chat via ChatKit Frontend (Priority: P1)

**Goal**: Users interact with the AI chatbot through a ChatKit-based chat interface in the frontend.

**Independent Test**: Open the frontend, navigate to `/chat`, send a message, and verify a response appears.

### Implementation for User Story 4

- [X] T027 [P] [US4] Create ChatKit proxy route in `frontend/src/app/api/chatkit/route.ts` — Next.js API route at `/api/chatkit`; extract last user message from ChatKit's OpenAI-format request; extract conversation_id from thread context; forward JWT from request headers; call FastAPI `POST /api/chat` at `NEXT_PUBLIC_API_BASE_URL`; translate response back to OpenAI Chat Completions format for ChatKit per contracts/chatkit-proxy.md
- [X] T028 [P] [US4] Create chat API helpers in `frontend/src/lib/api/chat.ts` — helper functions for calling `POST /api/chat` with JWT token; types for ChatRequest and ChatResponse matching contracts/chat-api.md
- [X] T029 [US4] Create chat page in `frontend/src/app/chat/page.tsx` — use ChatKit `useChatKit` hook in self-hosted mode with `url: '/api/chatkit'`; custom fetch to inject JWT Bearer token from Better Auth `authClient.token()`; glassmorphism styling consistent with Phase II (glass cards `bg-white/70 backdrop-blur-lg`, rounded-xl, teal accents); responsive layout per CLAUDE.md design rules
- [X] T030 [US4] Add chat navigation link to existing frontend layout/dashboard — add link to `/chat` page from the task board or navigation bar; use SVG icon (no emoji); consistent with existing Phase II UI patterns

### Validate Frontend

- [X] T031 [US4] Run `cd frontend && npx next build` — verify build succeeds with no errors; test manually by navigating to `http://localhost:3000/chat` and sending a message

**Checkpoint**: User Story 4 complete — ChatKit UI working, messages flow end-to-end

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, integration testing, and cleanup across all user stories

- [X] T032 Run full backend test suite: `cd backend && uv run pytest tests/ -v` — all tests (existing Phase II + new Phase III) must pass
- [X] T033 Run quickstart.md validation — follow `specs/001-phase3-todo-ai-chatbot/quickstart.md` step by step; verify setup instructions are accurate and complete
- [X] T034 Verify user isolation end-to-end — test that user A cannot access user B's conversations or tasks via chat
- [X] T035 Verify conversation resume after backend restart — stop backend, restart, continue existing conversation
- [X] T036 [P] Update `backend/src/main.py` app metadata — ensure title and version reflect Phase III

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup (T001-T003) — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) — core NL task management
- **User Story 2 (Phase 4)**: Depends on US1 (Phase 3) — extends chat service with conversation persistence
- **User Story 3 (Phase 5)**: Depends on US1 (Phase 3) — refines agent behavior and error handling
- **User Story 4 (Phase 6)**: Depends on US1 (Phase 3) + Frontend Setup (T004, T005) — frontend chat UI
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational → implements MCP server + chat service + chat route (core backend)
- **User Story 2 (P1)**: Depends on US1 → enhances chat service with history reconstruction
- **User Story 3 (P2)**: Depends on US1 → refines agent instructions and error handling
- **User Story 4 (P1)**: Depends on US1 → frontend ChatKit UI consuming `POST /api/chat`

### Within Each User Story

- Tests MUST be written in `pytest` and FAIL before implementation (Red)
- Models before services
- Services before endpoints/routes
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1**: T003, T004, T005 can run in parallel (different projects/files)
- **Phase 2**: T006, T007 (tests) in parallel; T008, T009, T011 (models/schemas) in parallel
- **Phase 3**: T012, T013 (tests) in parallel; T014 can parallel with tests
- **Phase 4-5**: US2 and US3 can run in parallel after US1 (both extend chat service but touch different concerns)
- **Phase 6**: T027, T028 (frontend files) in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all US1 tests together (Red phase):
Task T012: "pytest tests for MCP tool functions in backend/tests/test_mcp_tools.py"
Task T013: "pytest contract test for POST /api/chat in backend/tests/test_chat_api.py"

# Launch MCP init + tests in parallel:
Task T014: "Create MCP __init__.py at backend/src/mcp/__init__.py"
# (T014 is independent of T012/T013)
```

## Parallel Example: User Story 4

```bash
# Launch all US4 frontend files in parallel:
Task T027: "ChatKit proxy route in frontend/src/app/api/chatkit/route.ts"
Task T028: "Chat API helpers in frontend/src/lib/api/chat.ts"
# (T027 and T028 are different files, no dependencies)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T011)
3. Complete Phase 3: User Story 1 (T012-T019)
4. **STOP and VALIDATE**: Test `POST /api/chat` with curl — NL commands create/list/complete/delete/update tasks
5. Demo-ready with API-only chat

### Incremental Delivery

1. Setup + Foundational → Foundation ready (tables + schemas)
2. User Story 1 → NL task management via API (MVP!)
3. User Story 2 → Multi-turn conversation persistence
4. User Story 3 → Clear confirmations and error handling
5. User Story 4 → ChatKit frontend UI (full user experience)
6. Polish → End-to-end validation and cleanup

### Single-Developer Strategy

Complete stories sequentially in priority order:
1. Phase 1-2: Setup + Foundation
2. Phase 3: US1 (MVP — core chat + MCP)
3. Phase 4: US2 (conversation persistence)
4. Phase 5: US3 (feedback quality)
5. Phase 6: US4 (ChatKit frontend)
6. Phase 7: Polish

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (Red-Green-Refactor)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MCP server runs as subprocess (stdio) — tested independently from chat service
- ChatKit self-hosted mode requires Next.js proxy route (not direct OpenAI connection)
