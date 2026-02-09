# Data Model: Phase III Todo AI Chatbot

**Date**: 2026-02-09 | **Branch**: `001-phase3-todo-ai-chatbot`

## Existing Entities (Unchanged from Phase II)

### Task
```
Table: task
- id: Integer (PK, auto-increment)
- owner_user_id: String (indexed, NOT NULL)
- title: String (max 120, NOT NULL)
- description: String (max 500, nullable)
- is_completed: Boolean (default False)
- created_at: DateTime (UTC, default now)
- updated_at: DateTime (UTC, default now)
```

**SQLModel**: `backend/src/db/models/task.py` — no changes needed.

## New Entities (Phase III)

### Conversation
```
Table: conversation
- id: String (PK, UUID4, generated on creation)
- owner_user_id: String (indexed, NOT NULL)
- created_at: DateTime (UTC, default now)
```

**Relationships**:
- 1 User → many Conversations
- 1 Conversation → many Messages

**Lifecycle**: Created on first message when no `conversation_id` provided. No update/delete in Phase III scope.

**Isolation**: Queries always filter by `owner_user_id` to enforce user-level data isolation.

### Message
```
Table: message
- id: Integer (PK, auto-increment)
- conversation_id: String (FK → conversation.id, indexed, NOT NULL)
- role: String (NOT NULL, one of: "user", "assistant")
- content: Text (NOT NULL)
- created_at: DateTime (UTC, default now)
```

**Relationships**:
- 1 Conversation → many Messages (ordered by `created_at` ASC)

**Lifecycle**: Created during chat request processing. User message stored before agent run, assistant message stored after agent response.

**Validation**:
- `role` must be one of `"user"` or `"assistant"`
- `content` for user messages limited to 2000 characters (validated at API level)

## Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│   User       │       │   Conversation   │       │   Message    │
│  (Better     │ 1───N │                  │ 1───N │              │
│   Auth)      │       │  id (UUID)       │       │  id          │
│              │       │  owner_user_id   │       │  conv_id (FK)│
│  user_id     │       │  created_at      │       │  role        │
│              │       │                  │       │  content     │
│              │       │                  │       │  created_at  │
└──────────────┘       └──────────────────┘       └──────────────┘
       │
       │ 1───N
       ▼
┌──────────────┐
│   Task       │
│              │
│  id          │
│  owner_id    │
│  title       │
│  description │
│  is_completed│
│  created_at  │
│  updated_at  │
└──────────────┘
```

## SQLModel Definitions (New Files)

### `backend/src/db/models/conversation.py`
```python
import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from src.lib_time import utcnow


class Conversation(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    owner_user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=utcnow)
```

### `backend/src/db/models/message.py`
```python
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from src.lib_time import utcnow


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    role: str = Field(max_length=10)  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=utcnow)
```

## Database Auto-Creation

Existing `SQLModel.metadata.create_all(engine)` in `backend/src/db/database.py` will auto-create these tables on startup, provided the new models are imported before `init_db()` runs. The `backend/src/db/models/__init__.py` must import the new models.
