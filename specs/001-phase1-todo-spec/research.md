# Phase 0 Research: Phase I Todo Console Foundation

## Decision 1: Runtime and project shape
- Decision: Use Python 3.13+ single-project console architecture (`src/` + `tests/`).
- Rationale: Matches constitution baseline, Phase I scope, and simplest TDD path.
- Alternatives considered: Split backend/frontend structure was rejected because Phase I has no web surface.

## Decision 2: Command interaction model
- Decision: Implement command-style interface (`add`, `list`, `update`, `complete`, `uncomplete`, `delete`) with argument validation and explicit human-readable confirmations/errors.
- Rationale: Directly maps to user stories and FR-001..FR-009 while staying CLI-native.
- Alternatives considered: Interactive prompt wizard was rejected because it complicates deterministic testing and traceability.

## Decision 3: Task identifier generation
- Decision: Use monotonically increasing integer IDs starting at 1 per process run.
- Rationale: Satisfies FR-002 and keeps tests deterministic.
- Alternatives considered: UUIDs were rejected due to lower readability in console and unnecessary complexity for single-session scope.

## Decision 4: Title and input validation
- Decision: Enforce non-blank title (after trim) with max length 120 characters; descriptions optional up to 500 characters.
- Rationale: Resolves edge-case ambiguity and provides bounded input behavior for consistent errors.
- Alternatives considered: Unlimited string length was rejected because it creates inconsistent UX and weaker validation tests.

## Decision 5: Duplicate titles
- Decision: Allow duplicate titles and distinguish tasks by ID.
- Rationale: Spec requires unique identifier, not unique title; allowing duplicates avoids unnecessary user friction.
- Alternatives considered: Enforcing unique titles was rejected because it introduces avoidable conflict handling not required by scope.

## Decision 6: Task state model
- Decision: Use two states only: `pending` and `complete`, toggled via explicit commands.
- Rationale: Aligns exactly with FR-006 and acceptance scenarios.
- Alternatives considered: Additional states (archived, canceled) were rejected as out of scope.

## Decision 7: Time metadata
- Decision: Track `created_at` and `updated_at` in UTC ISO-8601 format.
- Rationale: Supports entity lifecycle clarity with deterministic serialization.
- Alternatives considered: Local timezone timestamps were rejected due to cross-machine inconsistency.

## Decision 8: Testing strategy
- Decision: Use `pytest` with Red-Green-Refactor across unit tests (validators/service) and integration-style command tests.
- Rationale: Required by constitution principle IV and enables traceable story-level evidence.
- Alternatives considered: `unittest` was rejected because constitution explicitly standardizes on `pytest`.

## Decision 9: Contract artifact for future phases
- Decision: Provide a REST-style OpenAPI contract in `contracts/` as design artifact while implementing CLI behavior in Phase I.
- Rationale: Satisfies planning requirement for contracts and eases migration to Phase II service surfaces.
- Alternatives considered: GraphQL schema was rejected because CRUD command mapping is clearer in REST for this scope.

## Clarification status
All previous unknowns in technical context are resolved. No `NEEDS CLARIFICATION` markers remain.
