# Tasks: Phase 2 Delivery

**Feature:** 002-phase2-delivery
**Phase:** II
**Created:** 2026-02-09

---

## Phase A: Foundation

### T-001: Install Tailwind CSS v4 and configure design tokens
**FR:** FR-007 | **US:** US-005 | **Priority:** P0
**Status:** [X]

**Steps:**
1. Run `npm install tailwindcss @tailwindcss/postcss` in frontend
2. Create `postcss.config.mjs` with `@tailwindcss/postcss` plugin
3. Replace `globals.css` with Tailwind directives and glassmorphism theme tokens
4. Remove `styles/tokens.css` (design tokens move into Tailwind theme)
5. Verify dev server starts without CSS errors

### T-002: Install Better Auth and Lucide React
**FR:** FR-001, FR-013 | **US:** US-001, US-002, US-005 | **Priority:** P0
**Status:** [X]

**Steps:**
1. Run `npm install better-auth lucide-react` in frontend
2. Verify packages appear in `package.json`

### T-003: Add CORS middleware to FastAPI backend
**FR:** FR-010 | **US:** US-006 | **Priority:** P0
**Status:** [X]

**Steps:**
1. Add `CORSMiddleware` to `backend/src/main.py`
2. Allow origins: `http://localhost:3000`
3. Allow methods: `GET, POST, PATCH, DELETE, OPTIONS`
4. Allow headers: `Authorization, Content-Type`
5. Allow credentials: `true`

### T-004: Create environment configuration files
**FR:** FR-011 | **US:** US-001, US-002 | **Priority:** P0
**Status:** [X]

**Steps:**
1. Create `frontend/.env.local` with `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`, `NEXT_PUBLIC_API_BASE_URL`
2. Ensure `backend/.env` or `backend/.env.example` has matching `JWT_SECRET`
3. Document env vars in spec

---

## Phase B: Authentication

### T-005: Configure Better Auth server with JWT plugin
**FR:** FR-001, FR-011 | **US:** US-001, US-002 | **Priority:** P0
**Status:** [X]
**Depends on:** T-002

**Steps:**
1. Create `frontend/src/lib/auth/server.ts` with Better Auth server config
2. Configure JWT plugin with HS256, audience=hackathon2, issuer=better-auth
3. Configure SQLite database adapter for Better Auth user storage
4. Export `auth` instance and `handlers`

### T-006: Create Better Auth API route handler
**FR:** FR-001 | **US:** US-001, US-002 | **Priority:** P0
**Status:** [X]
**Depends on:** T-005

**Steps:**
1. Create `frontend/src/app/api/auth/[...all]/route.ts`
2. Export GET and POST handlers from Better Auth

### T-007: Configure Better Auth client
**FR:** FR-001 | **US:** US-001, US-002 | **Priority:** P0
**Status:** [X]
**Depends on:** T-005

**Steps:**
1. Create `frontend/src/lib/auth/client.ts` with `createAuthClient`
2. Export `authClient` with `signIn`, `signUp`, `signOut`, `getSession`
3. Update `frontend/src/lib/auth/index.ts` to re-export client utilities

### T-008: Build signin page
**FR:** FR-003 | **US:** US-002 | **Priority:** P0
**Status:** [X]
**Depends on:** T-001, T-007

**Steps:**
1. Replace placeholder in `frontend/src/app/(auth)/signin/page.tsx`
2. Create glassmorphism-styled form with email and password fields
3. Wire form submission to `authClient.signIn.email()`
4. Handle success (redirect to `/tasks`) and error (show inline message)
5. Add link to signup page

### T-009: Build signup page
**FR:** FR-002 | **US:** US-001 | **Priority:** P0
**Status:** [X]
**Depends on:** T-001, T-007

**Steps:**
1. Replace placeholder in `frontend/src/app/(auth)/signup/page.tsx`
2. Create glassmorphism-styled form with name, email, password fields
3. Wire form submission to `authClient.signUp.email()`
4. Handle success (redirect to `/tasks`) and error (show inline message)
5. Add link to signin page

### T-010: Implement auth guard via Next.js middleware
**FR:** FR-004 | **US:** US-003 | **Priority:** P0
**Status:** [X]
**Depends on:** T-005

**Steps:**
1. Create `frontend/src/middleware.ts`
2. Check for Better Auth session cookie
3. Redirect to `/signin` if no valid session on protected routes (`/tasks`)
4. Allow public routes: `/`, `/signin`, `/signup`, `/api/auth/*`

### T-011: Add JWT token to API client
**FR:** FR-005 | **US:** US-004 | **Priority:** P0
**Status:** [X]
**Depends on:** T-007

**Steps:**
1. Modify `frontend/src/lib/api/tasks.ts` `request()` function
2. Accept optional token parameter
3. Add `Authorization: Bearer ${token}` header when token is provided
4. Create helper to get token from Better Auth session

### T-012: Add sign-out to task layout
**FR:** FR-012 | **US:** US-002 | **Priority:** P1
**Status:** [X]
**Depends on:** T-007

**Steps:**
1. Update `TaskLayout` to accept and display user info
2. Add sign-out button that calls `authClient.signOut()`
3. Redirect to `/signin` after sign-out

---

## Phase C: Frontend-Backend Integration

### T-013: Wire tasks page to API
**FR:** FR-006 | **US:** US-004 | **Priority:** P0
**Status:** [X]
**Depends on:** T-011

**Steps:**
1. Replace `useState<TaskItem[]>([])` with API-backed state
2. Fetch tasks on mount using `listTasks()` with JWT token
3. Create task via `createTask()` API call
4. Toggle task via `toggleTask()` API call
5. Delete task via `deleteTask()` API call
6. Refresh task list after mutations

### T-014: Implement loading, error, and empty states
**FR:** FR-009 | **US:** US-004 | **Priority:** P1
**Status:** [X]
**Depends on:** T-013

**Steps:**
1. Show loading skeleton/spinner while fetching tasks
2. Show error message if API call fails with retry option
3. Show empty state illustration when no tasks exist
4. Use `TaskStates` component for state display

---

## Phase D: Glassmorphism UI & Responsive Design

### T-015: Apply glassmorphism to task layout and cards
**FR:** FR-007, FR-008 | **US:** US-005 | **Priority:** P0
**Status:** [X]
**Depends on:** T-001

**Steps:**
1. Update `TaskLayout` with glassmorphism container classes
2. Update `TaskCard` with glass card classes: `bg-white/70 backdrop-blur-lg rounded-xl border border-white/20 shadow-lg shadow-black/5`
3. Style form with glass effect
4. Apply responsive grid/stack: `grid grid-cols-1 md:grid-cols-2 gap-4`
5. Style buttons with teal accent and hover transitions
6. Add Lucide icons to buttons (Plus, Check, Trash2, LogOut)

### T-016: Style auth pages with glassmorphism
**FR:** FR-007 | **US:** US-005 | **Priority:** P1
**Status:** [X]
**Depends on:** T-001, T-008, T-009

**Steps:**
1. Center auth form on page with glassmorphism card
2. Style inputs with glass borders and focus states
3. Style submit button with teal accent
4. Add subtle background gradient
5. Ensure mobile-responsive layout

### T-017: Update home page and layout
**FR:** FR-007 | **US:** US-005 | **Priority:** P1
**Status:** [X]
**Depends on:** T-001

**Steps:**
1. Update root layout with font imports (Space Grotesk, Source Sans 3)
2. Update home page to redirect to `/tasks` or show landing
3. Apply glassmorphism background gradient to body

---

## Phase E: Verification

### T-018: Run backend tests
**FR:** All | **US:** All | **Priority:** P0
**Status:** [X]
**Depends on:** T-003

**Steps:**
1. Run `cd /mnt/d/Haris/hackathons/hackathon2 && uv run pytest backend/tests/ -v`
2. All tests must pass
3. Fix any failures

### T-019: Verify E2E flow manually
**FR:** All | **US:** All | **Priority:** P0
**Status:** [X]
**Depends on:** T-013, T-015

**Steps:**
1. Start backend: `uv run fastapi dev backend/src/main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Test signup → signin → create/toggle/delete tasks → signout
4. Verify responsive layout on mobile and desktop viewports
