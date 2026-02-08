# Data Model: Phase I Todo Console Foundation

## Entity: Task

### Fields
| Field | Type | Required | Rules |
|---|---|---|---|
| id | integer | yes | Unique within current process run; starts at 1 and increments by 1 |
| title | string | yes | Trimmed; must be non-empty; max 120 chars |
| description | string | no | Optional; if provided max 500 chars |
| status | enum (`pending`, `complete`) | yes | Defaults to `pending` on creation |
| created_at | datetime (UTC ISO-8601) | yes | Set once at create |
| updated_at | datetime (UTC ISO-8601) | yes | Updated on each mutation |

## Entity: TaskCollection

### Description
In-memory aggregate holding all `Task` entities for the running session.

### Behavior
- Insert task on create.
- Lookup by `id` for update/delete/toggle.
- Return stable list order by `id` ascending.
- Reset entirely on process restart (FR-010).

## Entity: UserCommand

### Description
Normalized representation of a CLI action.

### Fields
| Field | Type | Required | Notes |
|---|---|---|---|
| action | enum | yes | `add`, `list`, `update`, `complete`, `uncomplete`, `delete` |
| task_id | integer | conditional | Required for update/complete/uncomplete/delete |
| title | string | conditional | Required for `add`; optional for `update` |
| description | string | optional | Optional for `add`/`update` |

## Relationships
- `TaskCollection` 1..* `Task`
- `UserCommand` acts on zero or one `Task` except `list` which targets collection view.

## Validation Rules (from FR-007/FR-008)
- Unknown `task_id` operations must return explicit error and no state change.
- Blank titles are invalid for create and invalid when updating title.
- Missing required arguments return usage or validation errors without crashing.

## State Transitions

| Current State | Command | Next State | Notes |
|---|---|---|---|
| pending | complete | complete | Must confirm success |
| complete | uncomplete | pending | Must confirm success |
| pending | update | pending | Content change only |
| complete | update | complete | Content change only |
| pending/complete | delete | removed | Entity no longer listed |

## Traceability Notes
- FR-001/FR-008 map to `title`/`description` validation.
- FR-002 maps to `id` generation.
- FR-003 maps to list projection of `id/title/status`.
- FR-004/FR-005/FR-006/FR-007/FR-009 map to command behaviors and state transitions.
- FR-010 maps to `TaskCollection` lifecycle.
