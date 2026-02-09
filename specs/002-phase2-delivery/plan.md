# Implementation Plan: Phase 2 Delivery

**Feature:** 002-phase2-delivery
**Phase:** II
**Created:** 2026-02-09

---

## 1. Technical Architecture

### Authentication Bridge: Better Auth + FastAPI JWT

Better Auth runs as a Next.js API route handler (`/api/auth/[...all]`). It manages user registration, login, and session storage. The JWT plugin issues JWTs that the frontend sends as Bearer tokens to the FastAPI backend.

**Flow:**
1. User submits credentials to Better Auth via Next.js API route
2. Better Auth validates and creates a session + JWT
3. Frontend stores session (cookie-based via Better Auth)
4. Frontend reads JWT from Better Auth session and attaches it to API requests
5. FastAPI validates JWT using shared secret (already implemented in `backend/src/auth/dependencies.py`)

**JWT Configuration:**
- Algorithm: HS256
- Secret: shared via `BETTER_AUTH_SECRET` / `JWT_SECRET` env vars
- Audience: `hackathon2`
- Issuer: `better-auth`
- Subject claim (`sub`): user ID

### Frontend Integration Architecture

```
AuthProvider (context)
  └─> Session state (user, token)
       ├─> Auth Guard (middleware.ts) — redirects to /signin if no session
       ├─> API Client (lib/api/tasks.ts) — injects Bearer token
       └─> UI Components — consume session for display
```

### Styling Strategy: Tailwind CSS v4

Tailwind CSS v4 uses CSS-first configuration. Design tokens defined in `globals.css` using `@theme`.

**Design Token System:**
- Glass background: `bg-white/70` with `backdrop-blur-lg`
- Border: `border-white/20`
- Shadow: `shadow-lg shadow-black/5`
- Radius: `rounded-xl` to `rounded-2xl`
- Primary: teal `#0f9d8a`
- Font heading: Space Grotesk
- Font body: Source Sans 3

## 2. Implementation Phases

### Phase A: Foundation (packages & config)
1. Install Tailwind CSS v4 in frontend
2. Install Better Auth + `@better-auth/jwt` in frontend
3. Install Lucide React for SVG icons
4. Configure Tailwind CSS with design tokens in globals.css
5. Add CORS middleware to FastAPI backend
6. Create `.env.local` with shared secrets

### Phase B: Authentication
7. Configure Better Auth server (`lib/auth/server.ts`) with JWT plugin
8. Create Better Auth API route handler (`app/api/auth/[...all]/route.ts`)
9. Configure Better Auth client (`lib/auth/client.ts`)
10. Build signin page with glassmorphism form
11. Build signup page with glassmorphism form
12. Implement auth guard via Next.js middleware
13. Add sign-out button to task layout
14. Update API client to inject JWT from session

### Phase C: Frontend-Backend Integration
15. Refactor tasks page to fetch from API on mount
16. Wire create task form to API
17. Wire toggle and delete actions to API
18. Add loading skeleton during fetch
19. Add error display on API failure
20. Add empty state when no tasks

### Phase D: Glassmorphism UI
21. Style task layout with glassmorphism containers
22. Style task cards with glass effect
23. Style auth pages consistently
24. Style form inputs with glass borders
25. Apply responsive grid/stack layout
26. Add Lucide icons to buttons and status chips
27. Ensure hover/focus transitions

## 3. Constitution Alignment

| Principle | How Addressed |
|---|---|
| I. Spec-Driven Development | spec.md → plan.md → tasks.md → implement |
| II. AI-Generated Implementation | All code generated from approved tasks |
| III. Phase-Gated Delivery | Phase II scope only — no Phase III features |
| IV. TDD with Pytest | Backend tests verified; frontend tests with vitest |
| V. End-to-End Traceability | Each task traces to FR → US |
| VI. Security & Multi-User Isolation | JWT auth + owner_user_id filtering |
| VII. Cloud-Native Portability | Config-driven (env vars for DB, secrets) |

## 4. Risk Mitigation

| Risk | Mitigation |
|---|---|
| Better Auth JWT format incompatible with PyJWT | Configure Better Auth JWT plugin with matching algorithm, audience, issuer |
| CORS blocks frontend-backend communication | Add CORSMiddleware to FastAPI with explicit origin allowlist |
| Tailwind v4 breaking changes | Use CSS-first config approach (no tailwind.config.ts needed) |
| Session management complexity | Use Better Auth's built-in cookie-based sessions |

## 5. Files to Create

| File | Purpose |
|---|---|
| `frontend/src/lib/auth/server.ts` | Better Auth server configuration |
| `frontend/src/lib/auth/client.ts` | Better Auth client for browser |
| `frontend/src/app/api/auth/[...all]/route.ts` | Better Auth API route handler |
| `frontend/src/middleware.ts` | Next.js middleware for auth guard |
| `frontend/.env.local` | Environment variables |

## 6. Files to Modify

| File | Changes |
|---|---|
| `frontend/package.json` | Add better-auth, tailwindcss, @tailwindcss/postcss, lucide-react |
| `frontend/src/app/globals.css` | Tailwind directives + design tokens |
| `frontend/src/app/layout.tsx` | Add font imports, auth provider |
| `frontend/src/app/(auth)/signin/page.tsx` | Real signin form |
| `frontend/src/app/(auth)/signup/page.tsx` | Real signup form |
| `frontend/src/app/tasks/page.tsx` | Replace in-memory state with API calls |
| `frontend/src/lib/api/tasks.ts` | Add Authorization header |
| `frontend/src/lib/auth/index.ts` | Re-export auth utilities |
| `frontend/src/lib/auth/guard.ts` | Remove — replaced by middleware.ts |
| `frontend/src/components/tasks/TaskCard.tsx` | Tailwind glassmorphism classes |
| `frontend/src/components/tasks/TaskLayout.tsx` | Tailwind responsive + sign-out |
| `frontend/src/components/tasks/TaskStates.tsx` | Tailwind styling |
| `frontend/src/styles/tokens.css` | Remove — replaced by Tailwind theme |
| `backend/src/main.py` | Add CORSMiddleware |
| `backend/.env` | Ensure JWT_SECRET matches |
