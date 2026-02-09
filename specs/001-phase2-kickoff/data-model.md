# Data Model: Phase II Full-Stack Todo Web App

## Entity: User

### Fields
| Field | Type | Required | Rules |
|---|---|---|---|
| id | string (UUID/text) | yes | Stable user identity from auth provider claims |
| email | string | yes | Valid email format |
| created_at | datetime (UTC) | yes | Set at user record creation |

## Entity: Task (SQLModel table)

### Fields
| Field | Type | Required | Rules |
|---|---|---|---|
| id | integer | yes | Primary key, auto-increment |
| owner_user_id | string | yes | Must match authenticated user id |
| title | string | yes | Trimmed, non-empty, max 120 chars |
| description | string | no | Optional, max 500 chars |
| is_completed | boolean | yes | Defaults to `false` |
| created_at | datetime (UTC) | yes | Set on insert |
| updated_at | datetime (UTC) | yes | Updated on mutation |

## API Schemas (Pydantic v2)

### TaskCreate
| Field | Type | Required | Rules |
|---|---|---|---|
| title | string | yes | 1..120 chars after trim |
| description | string | no | <=500 chars |

### TaskUpdate
| Field | Type | Required | Rules |
|---|---|---|---|
| title | string | no | If present: 1..120 chars after trim |
| description | string | no | If present: <=500 chars |
| is_completed | boolean | no | Optional direct status update |

### TaskRead
| Field | Type | Required | Rules |
|---|---|---|---|
| id | integer | yes | Task ID |
| title | string | yes | Current title |
| description | string | no | Nullable |
| is_completed | boolean | yes | Current completion state |
| created_at | datetime | yes | ISO-8601 |
| updated_at | datetime | yes | ISO-8601 |

### ErrorResponse
| Field | Type | Required | Rules |
|---|---|---|---|
| error | string | yes | Human-readable summary |
| code | string | yes | Stable machine-readable code |

## Relationships

- `User` 1..* `Task` via `Task.owner_user_id`.
- Authenticated session resolves one `User` per request.

## Validation Rules

- Unauthenticated requests to task endpoints return `401`.
- Cross-user task access returns `404` and does not mutate state.
- Blank or whitespace-only titles are invalid.
- Unknown task IDs return `404`.

## State Transitions

| Current State | Action | Next State |
|---|---|---|
| incomplete | toggle-complete | complete |
| complete | toggle-complete | incomplete |
| any | update content | same completion state unless explicitly changed |
| any | delete | removed |

## Traceability Notes

- FR-001, FR-002: `Task` + `TaskCreate/TaskRead/TaskUpdate`
- FR-003: persisted `Task` table in Neon
- FR-005, FR-006, FR-007: authenticated session + `401` behavior
- FR-008: `owner_user_id` enforced on all queries/mutations
- FR-009: endpoint contract maps to lifecycle operations
