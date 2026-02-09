# Hackathon 2 — Task Board

A full-stack task management web app built with FastAPI, Next.js, Better Auth, and Neon PostgreSQL. Uses Spec-Driven Development (SDD) across five phases.

---

## Quick Start

### Prerequisites

- Python 3.13+ with [uv](https://docs.astral.sh/uv/)
- Node.js 18+
- Neon PostgreSQL database (or SQLite for local dev)

### 1. Clone and install dependencies

```bash
# Backend
cd backend
uv sync --group dev

# Frontend
cd ../frontend
npm install --legacy-peer-deps
```

### 2. Configure environment variables

**Backend** — create `backend/.env`:
```env
DATABASE_URL=postgresql+psycopg://user:pass@your-neon-host/dbname?sslmode=require
JWT_SECRET=your-secret-at-least-32-chars
JWT_ALGORITHM=HS256
JWT_AUDIENCE=hackathon2
JWT_ISSUER=better-auth
CORS_ORIGINS=http://localhost:3000
```

**Frontend** — create `frontend/.env.local`:
```env
BETTER_AUTH_SECRET=same-secret-as-JWT_SECRET-above
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
DATABASE_URL=postgresql://user:pass@your-neon-host/dbname?sslmode=require
```

> Note: `BETTER_AUTH_SECRET` and `JWT_SECRET` must be the same value — this is the shared HS256 signing key.

### 3. Start both servers

Open **two terminals**:

**Terminal 1 — Backend (FastAPI on port 8000):**
```bash
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

**Terminal 2 — Frontend (Next.js on port 3000):**
```bash
cd frontend
npm run dev
```

### 4. Open the app

- **App:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs

### 5. Test flow

1. Visit http://localhost:3000 — redirects to `/signin`
2. Click "Sign up" — create account with name, email, password
3. Redirected to `/tasks` — create, toggle, and delete tasks
4. Tasks persist in Neon PostgreSQL
5. Sign out, sign back in — your tasks are still there

---

## Run Tests

```bash
# Backend (11 tests) — from backend/
cd backend
uv run pytest tests/ -v

# Frontend (3 tests) — from frontend/
cd frontend
npm run test
```

---

## Phase II Achievement Summary

### What Hackathon 2.docx Requires vs What Was Delivered

| # | Requirement (from Hackathon 2.docx) | Status | Implementation |
|---|---|---|---|
| 1 | RESTful API with CRUD + toggle | Delivered | `backend/src/api/routes/tasks.py` — 6 endpoints (GET list, GET by id, POST create, PATCH update, DELETE, POST toggle) |
| 2 | Backend JWT authentication | Delivered | `backend/src/auth/dependencies.py` — PyJWT HS256 decode with audience/issuer validation |
| 3 | User-level data isolation | Delivered | `backend/src/services/task_service.py` — all queries filtered by `owner_user_id` from JWT `sub` claim |
| 4 | SQLModel database models | Delivered | `backend/src/db/models/task.py` — Task model with owner, title, description, completion status, timestamps |
| 5 | Neon PostgreSQL connection | Delivered | `backend/src/db/database.py` — psycopg driver, auto-creates tables on startup |
| 6 | Better Auth integration | Delivered | `frontend/src/lib/auth/server.ts` — Better Auth with JWT plugin, HS256 custom signing via jose |
| 7 | Sign-in page | Delivered | `frontend/src/app/(auth)/signin/page.tsx` — glassmorphism form with email/password, error handling |
| 8 | Sign-up page | Delivered | `frontend/src/app/(auth)/signup/page.tsx` — glassmorphism form with name/email/password, validation |
| 9 | Auth guard (route protection) | Delivered | `frontend/src/middleware.ts` — redirects unauthenticated users to `/signin` |
| 10 | JWT token in API requests | Delivered | `frontend/src/lib/api/tasks.ts` — `authClient.token()` with retry, Bearer header injection |
| 11 | Frontend-backend integration | Delivered | `frontend/src/app/tasks/page.tsx` — all CRUD calls wired to backend API (not in-memory) |
| 12 | Responsive design | Delivered | Tailwind CSS v4 with `grid-cols-1 md:grid-cols-2` responsive layout |
| 13 | Tailwind CSS styling | Delivered | CSS-first Tailwind v4 config with glassmorphism design tokens in `globals.css` |
| 14 | Loading/error/empty states | Delivered | `frontend/src/components/tasks/TaskStates.tsx` — Lucide icons, retry button |
| 15 | Sign-out functionality | Delivered | `frontend/src/components/tasks/TaskLayout.tsx` — sign-out button with redirect |
| 16 | CORS configuration | Delivered | `backend/src/main.py` — CORSMiddleware with configurable origins |
| 17 | Backend tests passing | Delivered | 11 pytest tests passing (contract, integration, isolation, lifecycle) |
| 18 | Frontend tests passing | Delivered | 3 vitest tests passing |

### Tech Stack Delivered

| Layer | Technology | Version |
|---|---|---|
| Backend Runtime | Python + FastAPI | 3.13 / 0.116+ |
| Backend ORM | SQLModel | 0.0.24+ |
| Backend Auth | PyJWT (HS256) | 2.10+ |
| Backend DB Driver | psycopg | 3.3+ |
| Frontend Framework | Next.js App Router | 15.1.0 |
| Frontend UI | React | 19.0.0 |
| Frontend Styling | Tailwind CSS v4 | 4.1+ |
| Frontend Icons | Lucide React | 0.563+ |
| Authentication | Better Auth + JWT plugin | 1.4+ |
| Database | Neon Serverless PostgreSQL | — |
| Design Theme | Glassmorphism (soft/light) | — |

---

## Project Structure

```
hackathon2/
├── backend/
│   ├── src/
│   │   ├── main.py              # FastAPI app with CORS
│   │   ├── config.py            # Settings from .env
│   │   ├── api/routes/tasks.py  # 6 REST endpoints
│   │   ├── auth/dependencies.py # JWT verification
│   │   ├── db/
│   │   │   ├── database.py      # SQLModel engine
│   │   │   ├── dependencies.py  # Session injection
│   │   │   └── models/task.py   # Task model
│   │   ├── schemas/task.py      # Pydantic schemas
│   │   └── services/task_service.py # Business logic
│   ├── tests/                   # 11 pytest tests
│   └── .env                     # Backend env vars
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # Root layout + fonts
│   │   │   ├── page.tsx         # Redirect to /tasks
│   │   │   ├── globals.css      # Tailwind + design tokens
│   │   │   ├── (auth)/
│   │   │   │   ├── signin/page.tsx
│   │   │   │   └── signup/page.tsx
│   │   │   ├── tasks/page.tsx   # Main task board
│   │   │   └── api/auth/[...all]/route.ts  # Better Auth handler
│   │   ├── components/tasks/
│   │   │   ├── TaskCard.tsx     # Glass card component
│   │   │   ├── TaskLayout.tsx   # Layout + sign-out
│   │   │   └── TaskStates.tsx   # Loading/error/empty
│   │   ├── lib/
│   │   │   ├── auth/
│   │   │   │   ├── server.ts    # Better Auth config
│   │   │   │   ├── client.ts    # Auth client
│   │   │   │   └── index.ts     # Re-exports
│   │   │   └── api/tasks.ts     # API client with JWT
│   │   └── middleware.ts        # Auth guard
│   ├── tests/                   # 3 vitest tests
│   └── .env.local               # Frontend env vars
├── specs/
│   ├── 001-phase1-todo-spec/    # Phase I artifacts
│   ├── 001-phase2-kickoff/      # Phase II initial (stale)
│   └── 002-phase2-delivery/     # Phase II delivery (current)
├── CLAUDE.md                    # Agent instructions
├── AGENTS.md                    # SDD governance rules
└── README.md                    # This file
```

> Note: No root `pyproject.toml` — all Python config lives in `backend/pyproject.toml`.
```

---

## Phase I (Console App)

In-memory Python todo console with 13 passing tests. See `src/` and `tests/` directories.

```bash
uv run pytest -q    # 13 passed
```
