# Tasks: Phase II Full-Stack Todo Web App

**Input**: Design documents from `D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\`  
**Prerequisites**: `plan.md` (required), `spec.md` (required), `research.md`, `data-model.md`, `contracts/todo-api.openapi.yaml`

**Tests**: Required per story. Python scope MUST use `pytest` with Red-Green-Refactor and run via `uv run pytest`.

**Organization**: Tasks are grouped by user story to enable independent implementation and validation.

## Format: `[ID] [P?] [Story] [Trace] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: `US1`, `US2`, `US3`, or `SHARED`
- **[Trace]**: Functional requirement IDs (for traceability)

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 [SHARED] [FR-001..FR-010] Create web app directory skeleton: `backend/src`, `backend/tests/{unit,integration,contract}`, `frontend/src/{app,components,lib,styles}`, `frontend/tests`.
- [X] T002 [P] [SHARED] [FR-001..FR-010] Add backend dependency config in `backend/pyproject.toml` (FastAPI, SQLModel, Pydantic v2, pytest tooling).
- [X] T003 [P] [SHARED] [FR-001..FR-010] Add frontend package config in `frontend/package.json` (Next.js App Router baseline and scripts).
- [X] T004 [SHARED] [FR-001..FR-010] Add environment templates `backend/.env.example` and `frontend/.env.example` for DB/auth secrets.

## Phase 2: Foundational (Blocking)

- [X] T005 [SHARED] [FR-006, FR-007, FR-008] Implement backend settings and secret loading in `backend/src/config.py`.
- [X] T006 [P] [SHARED] [FR-003, FR-008] Implement SQLModel engine/session setup for Neon in `backend/src/db/database.py`.
- [X] T007 [P] [SHARED] [FR-003, FR-008] Implement Task persistence model in `backend/src/db/models/task.py`.
- [X] T008 [P] [SHARED] [FR-006, FR-007, FR-008] Implement JWT verification dependency in `backend/src/auth/dependencies.py`.
- [X] T009 [SHARED] [FR-006, FR-007] Implement shared API error response model and handlers in `backend/src/api/errors.py`.
- [X] T010 [SHARED] [FR-009] Create task route scaffold in `backend/src/api/routes/tasks.py` and register router in `backend/src/main.py`.
- [X] T011 [SHARED] [FR-004] Create frontend design tokens and typography import in `frontend/src/styles/tokens.css` and wire in `frontend/src/app/globals.css`.

**Checkpoint**: Foundation complete. User stories can proceed.

## Phase 3: User Story 1 - Manage Core Todo Lifecycle on Web (Priority: P1) 🎯

**Goal**: Authenticated users can create/list/detail/update/toggle/delete tasks through web and REST API.  
**Independent Test**: Sign in and complete full lifecycle with persisted refresh behavior.

### Tests First (Red) ⚠️

- [X] T012 [P] [US1] [FR-001, FR-002, FR-009] Add API contract tests for `GET/POST /tasks`, `GET/PATCH/DELETE /tasks/{taskId}`, `POST /tasks/{taskId}/toggle-complete` in `backend/tests/contract/test_tasks_contract.py`.
- [X] T013 [P] [US1] [FR-001, FR-003, FR-010] Add backend integration lifecycle test (create->detail->update->toggle->delete->refresh) in `backend/tests/integration/test_task_lifecycle.py`.
- [X] T014 [P] [US1] [FR-001, FR-004] Add frontend acceptance flow for lifecycle controls in desktop and mobile viewports in `frontend/tests/task-lifecycle.spec.ts`.
- [X] T015 [US1] [FR-001, FR-002, FR-003] Run failing test evidence (Red): `uv run pytest backend/tests/contract/test_tasks_contract.py backend/tests/integration/test_task_lifecycle.py`.

### Implementation (Green)

- [X] T016 [P] [US1] [FR-009] Implement Pydantic task schemas `TaskCreate`, `TaskUpdate`, `TaskRead` in `backend/src/schemas/task.py`.
- [X] T017 [US1] [FR-001, FR-002, FR-003] Implement task service CRUD/toggle operations in `backend/src/services/task_service.py`.
- [X] T018 [US1] [FR-001, FR-002, FR-009] Implement task API handlers in `backend/src/api/routes/tasks.py`.
- [X] T019 [P] [US1] [FR-001, FR-002, FR-004] Implement task list/detail/edit UI and state actions in `frontend/src/app/tasks/page.tsx` and `frontend/src/components/tasks/*`.
- [X] T020 [US1] [FR-003, FR-010] Implement frontend API client and mutation handling in `frontend/src/lib/api/tasks.ts`.
- [X] T021 [US1] [FR-001, FR-003] Re-run US1 tests to Green and capture results.

## Phase 4: User Story 2 - Protect Multi-User Boundaries (Priority: P2)

**Goal**: Ensure auth is required and each user can access only own tasks.  
**Independent Test**: User B cannot access/modify User A tasks; unauthenticated requests return `401`.

### Tests First (Red) ⚠️

- [X] T022 [P] [US2] [FR-006, FR-007] Add unauthorized-request tests for all task endpoints in `backend/tests/integration/test_auth_required.py`.
- [X] T023 [P] [US2] [FR-008] Add ownership isolation tests for list/detail/update/delete/toggle in `backend/tests/integration/test_task_isolation.py`.
- [X] T024 [US2] [FR-006, FR-007, FR-008] Run failing US2 tests (Red): `uv run pytest backend/tests/integration/test_auth_required.py backend/tests/integration/test_task_isolation.py`.

### Implementation (Green)

- [X] T025 [US2] [FR-006, FR-007] Enforce authenticated dependency on all task routes in `backend/src/api/routes/tasks.py`.
- [X] T026 [US2] [FR-008] Enforce owner-scoped queries and 404-on-nonowner behavior in `backend/src/services/task_service.py`.
- [X] T027 [P] [US2] [FR-006, FR-007] Implement frontend auth gate and signin/signup route handling in `frontend/src/app/(auth)/*` and `frontend/src/lib/auth/*`.
- [X] T028 [US2] [FR-006, FR-007, FR-008] Re-run US2 tests to Green and capture results.

## Phase 5: User Story 3 - Use App Across Screen Sizes (Priority: P3)

**Goal**: Full lifecycle remains usable on desktop and mobile with clear states and accessible interactions.  
**Independent Test**: Complete lifecycle at desktop and mobile widths with no blocked primary actions.

### Tests First (Red) ⚠️

- [X] T029 [P] [US3] [FR-004] Add responsive acceptance checks (desktop/mobile) for primary task actions in `frontend/tests/responsive-task-ux.spec.ts`.
- [X] T030 [P] [US3] [FR-004] Add UI state checks (loading/empty/error) in `frontend/tests/task-ui-states.spec.ts`.
- [X] T031 [US3] [FR-004] Run failing frontend checks (Red) using project frontend test runner.

### Implementation (Green)

- [X] T032 [US3] [FR-004] Implement responsive grid-to-stack layout behavior and tokens in `frontend/src/components/tasks/TaskLayout.tsx` and `frontend/src/styles/tokens.css`.
- [X] T033 [US3] [FR-004] Implement empty/loading/error states in `frontend/src/components/tasks/TaskStates.tsx`.
- [X] T034 [US3] [FR-004] Ensure typography/color/motion follow planned UI direction in `frontend/src/styles/tokens.css` and `frontend/src/app/globals.css`.
- [X] T035 [US3] [FR-004] Re-run US3 frontend checks to Green and capture results.

## Phase 6: Polish & Cross-Cutting

- [X] T036 [P] [SHARED] [FR-001..FR-010] Add OpenAPI contract verification against implementation in `backend/tests/contract/test_openapi_sync.py`.
- [X] T037 [P] [SHARED] [FR-001..FR-010] Add regression tests for preserved Phase I lifecycle semantics in `backend/tests/integration/test_phase1_parity.py`.
- [X] T038 [SHARED] [FR-001..FR-010] Run full backend test suite: `uv run pytest` and record evidence.
- [X] T039 [SHARED] [FR-004] Run frontend acceptance suite and record desktop/mobile evidence.
- [X] T040 [SHARED] [FR-001..FR-010] Update `README.md` with Phase II run/test/deploy verification steps and evidence links.

## Dependencies & Execution Order

- Setup (T001-T004) -> Foundational (T005-T011) -> US1 (T012-T021) -> US2 (T022-T028) -> US3 (T029-T035) -> Polish (T036-T040).
- User stories may overlap only after Foundational completion and only when dependencies are satisfied.
- For each story: tests must be authored and executed in failing state before implementation tasks begin.

## Requirement-to-Task Traceability

| Requirement | User Story | Tasks | Validation |
|---|---|---|---|
| FR-001 | US1 | T012-T021 | API contract + integration lifecycle + frontend lifecycle checks |
| FR-002 | US1 | T012, T016-T020 | List/detail behavior validated in API + UI tests |
| FR-003 | US1 | T013, T017, T020, T021 | Persistence verified via refresh and integration tests |
| FR-004 | US3 | T014, T029-T035, T039 | Responsive + UI state checks on desktop/mobile |
| FR-005 | US2 | T027 | Signup/signin paths implemented and validated in acceptance flow |
| FR-006 | US2 | T008, T022, T025, T027, T028 | Auth required checks across all task routes |
| FR-007 | US2 | T022, T025, T028 | 401 behavior validated for missing/invalid auth |
| FR-008 | US2 | T023, T026, T028 | Ownership isolation enforced and tested |
| FR-009 | US1 | T010, T012, T018 | Stable REST routes implemented and contract-tested |
| FR-010 | US1 | T013, T021, T037 | Regression parity with Phase I lifecycle behavior |

## Notes

- Use `uv` for all Python dependency and test workflows.
- Keep commits small and traceable to task IDs.
- Do not start `/sp.implement` until this task list is approved.



