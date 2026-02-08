# Tasks: Phase I Todo Console Foundation

**Input**: Design documents from `/specs/001-phase1-todo-spec/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/todo-api.openapi.yaml`

**Tests**: Required per story. Python scope MUST use `pytest` with Red-Green-Refactor.

## Format: `[ID] [P?] [Story] [Req] Description`

- `[P]`: Can run in parallel (different files, no direct dependency)
- `[Story]`: `US1`, `US2`, `US3`, or `SHARED`
- `[Req]`: Functional requirement IDs from `spec.md` (e.g., `FR-001`)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create baseline project and test structure for Phase I console scope.

- [X] T001 [SHARED] [FR-010] Create source and test directories in `src/` and `tests/` per plan structure.
- [X] T002 [P] [SHARED] [FR-010] Add package markers (`__init__.py`) for `src/cli/`, `src/models/`, `src/services/`, `src/lib/`.
- [X] T003 [P] [SHARED] [FR-010] Add `pytest` configuration file (`pytest.ini`) for `tests/unit/` and `tests/integration/` discovery.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define core domain model and validation behavior all stories depend on.

**CRITICAL**: User-story implementation starts only after this phase.

- [X] T004 [SHARED] [FR-002, FR-010] Define `Task` model and status enum in `src/models/task.py` based on `data-model.md`.
- [X] T005 [P] [SHARED] [FR-008] Implement title/description validators in `src/lib/validators.py` (blank title, max lengths).
- [X] T006 [P] [SHARED] [FR-007] Define shared domain error types for validation and missing task IDs in `src/lib/errors.py`.
- [X] T007 [SHARED] [FR-002, FR-010] Create in-memory task repository/collection behavior in `src/services/task_service.py` with deterministic ID generation.

**Checkpoint**: Domain foundation complete; story work can proceed.

---

## Phase 3: User Story 1 - Capture New Tasks (Priority: P1) 🎯 MVP

**Goal**: Add tasks with required title and optional description, then list them.

**Independent Test**: Add task(s) and verify list includes ID/title/status with success confirmation.

### Tests for User Story 1 (REQUIRED) ⚠️

- [X] T008 [P] [US1] [FR-001, FR-002, FR-003, FR-008] Write Red unit tests for create/list behavior in `tests/unit/test_task_service.py`.
- [X] T009 [P] [US1] [FR-001, FR-003, FR-009] Write Red integration tests for `add` + `list` CLI flow in `tests/integration/test_cli_commands.py`.
- [X] T010 [US1] [FR-008] Execute `pytest -q tests/unit/test_task_service.py tests/integration/test_cli_commands.py` and capture failing evidence (Red).

### Implementation for User Story 1

- [X] T011 [P] [US1] [FR-001, FR-002, FR-008] Implement create-task service logic in `src/services/task_service.py`.
- [X] T012 [P] [US1] [FR-003] Implement list projection formatting for task summaries in `src/services/task_service.py`.
- [X] T013 [US1] [FR-001, FR-003, FR-009] Implement `add` and `list` command handlers in `src/cli/commands.py`.
- [X] T014 [US1] [FR-001, FR-002, FR-003, FR-008, FR-009] Run targeted tests to Green and refactor as needed.

**Checkpoint**: US1 independently functional and testable.

---

## Phase 4: User Story 2 - Maintain Existing Tasks (Priority: P1)

**Goal**: Update, complete/uncomplete, and delete tasks by ID.

**Independent Test**: Update/toggle/delete a task and verify only the targeted task changes.

### Tests for User Story 2 (REQUIRED) ⚠️

- [X] T015 [P] [US2] [FR-004, FR-005, FR-006, FR-007] Write Red unit tests for update/toggle/delete behavior in `tests/unit/test_task_service.py`.
- [X] T016 [P] [US2] [FR-004, FR-005, FR-006, FR-007, FR-009] Write Red integration tests for `update`, `complete`, `uncomplete`, `delete` in `tests/integration/test_cli_commands.py`.
- [X] T017 [US2] [FR-004, FR-005, FR-006, FR-007] Execute `pytest -q tests/unit/test_task_service.py tests/integration/test_cli_commands.py` and capture failing evidence (Red).

### Implementation for User Story 2

- [X] T018 [P] [US2] [FR-004, FR-006] Implement update and status toggle service methods in `src/services/task_service.py`.
- [X] T019 [P] [US2] [FR-005, FR-007] Implement delete + unknown-ID error handling in `src/services/task_service.py`.
- [X] T020 [US2] [FR-004, FR-005, FR-006, FR-007, FR-009] Implement `update`, `complete`, `uncomplete`, `delete` handlers in `src/cli/commands.py`.
- [X] T021 [US2] [FR-004, FR-005, FR-006, FR-007, FR-009] Run targeted tests to Green and refactor as needed.

**Checkpoint**: US2 independently functional and testable.

---

## Phase 5: User Story 3 - Review Task State Clearly (Priority: P2)

**Goal**: Ensure list output clearly communicates mixed and empty task states.

**Independent Test**: List empty and mixed-state tasks with consistent, readable status labels.

### Tests for User Story 3 (REQUIRED) ⚠️

- [X] T022 [P] [US3] [FR-003] Write Red integration tests for empty-state and mixed-state list output in `tests/integration/test_cli_commands.py`.
- [X] T023 [P] [US3] [FR-003, FR-009] Write Red snapshot/format assertions for status labels and confirmation text in `tests/integration/test_cli_commands.py`.
- [X] T024 [US3] [FR-003] Execute `pytest -q tests/integration/test_cli_commands.py` and capture failing evidence (Red).

### Implementation for User Story 3

- [X] T025 [P] [US3] [FR-003] Implement/adjust list renderer formatting in `src/cli/commands.py`.
- [X] T026 [US3] [FR-003, FR-009] Add explicit empty-state message and consistent status indicators in `src/cli/commands.py`.
- [X] T027 [US3] [FR-003, FR-009] Run targeted tests to Green and refactor as needed.

**Checkpoint**: US3 independently functional and testable.

---

## Phase 6: Polish & Cross-Cutting Validation

**Purpose**: Final traceability and acceptance evidence for Phase I submission.

- [X] T028 [P] [SHARED] [FR-001..FR-010] Add requirement-to-test trace matrix in `specs/001-phase1-todo-spec/tasks.md` (Traceability Matrix section).
- [X] T029 [P] [SHARED] [FR-001..FR-010] Run full suite `pytest` and record pass evidence for phase checkpoint.
- [X] T030 [SHARED] [FR-001..FR-010] Execute scripted acceptance flow from `specs/001-phase1-todo-spec/quickstart.md` and record outputs in `README.md` evidence section.

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): starts immediately.
- Foundational (Phase 2): depends on Setup; blocks all user stories.
- User Stories (Phases 3-5): depend on Foundational completion.
- Polish (Phase 6): depends on completion of all targeted stories.

### User Story Dependencies

- US1 (P1): starts after Foundational; independent MVP slice.
- US2 (P1): starts after Foundational; depends on existing create/list behavior for realistic flows.
- US3 (P2): starts after US1 list baseline exists.

### Within Each Story

- Tests first (`pytest`) and fail (Red).
- Minimal implementation to pass tests (Green).
- Refactor with tests passing.

### Parallel Opportunities

- T002, T003 can run in parallel.
- T005, T006 can run in parallel.
- Per story, test-writing tasks marked `[P]` can run in parallel.
- Per story, non-overlapping implementation tasks marked `[P]` can run in parallel.

---

## Traceability Matrix

| Requirement | User Story | Planned Tasks | Validation Method |
|---|---|---|---|
| FR-001 | US1 | T008, T009, T011, T013, T014 | `pytest` unit + integration tests for create flow |
| FR-002 | US1 | T004, T007, T008, T011, T014 | `pytest` assertions on deterministic ID generation |
| FR-003 | US1, US3 | T008, T009, T012, T013, T022, T023, T025, T026, T027 | `pytest` list output tests (mixed + empty states) |
| FR-004 | US2 | T015, T016, T018, T020, T021 | `pytest` update behavior tests |
| FR-005 | US2 | T015, T016, T019, T020, T021 | `pytest` delete behavior tests |
| FR-006 | US2 | T015, T016, T018, T020, T021 | `pytest` complete/uncomplete state tests |
| FR-007 | US2 | T006, T015, T016, T017, T019, T020, T021 | Negative `pytest` tests for unknown IDs |
| FR-008 | US1 | T005, T008, T010, T011, T014 | Validation-focused `pytest` tests |
| FR-009 | US1, US2, US3 | T009, T013, T016, T020, T023, T026 | Integration tests for confirmation/error output |
| FR-010 | SHARED | T001, T003, T004, T007 | Session lifecycle checks in unit/integration tests |

---

## Implementation Strategy

### MVP First

1. Complete Phase 1 + Phase 2.
2. Deliver US1 with Red-Green-Refactor proof.
3. Validate US1 independently before US2/US3.

### Incremental Delivery

1. US1 (capture tasks) -> validate.
2. US2 (maintain tasks) -> validate.
3. US3 (review clarity) -> validate.

### Notes

- Keep commits aligned to task IDs for auditability.
- Do not start implementation tasks before corresponding Red tests are captured.
- Any scope change must update `spec.md` and re-align plan/tasks before coding.
