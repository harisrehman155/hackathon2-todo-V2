# API Contract: ChatKit Proxy Route

**Date**: 2026-02-09 | **Version**: 1.0

## Overview

ChatKit in self-hosted mode sends requests in OpenAI Chat Completions format to a backend URL. Since our actual chat logic runs on FastAPI (`POST /api/chat`), a Next.js API route acts as a proxy/translator between ChatKit's format and our custom format.

## `POST /api/chatkit` (Next.js API Route)

**Purpose**: Proxy between ChatKit frontend component and FastAPI backend.

### Flow

```
ChatKit UI → POST /api/chatkit (Next.js) → POST http://localhost:8000/api/chat (FastAPI) → Response
```

### Request (from ChatKit — OpenAI format)

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    { "role": "user", "content": "Add a task to buy groceries" }
  ],
  "stream": false
}
```

### Translation Logic

1. Extract the last user message from `messages` array
2. Extract `conversation_id` from custom metadata or thread context (if available)
3. Forward JWT token from request headers
4. Call FastAPI `POST /api/chat` with `{ message, conversation_id }`
5. Receive response from FastAPI
6. Translate back to OpenAI Chat Completions format for ChatKit

### Response (to ChatKit — OpenAI format)

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I've added 'Buy groceries' to your task list."
      },
      "finish_reason": "stop"
    }
  ]
}
```

## Environment Variables

| Var | Default | Purpose |
|-----|---------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | `http://localhost:8000` | FastAPI backend URL |
| `NEXT_PUBLIC_CHATKIT_API_DOMAIN_KEY` | `domain_pk_localhost_dev` | ChatKit domain key |
