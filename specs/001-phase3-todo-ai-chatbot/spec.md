# Feature Specification: Phase III Todo AI Chatbot

**Feature Branch**: `001-phase3-todo-ai-chatbot`
**Created**: 2026-02-09
**Status**: Draft
**Input**: Hackathon 2.docx — Phase III: Todo AI Chatbot, Basic Level Functionality

## Objective

Create an AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture. The chatbot uses OpenAI Agents SDK for AI logic and an MCP server (built with the Official MCP SDK) that exposes task operations as tools. The server is stateless — all conversation state is persisted to the database.

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              FastAPI Server                   │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │                 │
│  ChatKit UI     │────>│  │         Chat Endpoint                  │  │     │    Neon DB      │
│  (Frontend)     │     │  │  POST /api/chat                        │  │     │  (PostgreSQL)   │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │  - tasks        │
│                 │     │                  v                           │     │  - conversations│
│                 │     │  ┌────────────────────────────────────────┐  │     │  - messages     │
│                 │<────│  │      OpenAI Agents SDK                 │  │     │                 │
│                 │     │  │      (Agent + Runner)                  │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  v                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │                 │
│                 │     │  │         MCP Server                     │──┼────>│                 │
│                 │     │  │  (MCP Tools for Task Operations)       │<─┼────│                 │
│                 │     │  └────────────────────────────────────────┘  │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

**Three-layer architecture inside FastAPI:**
1. **Chat Endpoint** (`POST /api/chat`) — receives user messages, returns assistant responses
2. **OpenAI Agents SDK** — processes natural language, decides which tools to invoke
3. **MCP Server** — exposes task CRUD operations as tools the agent can call

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend Chat UI | OpenAI ChatKit |
| Backend Server | FastAPI (existing from Phase II) |
| AI Agent Logic | OpenAI Agents SDK |
| Tool Server | MCP Server (Official MCP SDK) |
| Database | Neon Serverless PostgreSQL (existing from Phase II) |
| ORM | SQLModel (existing from Phase II) |
| Authentication | Better Auth + JWT (existing from Phase II) |
| Spec-Driven Dev | Claude Code + Spec-Kit Plus |

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Manage Tasks in Natural Language (Priority: P1)

As an authenticated user, I can manage my todo list by chatting in plain language instead of using form-based task controls.

**Why this priority**: Natural language task management is the core value of Phase III.

**Independent Test**: Send natural language task commands in a chat session and confirm corresponding task updates in the database.

**Acceptance Scenarios**:

1. **Given** an authenticated user with an active chat session, **When** the user says "Add a task to buy groceries," **Then** the `add_task` MCP tool is invoked, a new task is created in the database, and the assistant confirms the action.
2. **Given** an authenticated user with existing tasks, **When** the user asks "Show me all my tasks," **Then** the `list_tasks` MCP tool is invoked and the assistant returns the user's task list.
3. **Given** an authenticated user with a pending task, **When** the user says "Mark task 3 as complete," **Then** the `complete_task` MCP tool is invoked, the task is marked complete, and the assistant confirms.
4. **Given** an authenticated user with task ownership, **When** the user says "Update task 2 title to 'Buy organic groceries'," **Then** the `update_task` MCP tool is invoked and the assistant confirms the change.
5. **Given** an authenticated user with task ownership, **When** the user says "Delete task 5," **Then** the `delete_task` MCP tool is invoked, the task is removed, and the assistant confirms.

---

### User Story 2 — Continue Conversations Across Requests (Priority: P1)

As an authenticated user, I can continue the same conversation over multiple requests and after service restarts without losing chat history.

**Why this priority**: Persistent context is required for coherent AI behavior in a stateless request lifecycle.

**Independent Test**: Send multiple turns in one conversation, restart the service, send another turn that still uses prior context.

**Acceptance Scenarios**:

1. **Given** a conversation identifier from a prior exchange, **When** the user sends a new message with that identifier, **Then** the assistant uses prior conversation context and returns a relevant response.
2. **Given** no conversation identifier is supplied, **When** the user sends the first message, **Then** a new conversation is created and its identifier is returned.
3. **Given** a previous conversation exists, **When** the backend service is restarted and the user continues, **Then** chat history is still available and the conversation resumes.

---

### User Story 3 — Receive Safe and Clear Assistant Feedback (Priority: P2)

As an authenticated user, I receive clear confirmations for successful actions and understandable feedback when an action cannot be completed.

**Why this priority**: Reliable confirmation and error feedback are critical to user trust.

**Independent Test**: Trigger valid and invalid commands and verify response clarity, correctness, and safety.

**Acceptance Scenarios**:

1. **Given** a valid task command, **When** the assistant completes the action, **Then** the response clearly states what changed (e.g., "Task 'Buy groceries' has been created.").
2. **Given** a request referencing a non-existent task, **When** the assistant attempts the action, **Then** the response explains the issue and suggests the next step.
3. **Given** an ambiguous command, **When** intent cannot be resolved confidently, **Then** the assistant asks a clarifying follow-up instead of performing a risky action.

---

### User Story 4 — Chat via ChatKit Frontend (Priority: P1)

As an authenticated user, I can interact with the AI chatbot through a ChatKit-based chat interface in the frontend.

**Why this priority**: The doc requires a ChatKit-based UI as the primary interaction surface.

**Independent Test**: Open the frontend, navigate to the chat interface, send a message, and verify a response appears.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the frontend, **When** the user navigates to the chat page, **Then** a ChatKit-powered chat interface is displayed.
2. **Given** the chat interface is loaded, **When** the user types a message and sends it, **Then** the message is sent to `POST /api/chat` and the assistant's response is displayed.
3. **Given** an existing conversation, **When** the user returns to the chat page, **Then** the previous conversation can be resumed.

### Edge Cases

- User message is empty, whitespace-only, or exceeds 2000 characters.
- User requests completion, update, or deletion for a task ID that does not exist for that user.
- User references a task by vague text (e.g., "delete the meeting task") and multiple tasks match.
- Conversation identifier is invalid, belongs to another user, or is malformed.
- Underlying task action fails mid-request; assistant must avoid duplicate or contradictory confirmations.
- Repeated identical messages are sent due to client retries.
- OpenAI API is temporarily unavailable or returns an error — the user message is persisted, a user-friendly error response is returned, and the user can retry manually.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose a `POST /api/chat` endpoint that accepts a user message (and optional conversation ID) and returns an assistant response with conversation ID.
- **FR-002**: System MUST use OpenAI Agents SDK to process natural language and determine which MCP tools to invoke.
- **FR-003**: System MUST implement an MCP server (using Official MCP SDK) exposing the following 5 tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`.
- **FR-004**: System MUST create a new conversation when no conversation identifier is provided and return that identifier to the client.
- **FR-005**: System MUST persist conversation and message history to the database so each request can reconstruct prior context.
- **FR-006**: System MUST process each chat request statelessly — the server holds NO in-memory session state between requests. All state is reconstructed from the database.
- **FR-007**: System MUST enforce user-level data isolation so users can only access and modify their own tasks, conversations, and messages.
- **FR-008**: System MUST include action confirmations for successful task changes in assistant responses.
- **FR-009**: System MUST gracefully handle invalid commands, missing tasks, and tool/action failures with user-friendly responses.
- **FR-010**: System MUST expose, in each chat response, the conversation identifier and assistant response text.
- **FR-011**: System MUST support multi-turn conversation continuation by accepting an existing conversation identifier.
- **FR-012**: System MUST log sufficient interaction records to audit user request, assistant response, and resulting task action outcomes.
- **FR-013**: System MUST allow users to resume prior conversations after backend restarts, preserving context from persisted history.
- **FR-014**: System MUST provide a ChatKit-based frontend chat interface using **hosted mode** (OpenAI-hosted widget). Domain allowlist MUST be configured in the OpenAI platform settings for the deployment URL.
- **FR-015**: System MUST authenticate all chat requests using the existing JWT Bearer token mechanism from Phase II.

### Chat API Endpoint Specification

#### `POST /api/chat`

**Request**:
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional-uuid-string"
}
```

- `message`: Required, non-empty, maximum **2000 characters**.
- `conversation_id`: Optional UUID string. Omit to create a new conversation.

**Response**:
```json
{
  "response": "I've added 'Buy groceries' to your task list.",
  "conversation_id": "uuid-string"
}
```

- If `conversation_id` is omitted, a new conversation is created.
- If `conversation_id` is provided, the conversation history is loaded from the database and appended.
- Authentication: JWT Bearer token required (same as Phase II task endpoints).

### MCP Tools Specification

The MCP server MUST expose the following tools for the AI agent:

| Tool | Parameters | Description |
|------|-----------|-------------|
| `add_task` | `title` (string, required), `description` (string, optional) | Creates a new task for the authenticated user |
| `list_tasks` | `status` (string, optional: "all", "pending", "completed") | Lists tasks for the authenticated user, optionally filtered by status |
| `complete_task` | `task_id` (integer, required) | Marks the specified task as complete |
| `delete_task` | `task_id` (integer, required) | Deletes the specified task |
| `update_task` | `task_id` (integer, required), `title` (string, optional), `description` (string, optional) | Updates the specified task's fields |

All MCP tools MUST enforce user-level data isolation (only operate on tasks owned by the authenticated user). The MCP tools are stateless — they read from and write to the database directly.

The MCP server MUST use **stdio** transport — it runs as a subprocess within the FastAPI server process, and the OpenAI Agents SDK connects to it via stdin/stdout.

### Agent Behavior Specification

The AI agent MUST follow this stateless conversation flow per request:

1. Receive user message via `POST /api/chat`
2. Fetch conversation history from database (if `conversation_id` provided)
3. Build message array for agent (history + new message)
4. Store user message in database
5. Run agent with MCP tools (OpenAI Agents SDK)
6. Agent invokes appropriate MCP tool(s) based on user intent
7. Store assistant response in database
8. Return response to client
9. Server holds NO state (ready for next request)

### Natural Language Commands

The chatbot MUST understand and respond to commands such as:

- "Add a task to buy groceries"
- "Show me all my tasks"
- "What tasks do I have pending?"
- "Mark task 3 as complete"
- "Delete task 5"
- "Update task 2 title to 'Buy organic groceries'"
- "What tasks are completed?"
- "Remove all completed tasks"
- "Reschedule my morning meetings to 2 PM" (interpreted as update)

### Key Entities *(include if feature involves data)*

- **Task**: Existing user-owned todo item from Phase II (title, optional description, completion state, audit timestamps). Unchanged.
- **Conversation**: A user-owned chat session container with `id` (UUID), `owner_user_id`, and `created_at`.
- **Message**: A single user or assistant utterance linked to a conversation with `id`, `conversation_id`, `role` (user/assistant), `content`, and `created_at`.

### Database Models (New Tables)

**conversations**:
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | Primary key |
| owner_user_id | String | Indexed, NOT NULL |
| created_at | Timestamp | NOT NULL, default UTC now |

**messages**:
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary key, auto-increment |
| conversation_id | UUID | Foreign key -> conversations.id, NOT NULL |
| role | String | "user" or "assistant", NOT NULL |
| content | Text | NOT NULL |
| created_at | Timestamp | NOT NULL, default UTC now |

## Assumptions

- Authentication and user identity from Phase II remain available and valid for Phase III chat interactions.
- Existing task semantics from Phase II remain unchanged (pending/completed lifecycle and ownership rules).
- The existing `tasks` table and CRUD service from Phase II are preserved; MCP tools delegate to the existing task service layer.
- OpenAI API key is available as an environment variable (`OPENAI_API_KEY`).
- The OpenAI Agents SDK agent uses the **gpt-4o-mini** model for cost-effective, low-latency tool-calling.
- Users interact through one active conversational interface per session, with optional continuation of older conversations.

## Deliverables

GitHub repository with:
- `/frontend` — ChatKit-based UI with chat interface
- `/backend` — FastAPI + OpenAI Agents SDK + MCP Server
- `/specs` — Specification files for agent and MCP tools
- Database migration scripts (or auto-creation via SQLModel)
- README with setup instructions

Working chatbot that can:
- Manage tasks through natural language via MCP tools
- Maintain conversation context via database (stateless server)
- Provide helpful responses with action confirmations
- Handle errors gracefully
- Resume conversations after server restart

## Environment Variables (New for Phase III)

| Var | Location | Purpose |
|-----|----------|---------|
| `OPENAI_API_KEY` | `backend/.env` | OpenAI API key for Agents SDK |
| `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` | `frontend/.env.local` | OpenAI ChatKit domain key (for hosted ChatKit) |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 95% of valid natural language todo commands (add, list, complete, delete, update) complete the intended action on first attempt in acceptance testing.
- **SC-002**: 100% of tested cross-user access attempts are rejected for task and conversation data.
- **SC-003**: At least 90% of tested chat requests return a user-visible response within 3 seconds under normal demo load.
- **SC-004**: At least 95% of successful task-changing commands include explicit user-facing confirmation of the action taken.
- **SC-005**: 100% of sampled resumed conversations after service restart preserve prior context and continue without data loss.
- **SC-006**: All 5 MCP tools (`add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`) function correctly when invoked by the agent.

## Constitution Alignment *(mandatory)*

### Phase Mapping

- **Target Phase**: Phase III
- **Prerequisite Check**: Requires validated Phase I-II capabilities for authenticated multi-user todo management, persistent storage, and ownership isolation; this feature extends those capabilities with conversational interaction while preserving existing user/task behavior.

### Spec-Driven Execution Evidence

- **Spec Source**: `Hackathon 2.docx` (Phase III: Todo AI Chatbot, Basic Level Functionality section)
- **Planned Sequence**: `Specify -> Plan -> Tasks -> Implement`
- **Manual Coding Exception**: None

### Traceability Commitments

- [x] Every functional requirement maps to at least one planned task.
- [x] Every user story has at least one validation method (automated test or scripted acceptance check).
- [x] Submission evidence needed for this scope is listed (repo/demo/deploy links when applicable).

### Test-Driven Development Commitments

- [x] Python behavior changes include tests authored first using `pytest`.
- [x] Test cases are expected to fail before implementation (Red), then pass after implementation (Green), with cleanup/refinement noted (Refactor).
- [x] The spec lists the command used to run relevant tests: `cd backend && uv run pytest tests/ -v`.

## Clarifications

### Session 2026-02-09

- Q: How should the MCP server connect to the OpenAI Agents SDK within the FastAPI process? → A: stdio transport — MCP server runs as a subprocess; agent connects via stdin/stdout.
- Q: Which OpenAI model should the Agents SDK use for the chatbot? → A: gpt-4o-mini — fast, cheap, strong tool-calling capability.
- Q: How should the system handle OpenAI API failures during a chat request? → A: Return user-friendly error, keep user message persisted; user retries manually.
- Q: Should the ChatKit frontend use hosted mode or self-hosted mode? → A: Hosted mode — OpenAI-hosted widget with domain allowlist configuration.
- Q: What is the maximum message content size per chat request? → A: 2000 characters.
