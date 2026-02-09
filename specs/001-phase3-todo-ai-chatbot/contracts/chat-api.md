# API Contract: Chat Endpoint

**Date**: 2026-02-09 | **Version**: 1.0

## `POST /api/chat`

**Authentication**: Bearer JWT (same as Phase II task endpoints)

### Request

**Headers**:
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Body**:
```json
{
  "message": "string (required, 1-2000 chars)",
  "conversation_id": "string (optional, UUID)"
}
```

**Validation**:
- `message`: Required, non-empty after trimming, max 2000 characters
- `conversation_id`: Optional. If provided, must be a valid UUID owned by the authenticated user

### Response

**200 OK** — Successful chat response:
```json
{
  "response": "I've added 'Buy groceries' to your task list.",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**400 Bad Request** — Invalid input:
```json
{
  "error": "Message must be between 1 and 2000 characters",
  "code": "bad_request"
}
```

**401 Unauthorized** — Missing or invalid JWT:
```json
{
  "error": "Missing bearer token",
  "code": "unauthorized"
}
```

**403 Forbidden** — Conversation belongs to another user:
```json
{
  "error": "Conversation not found",
  "code": "not_found"
}
```

**500 Internal Server Error** — OpenAI API failure (user message still persisted):
```json
{
  "error": "Assistant is temporarily unavailable. Your message has been saved. Please try again.",
  "code": "service_error",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Behavior

1. If `conversation_id` is omitted → create new Conversation, return its ID
2. If `conversation_id` is provided → load existing conversation (verify ownership), append to history
3. User message is always persisted to DB before agent invocation
4. On agent success → store assistant response, return it
5. On agent failure → return error with `conversation_id` so user can retry

## MCP Tools (Internal — Not HTTP Endpoints)

These are exposed by the MCP server to the OpenAI Agents SDK agent. Not callable via HTTP.

| Tool | Parameters | Returns |
|------|-----------|---------|
| `add_task(user_id, title, description?)` | user_id: str, title: str, description: str="" | Confirmation string with task details |
| `list_tasks(user_id, status?)` | user_id: str, status: str="all" | Formatted task list string |
| `complete_task(user_id, task_id)` | user_id: str, task_id: int | Confirmation string |
| `delete_task(user_id, task_id)` | user_id: str, task_id: int | Confirmation string |
| `update_task(user_id, task_id, title?, description?)` | user_id: str, task_id: int, title: str=None, description: str=None | Confirmation string |
