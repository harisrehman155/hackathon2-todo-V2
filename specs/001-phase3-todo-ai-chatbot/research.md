# Phase 0 Research: Phase III Todo AI Chatbot

**Date**: 2026-02-09 | **Branch**: `001-phase3-todo-ai-chatbot`

## 1. OpenAI Agents SDK (Python)

**Decision**: Use `openai-agents` package for AI agent logic.

**Rationale**: Official OpenAI framework with native MCP server support, async Runner, and tool-calling built in. Lightweight and purpose-built for agent workflows.

**Alternatives considered**:
- LangChain — heavier, more dependencies, overkill for this scope
- Direct OpenAI API — no built-in MCP integration, more boilerplate

**Key findings**:
- **Package**: `openai-agents` (PyPI), installed via `uv add openai-agents`
- **Import**: `from agents import Agent, Runner` (module name is `agents`, not `openai_agents`)
- **Agent creation**: `Agent(name=..., instructions=..., mcp_servers=[server], model="gpt-4o-mini")`
- **Execution**: `result = await Runner.run(agent, input_text)` — async, returns `RunResult`
- **Output access**: `result.final_output` for the agent's text response
- **MCP integration**: `MCPServerStdio` class from `agents.mcp` for stdio transport
- **Lifecycle**: Use `async with MCPServerStdio(...) as server:` context manager
- **MCPServerStdio params**: `{"command": "uv", "args": ["run", "mcp_server.py"]}`

**Minimal integration pattern**:
```python
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

async with MCPServerStdio(
    name="Todo MCP",
    params={"command": "uv", "args": ["run", "src/mcp/server.py"]},
) as server:
    agent = Agent(
        name="Todo Assistant",
        instructions="You help users manage their todo list.",
        mcp_servers=[server],
        model="gpt-4o-mini",
    )
    result = await Runner.run(agent, "Add a task to buy groceries")
    print(result.final_output)
```

## 2. MCP Server (Official MCP SDK)

**Decision**: Use `mcp` package (official SDK) with `FastMCP` for tool definitions.

**Rationale**: Official SDK from Model Context Protocol project. FastMCP 1.0 was merged into the official `mcp` package, providing the `@mcp.tool()` decorator pattern. Simpler than standalone `fastmcp` package and sufficient for our 5 tools.

**Alternatives considered**:
- Standalone `fastmcp` (v2+) — more features than needed, separate package
- Raw MCP protocol implementation — too low-level

**Key findings**:
- **Package**: `mcp` (PyPI), installed via `uv add "mcp[cli]"`
- **Import**: `from mcp.server.fastmcp import FastMCP`
- **Server creation**: `mcp = FastMCP("Todo Tools")`
- **Tool definition**: `@mcp.tool()` decorator on async functions
- **Transport**: stdio (default) — `mcp.run()` starts stdio server
- **Tool parameters**: Type-annotated function parameters become tool schema
- **User context passing**: MCP tools receive user_id via tool parameter or context injection

**Tool definition pattern**:
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Todo Tools")

@mcp.tool()
async def add_task(user_id: str, title: str, description: str = "") -> str:
    """Create a new task for the user."""
    # DB operations here
    return f"Task '{title}' created successfully."

@mcp.tool()
async def list_tasks(user_id: str, status: str = "all") -> str:
    """List tasks for the user, optionally filtered by status."""
    # DB operations here
    return "1. Buy groceries (pending)\n2. Call mom (completed)"

if __name__ == "__main__":
    mcp.run()  # starts stdio transport
```

## 3. OpenAI ChatKit (Frontend)

**Decision**: Use `@openai/chatkit-react` in self-hosted mode with custom backend URL pointing to our FastAPI `POST /api/chat`.

**Rationale**: The doc requires ChatKit, but hosted mode connects directly to OpenAI — it does NOT support routing to a custom backend. Self-hosted mode allows `url` + custom `fetch` to point to our FastAPI backend while still using the ChatKit UI component. This gives us the ChatKit UI requirement while routing requests to our agent backend.

**Critical finding**: ChatKit's "hosted mode" uses `getClientSecret` to talk directly to OpenAI's API — it does NOT send messages to a custom backend. For our architecture (custom agent + MCP on FastAPI), we MUST use self-hosted mode with a custom URL.

**Alternatives considered**:
- Hosted mode — won't work because it talks to OpenAI directly, not our custom backend
- Custom React chat UI from scratch — more work, doesn't satisfy "ChatKit" requirement
- Vercel AI SDK Chat UI — different library, doesn't meet doc requirement

**Key findings**:
- **Packages**: `@openai/chatkit-react` (npm)
- **Self-hosted config**: `api: { url: '/api/chatkit', domainKey: '...', fetch: customFetch }`
- **Domain key**: `domain_pk_localhost_dev` for local dev, real key from OpenAI platform for production
- **Custom fetch**: Inject JWT Authorization header for auth
- **Environment vars**: `NEXT_PUBLIC_CHATKIT_API_DOMAIN_KEY` for domain key

**Integration pattern**:
```tsx
import { useChatKit, ChatKit } from '@openai/chatkit-react';

function ChatPage() {
  const { control } = useChatKit({
    api: {
      url: '/api/chatkit',  // proxied to FastAPI backend
      domainKey: process.env.NEXT_PUBLIC_CHATKIT_API_DOMAIN_KEY!,
      fetch: async (url, init) => {
        const token = await getAuthToken();
        const headers = new Headers(init?.headers);
        headers.set('Authorization', `Bearer ${token}`);
        return fetch(url, { ...init, headers });
      },
    },
  });
  return <ChatKit control={control} />;
}
```

**Backend compatibility note**: ChatKit self-hosted mode expects the backend to implement the OpenAI Chat Completions API schema. Our FastAPI backend at `/api/chatkit` must return responses in OpenAI-compatible format, OR we use a Next.js API route as a proxy that translates between ChatKit format and our custom `POST /api/chat` format.

## 4. Stateless Chat Architecture

**Decision**: Per-request database reconstruction of conversation context.

**Rationale**: Matches doc requirement for stateless server. Each request loads history from DB, appends new message, runs agent, stores response, returns result.

**Key findings**:
- No in-memory session state between requests
- Conversation history stored in `messages` table ordered by `created_at`
- History loaded per request and passed to Agent via Runner
- Agent can use `conversation_id` parameter for multi-turn context
- Server restarts preserve all state (in DB)

## 5. User Context Passing to MCP Tools

**Decision**: Pass `user_id` as a parameter in the agent instructions and tool calls.

**Rationale**: MCP tools run as a separate process (stdio). The simplest approach is to inject the authenticated `user_id` into the agent's system instructions so the agent passes it to tool calls. This avoids complex cross-process auth state.

**Pattern**: Agent instructions include `"The current user ID is {user_id}. Always pass this user_id to tools."` and each MCP tool accepts `user_id` as a required parameter.
