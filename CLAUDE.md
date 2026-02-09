@AGENTS.md

## Phase Versioning
- Each phase lives on its own git branch — do NOT copy phase code across branches
- Phase I code is on branch `001-phase1-todo-spec` / `phase1`
- Phase II code is on branch `002-phase2-delivery` / `phase2`
- To access a previous phase: `git checkout <branch-name>`
- No root `pyproject.toml` — all Python deps and config live in `backend/pyproject.toml`

## Tech Stack Reference

### Backend: FastAPI + SQLModel
- **Run dev:** `cd backend && uv run uvicorn src.main:app --reload --port 8000`
- **Run tests:** `cd backend && uv run pytest tests/ -v`
- **Module prefix:** `src.` in all imports (backend is self-contained)
- **Config:** `@dataclass(frozen=True)` in `backend/src/config.py`, reads `backend/.env` via `python-dotenv`
- **DB driver:** `psycopg[binary]` for Neon PostgreSQL, `sqlite` fallback for tests
- **Dependencies:** All in `backend/pyproject.toml` (includes `fastapi[standard]`, `psycopg[binary]`, `python-dotenv`)

### Frontend: Next.js 15 + React 19
- **Run dev:** `cd frontend && npm run dev`
- **Run tests:** `cd frontend && npm run test` (vitest)
- **Build:** `cd frontend && npx next build`
- **Path alias:** `@/*` -> `./src/*` (configured in `tsconfig.json` with `baseUrl` + `paths`)
- **Module resolution:** `"moduleResolution": "bundler"` (required for `@/` imports)
- **npm install:** Always use `--legacy-peer-deps` (vite peer conflict with @tanstack/react-start from better-auth)

### Authentication: Better Auth + PyJWT Bridge
- **JWT:** HS256, audience=`hackathon2`, issuer=`better-auth`
- **Shared secret:** `BETTER_AUTH_SECRET` (frontend) = `JWT_SECRET` (backend)
- **Better Auth server:** `frontend/src/lib/auth/server.ts`
- **Better Auth client:** `frontend/src/lib/auth/client.ts` using `createAuthClient` from `better-auth/react`
- **JWT plugin gotcha:** `jwks.remoteUrl` is REQUIRED even when using custom `sign` function
- **Token retrieval:** `authClient.token()` returns `{ data: { token } }`
- **Auth guard:** `frontend/src/middleware.ts` using `getSessionCookie` from `better-auth/cookies`
- **API route:** `frontend/src/app/api/auth/[...all]/route.ts` — catch-all handler

### Database: Neon PostgreSQL
- **Backend URL format:** `postgresql+psycopg://user:pass@host/db?sslmode=require` (note `+psycopg` dialect)
- **Frontend URL format:** `postgresql://user:pass@host/db?sslmode=require` (standard for `pg` driver)
- **Backend tables:** Auto-created by `SQLModel.metadata.create_all()` on startup
- **Auth tables:** Auto-created by Better Auth on first request (user, session, account, verification, jwks)
- **Node.js `pg` SSL:** Use `ssl: { rejectUnauthorized: false }` for Neon pooler connections
- **pg driver warning:** SSL mode warning is cosmetic — connection works fine

### Tailwind CSS v4
- **CSS-first config:** `@import "tailwindcss"` + `@theme { }` in `globals.css`
- **PostCSS:** `postcss.config.mjs` with `@tailwindcss/postcss` plugin
- **No `tailwind.config.ts` needed** in v4 — all config goes in CSS

## Environment Variables

### Backend (`backend/.env`)
| Var | Purpose | Example |
|-----|---------|---------|
| `DATABASE_URL` | Neon PostgreSQL (psycopg dialect) | `postgresql+psycopg://...` |
| `JWT_SECRET` | Shared secret for JWT verification | Must match `BETTER_AUTH_SECRET` |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `JWT_AUDIENCE` | JWT audience claim | `hackathon2` |
| `JWT_ISSUER` | JWT issuer claim | `better-auth` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:3000` |

### Frontend (`frontend/.env.local`)
| Var | Purpose | Example |
|-----|---------|---------|
| `BETTER_AUTH_SECRET` | Auth signing secret | Must match `JWT_SECRET` |
| `BETTER_AUTH_URL` | Better Auth base URL | `http://localhost:3000` |
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL | `http://localhost:8000` |
| `DATABASE_URL` | Neon PostgreSQL (for Better Auth) | `postgresql://...` |

## Frontend Design Rules

1. **Use `ui-ux-pro-max` skill for all frontend UI/UX work.**
   - Run `python3 .claude/skills/ui-ux-pro-max/scripts/search.py` for design system generation
   - Always generate a design system with `--design-system` before implementing UI
   - Persist design system with `--persist` for cross-session consistency

2. **Theme: Soft / Light / Glassmorphism**
   - Use glassmorphism style: frosted glass cards with `backdrop-blur`, semi-transparent backgrounds
   - Light mode primary: soft whites, pale grays, subtle teal accents
   - Glass card backgrounds: `bg-white/70` to `bg-white/80` with `backdrop-blur-lg`
   - Borders: `border-white/20` or `border-gray-200/50` for glass effect
   - Shadows: soft, diffused box-shadows (no harsh drop shadows)
   - Typography: clean sans-serif fonts (Space Grotesk headings, Inter or Source Sans 3 body)
   - Accent color: teal/cyan for interactive elements
   - Rounded corners: generous border-radius (`rounded-xl` to `rounded-2xl`)

3. **UI Quality Standards (from ui-ux-pro-max)**
   - No emojis as icons — use SVG icons (Lucide, Heroicons)
   - All clickable elements must have `cursor-pointer`
   - Hover transitions: 150-300ms using `transition-colors`
   - Minimum touch target: 44x44px
   - Color contrast: minimum 4.5:1 ratio
   - Focus states visible on all interactive elements
   - `prefers-reduced-motion` respected for animations
   - Responsive at 375px, 768px, 1024px, 1440px breakpoints

4. **Pre-Delivery UI Checklist**
   - [ ] No emoji icons (SVG only)
   - [ ] Glass cards visible with sufficient contrast
   - [ ] Hover states don't cause layout shift
   - [ ] All forms have proper labels
   - [ ] Light mode text contrast >= 4.5:1
   - [ ] Responsive on mobile and desktop
   - [ ] Loading and error states implemented

## Phase III: AI Chatbot (branch: 001-phase3-todo-ai-chatbot)

### New Backend Dependencies
- `openai-agents` — OpenAI Agents SDK (`from agents import Agent, Runner`)
- `mcp[cli]` — MCP SDK (`from mcp.server.fastmcp import FastMCP`)
- Install: `cd backend && uv add openai-agents "mcp[cli]"`

### New Frontend Dependencies
- `@openai/chatkit-react` — ChatKit React component
- Install: `cd frontend && npm install @openai/chatkit-react --legacy-peer-deps`

### Phase III Architecture
- **Chat endpoint**: `POST /api/chat` (message + optional conversation_id → response + conversation_id)
- **MCP Server**: `backend/src/mcp/server.py` — 5 tools (add_task, list_tasks, complete_task, delete_task, update_task)
- **MCP transport**: stdio — runs as subprocess via `MCPServerStdio` from `agents.mcp`
- **Agent**: `Agent(name=..., instructions=..., mcp_servers=[server], model="gpt-4o-mini")`
- **Execution**: `result = await Runner.run(agent, messages)` → `result.final_output`
- **User isolation in MCP**: user_id passed as tool parameter (cross-process, no shared auth state)
- **ChatKit mode**: Self-hosted (NOT hosted — hosted talks directly to OpenAI, cannot route to custom backend)
- **ChatKit proxy**: Next.js API route at `/api/chatkit` translates OpenAI format ↔ custom `POST /api/chat`
- **Stateless**: All conversation state in DB (conversation + message tables), reconstructed per request

### Phase III New Tables
- `conversation`: id (UUID PK), owner_user_id (indexed), created_at
- `message`: id (int PK), conversation_id (FK), role ("user"/"assistant"), content, created_at
- Auto-created via `SQLModel.metadata.create_all()` — new models must be imported in `backend/src/db/models/__init__.py`

### Phase III Environment Variables
| Var | Location | Purpose |
|-----|----------|---------|
| `OPENAI_API_KEY` | `backend/.env` | OpenAI API key for Agents SDK |
| `NEXT_PUBLIC_CHATKIT_API_DOMAIN_KEY` | `frontend/.env.local` | ChatKit domain key (use `domain_pk_localhost_dev` for local dev) |

### Phase III New Files
```
backend/src/mcp/__init__.py, server.py          # MCP server with 5 todo tools
backend/src/api/routes/chat.py                   # POST /api/chat endpoint
backend/src/services/chat_service.py             # Agent orchestration + conversation mgmt
backend/src/db/models/conversation.py, message.py # New SQLModels
backend/src/schemas/chat.py                      # ChatRequest, ChatResponse
frontend/src/app/api/chatkit/route.ts            # ChatKit proxy to FastAPI
frontend/src/app/chat/page.tsx                   # Chat page with ChatKit UI
frontend/src/lib/api/chat.ts                     # Chat API client helpers
```

### Phase III SDD Progress
- [x] Specify (spec.md)
- [x] Clarify (5 questions resolved)
- [x] Plan (plan.md + research.md + data-model.md + contracts/ + quickstart.md)
- [x] Tasks (tasks.md — 36 tasks, 7 phases, 4 user stories)
- [ ] Implement (next: /sp.implement)
