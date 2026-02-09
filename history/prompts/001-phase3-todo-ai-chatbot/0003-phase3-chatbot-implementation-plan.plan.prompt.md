---
id: "0003"
title: phase3-chatbot-implementation-plan
stage: plan
date: 2026-02-09
surface: claude-code
model: claude-opus-4-6
feature: 001-phase3-todo-ai-chatbot
branch: 001-phase3-todo-ai-chatbot
user: harisrehman
command: /sp.plan
labels: [plan, phase3, chatbot, agents-sdk, mcp, chatkit]
links:
  spec: specs/001-phase3-todo-ai-chatbot/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - specs/001-phase3-todo-ai-chatbot/plan.md
  - specs/001-phase3-todo-ai-chatbot/research.md
  - specs/001-phase3-todo-ai-chatbot/data-model.md
  - specs/001-phase3-todo-ai-chatbot/quickstart.md
  - specs/001-phase3-todo-ai-chatbot/contracts/chat-api.md
  - specs/001-phase3-todo-ai-chatbot/contracts/chatkit-proxy.md
tests:
  - n/a (planning stage only)
---

## Prompt

/sp.plan — Execute the implementation planning workflow for Phase III Todo AI Chatbot. Generate research.md, data-model.md, contracts/, quickstart.md, and fill plan.md template with architecture, component design, testing strategy, and constitution checks.

## Response snapshot

Completed Phase 0 (Research) and Phase 1 (Design & Contracts) planning for Phase III.

Phase 0 Research resolved 5 technology decisions:
1. OpenAI Agents SDK (`openai-agents` package, `from agents import Agent, Runner`)
2. MCP SDK (`mcp` package, `from mcp.server.fastmcp import FastMCP`, stdio transport)
3. ChatKit (`@openai/chatkit-react`, self-hosted mode with proxy to custom backend)
4. Stateless architecture (per-request DB reconstruction)
5. User context passing (user_id as MCP tool parameter)

Phase 1 Design produced:
- data-model.md: 2 new tables (conversation, message) + existing task table unchanged
- contracts/chat-api.md: POST /api/chat with request/response schemas and error codes
- contracts/chatkit-proxy.md: Next.js proxy route translating ChatKit format to custom API
- quickstart.md: Full setup guide for both backend and frontend

Plan.md completed with 7 constitution checks (all PASS), full project structure, 7 component designs, integration flow, testing strategy, and dependency changes.

## Outcome

- Impact: Complete implementation plan ready for /sp.tasks
- Tests: n/a (planning stage)
- Files: 6 new files created, 1 file updated (plan.md)
- Next prompts: /sp.tasks
- Reflection: Key finding — ChatKit hosted mode talks directly to OpenAI, cannot route to custom backend. Self-hosted mode with Next.js proxy is required.

## Evaluation notes (flywheel)

- Failure modes observed: Web fetch failed on several blog sites (403/429); intermediate research output was sufficient
- Graders run and results (PASS/FAIL): Constitution check PASS (all 7 gates)
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
