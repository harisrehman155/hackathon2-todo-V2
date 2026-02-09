# Phase II Criteria

## Objective
Evolve Phase I into a full-stack web todo app with persistent storage, authentication, and responsive UI.

## Stack
- **Backend:** FastAPI + SQLModel + PyJWT + psycopg (Neon PostgreSQL)
- **Frontend:** Next.js 15 App Router + React 19 + Tailwind CSS v4
- **Auth:** Better Auth with JWT plugin (HS256 custom sign via jose)
- **DB:** Neon Serverless PostgreSQL (SQLite fallback for tests)
- **Icons:** Lucide React (SVG only, no emojis)

## Expected Scope

### Backend
- RESTful task CRUD + toggle-complete endpoints at `/tasks`
- JWT verification via PyJWT (`backend/src/auth/dependencies.py`)
- Task ownership filtering by `owner_user_id` from JWT `sub` claim
- CORS middleware allowing frontend origin
- SQLModel auto-creates tables on startup

### Frontend
- Better Auth server config with JWT plugin and HS256 custom signing
- Better Auth client with `jwtClient()` plugin for token retrieval
- Catch-all API route at `/api/auth/[...all]`
- Auth guard middleware using `getSessionCookie` from `better-auth/cookies`
- Signin/Signup pages with glassmorphism styling
- Tasks page wired to backend API (not in-memory state)
- Loading, error, and empty states with Lucide icons
- Responsive grid-to-stack layout (`grid-cols-1 md:grid-cols-2`)

### Authentication Bridge
- Shared JWT secret: `BETTER_AUTH_SECRET` (frontend) = `JWT_SECRET` (backend)
- JWT claims: `sub` (user ID), `aud` (hackathon2), `iss` (better-auth)
- Token injected into API requests via `Authorization: Bearer` header

## Implementation Gotchas (Learned)

1. **Better Auth JWT plugin requires `jwks.remoteUrl`** even with custom `sign` function
2. **Better Auth JWT plugin requires `jwks.keyPairConfig`** (e.g. EdDSA/Ed25519)
3. **npm install needs `--legacy-peer-deps`** due to vite peer conflict from @tanstack/react-start
4. **`fastapi[standard]` must be installed** for the `fastapi` CLI command
5. **tsconfig.json needs `moduleResolution: "bundler"`** and `baseUrl`/`paths` for `@/` imports
6. **Neon backend URL uses `postgresql+psycopg://`** dialect prefix
7. **Neon frontend URL uses standard `postgresql://`** for the `pg` driver
8. **Node.js `pg` SSL warning** about sslmode is cosmetic — connections work
9. **Better Auth auto-creates tables** on first request (CLI migration optional)

## Activation Rule
Activate when Phase I is complete and branch transitions to Phase II scope.

## Minimal Gates
- Do not start implementation before Phase I done criteria
- Keep SDD order: Specify -> Plan -> Tasks -> Implement
- Require test and evidence mappings before merge
- Backend pytest tests must pass (`uv run pytest backend/tests/ -v`)
- Frontend build must succeed (`npx next build`)
- Multi-user task isolation must be verified
