# Quickstart: Phase III Todo AI Chatbot

## Prerequisites

- Phase II backend running (`cd backend && uv run uvicorn src.main:app --reload --port 8000`)
- Phase II frontend running (`cd frontend && npm run dev`)
- OpenAI API key with access to gpt-4o-mini
- Neon PostgreSQL database (from Phase II)

## Backend Setup

### 1. Install new dependencies

```bash
cd backend
uv add openai-agents "mcp[cli]"
```

### 2. Add environment variables

Add to `backend/.env`:
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 3. Create MCP server

Create `backend/src/mcp/server.py` with the 5 todo tools (`add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`).

### 4. Create chat route

Create `backend/src/api/routes/chat.py` with `POST /api/chat` endpoint.

### 5. Create chat service

Create `backend/src/services/chat_service.py` with agent orchestration logic.

### 6. Register router

Add chat router to `backend/src/main.py`.

### 7. Run backend

```bash
cd backend && uv run uvicorn src.main:app --reload --port 8000
```

### 8. Test endpoint

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer <your-jwt>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

## Frontend Setup

### 1. Install ChatKit

```bash
cd frontend
npm install @openai/chatkit-react --legacy-peer-deps
```

### 2. Add environment variable

Add to `frontend/.env.local`:
```
NEXT_PUBLIC_CHATKIT_API_DOMAIN_KEY=domain_pk_localhost_dev
```

### 3. Create ChatKit proxy route

Create `frontend/src/app/api/chatkit/route.ts` — translates between ChatKit format and FastAPI `POST /api/chat`.

### 4. Create chat page

Create `frontend/src/app/chat/page.tsx` with ChatKit component.

### 5. Run frontend

```bash
cd frontend && npm run dev
```

### 6. Test

Navigate to `http://localhost:3000/chat` and send a message.

## Running Tests

```bash
cd backend && uv run pytest tests/ -v
```

## New File Summary

### Backend (new files)
```
backend/src/
├── mcp/
│   ├── __init__.py
│   └── server.py              # MCP server with 5 todo tools
├── api/routes/
│   └── chat.py                # POST /api/chat endpoint
├── services/
│   └── chat_service.py        # Agent orchestration + conversation management
├── db/models/
│   ├── conversation.py        # Conversation SQLModel
│   └── message.py             # Message SQLModel
└── schemas/
    └── chat.py                # ChatRequest, ChatResponse Pydantic models
```

### Frontend (new files)
```
frontend/src/
├── app/
│   ├── api/chatkit/
│   │   └── route.ts           # ChatKit proxy to FastAPI
│   └── chat/
│       └── page.tsx           # Chat page with ChatKit component
└── lib/api/
    └── chat.ts                # Chat API client helpers
```
