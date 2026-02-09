# Phase 0 Research: Phase II Full-Stack Todo Web App

## Decision 1: Validation layer with Pydantic v2
- Decision: Use explicit Pydantic request/response models in FastAPI (`TaskCreate`, `TaskUpdate`, `TaskRead`, `ErrorResponse`) instead of relying only on ORM objects.
- Rationale: Provides strict input validation, stable API contracts, and clean separation between persistence models and transport models.
- Alternatives considered: SQLModel-only serialization was rejected because it couples storage and API surface and weakens schema control.

## Decision 2: Authentication and user identity handling
- Decision: Verify Better Auth JWTs in backend middleware/dependency and derive `current_user_id` for all task operations.
- Rationale: Meets FR-006/FR-007 and constitution security principle by enforcing server-side auth.
- Alternatives considered: Frontend-only checks were rejected because they do not protect API data access.

## Decision 3: Ownership enforcement strategy
- Decision: Scope all task queries/mutations by `owner_user_id` and return `404` for out-of-scope task IDs.
- Rationale: Prevents cross-user disclosure and update/delete side effects while keeping endpoint behavior predictable.
- Alternatives considered: Returning `403` on ownership misses was rejected to avoid exposing task existence to non-owners.

## Decision 4: Persistence and schema baseline
- Decision: Store tasks in Neon Postgres with SQLModel table for lifecycle fields and ownership reference.
- Rationale: Aligns with Phase II mandatory stack and enables persistent multi-user behavior (FR-003, FR-008).
- Alternatives considered: SQLite was rejected because Phase II baseline explicitly calls for Neon.

## Decision 5: REST route pattern
- Decision: Use REST-style endpoints: `GET/POST /tasks`, `GET/PATCH/DELETE /tasks/{task_id}`, `POST /tasks/{task_id}/toggle-complete`.
- Rationale: Directly satisfies FR-009 and maps cleanly to user workflows.
- Alternatives considered: GraphQL was rejected as unnecessary for this scope.

## Decision 6: Backend testing strategy
- Decision: Use `pytest` with red-green-refactor for unit + integration/API tests, executed through `uv run pytest`.
- Rationale: Required by constitution and AGENTS rules for Python scope.
- Alternatives considered: `unittest` was rejected because `pytest` is the project standard.

## Decision 7: Responsive validation baseline
- Decision: Validate lifecycle flows on desktop and mobile breakpoints using scripted acceptance checks in quickstart.
- Rationale: Ensures FR-004 and US3 are testable and evidenced.
- Alternatives considered: Desktop-only checks were rejected because mobile support is explicit scope.

## Decision 8: Frontend UI system baseline
- Decision: Use a token-driven UI system with CSS variables, `Space Grotesk` headings, `Source Sans 3` body text, and a teal-accent neutral palette across task screens.
- Rationale: Gives the frontend a clear and reusable visual identity for Phase II while keeping components easy to evolve in later phases.
- Alternatives considered: Default framework styling was rejected because it leads to inconsistent UI and weak responsive design intent.

## Clarification status
All previously unknown technical decisions are resolved. No `NEEDS CLARIFICATION` markers remain.
