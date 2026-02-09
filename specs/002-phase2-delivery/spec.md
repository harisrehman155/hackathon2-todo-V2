# Feature Specification: Phase 2 Delivery — Auth, Integration & UI

**Feature ID:** 002-phase2-delivery
**Phase:** II (Web Application)
**Status:** Active
**Created:** 2026-02-09

---

## 1. Overview

Complete the Phase II web application by implementing the remaining gaps: Better Auth integration, frontend-backend wiring, Tailwind CSS with glassmorphism design system, and responsive UI. The backend is ~80% scaffolded; the frontend has component structure but uses in-memory state and placeholder auth.

## 2. User Stories

### US-001: Authenticated Sign-Up
**As** a new user, **I want** to create an account with email and password via Better Auth **so that** my tasks are persistent and private.

**Acceptance Criteria:**
- AC-001.1: Signup page renders a glassmorphism-styled form with email, password, and confirm-password fields
- AC-001.2: On successful signup, user is redirected to `/tasks`
- AC-001.3: On failure (duplicate email, weak password), user sees inline error message
- AC-001.4: Signup creates a session and JWT token via Better Auth

### US-002: Authenticated Sign-In
**As** a returning user, **I want** to sign in with my email and password **so that** I can access my tasks.

**Acceptance Criteria:**
- AC-002.1: Signin page renders a glassmorphism-styled form with email and password fields
- AC-002.2: On successful signin, user is redirected to `/tasks`
- AC-002.3: On failure (wrong credentials), user sees inline error message
- AC-002.4: Signin creates a session and JWT token via Better Auth

### US-003: Route Protection
**As** an unauthenticated visitor, **I want** to be redirected to `/signin` when accessing protected pages **so that** only authenticated users can manage tasks.

**Acceptance Criteria:**
- AC-003.1: Visiting `/tasks` without a session redirects to `/signin`
- AC-003.2: After signin, user is redirected back to the originally requested page
- AC-003.3: Auth guard runs on all protected routes (currently: `/tasks`)

### US-004: API-Connected Task Management
**As** an authenticated user, **I want** to create, view, toggle, and delete tasks through the web UI **so that** my tasks persist in the database.

**Acceptance Criteria:**
- AC-004.1: Tasks page fetches tasks from `GET /tasks` on mount
- AC-004.2: Creating a task calls `POST /tasks` and updates the list
- AC-004.3: Toggling a task calls `POST /tasks/{id}/toggle-complete`
- AC-004.4: Deleting a task calls `DELETE /tasks/{id}` and removes from list
- AC-004.5: JWT token is attached to every API request via Authorization Bearer header
- AC-004.6: Loading state is shown while API calls are in progress
- AC-004.7: Error state is shown if API calls fail
- AC-004.8: Empty state is shown when user has no tasks

### US-005: Responsive Glassmorphism UI
**As** a user on any device, **I want** a soft, light, glassmorphism-themed interface **so that** the app looks modern and is usable on mobile and desktop.

**Acceptance Criteria:**
- AC-005.1: Tailwind CSS is installed and configured
- AC-005.2: Design tokens use glassmorphism patterns (frosted glass, backdrop-blur, soft shadows)
- AC-005.3: Task cards use `bg-white/70 backdrop-blur-lg` with rounded corners
- AC-005.4: Layout is responsive: grid on desktop (>=768px), stack on mobile (<768px)
- AC-005.5: Typography uses Space Grotesk for headings, Inter/Source Sans 3 for body
- AC-005.6: All interactive elements have hover transitions (150-300ms)
- AC-005.7: SVG icons used instead of emojis (Lucide React)
- AC-005.8: Minimum touch target 44x44px on mobile

### US-006: Multi-User Data Isolation
**As** one of multiple users, **I want** to only see my own tasks **so that** my data is private.

**Acceptance Criteria:**
- AC-006.1: Backend filters tasks by `owner_user_id` from JWT `sub` claim
- AC-006.2: User A cannot see, modify, or delete User B's tasks
- AC-006.3: CORS is configured to allow frontend origin

## 3. Functional Requirements

| ID | Requirement | User Story | Priority |
|---|---|---|---|
| FR-001 | Install and configure Better Auth with JWT plugin on Next.js frontend | US-001, US-002 | P0 |
| FR-002 | Implement signup page with glassmorphism form and Better Auth client | US-001 | P0 |
| FR-003 | Implement signin page with glassmorphism form and Better Auth client | US-002 | P0 |
| FR-004 | Implement auth guard middleware redirecting unauthenticated users to `/signin` | US-003 | P0 |
| FR-005 | Attach JWT token to all API requests via Authorization Bearer header | US-004 | P0 |
| FR-006 | Wire tasks page to use `lib/api/tasks.ts` instead of in-memory useState | US-004 | P0 |
| FR-007 | Install and configure Tailwind CSS v4 with glassmorphism design tokens | US-005 | P0 |
| FR-008 | Implement responsive grid-to-stack layout for task list | US-005 | P1 |
| FR-009 | Implement loading, error, and empty states with proper UI feedback | US-004 | P1 |
| FR-010 | Verify CORS configuration allows frontend-backend communication | US-006 | P0 |
| FR-011 | Configure shared JWT secret between Better Auth and FastAPI | US-001, US-002 | P0 |
| FR-012 | Add sign-out functionality clearing session and redirecting to `/signin` | US-002 | P1 |
| FR-013 | Install Lucide React for SVG icons | US-005 | P1 |

## 4. Non-Functional Requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-001 | Page load time | < 3 seconds on 3G |
| NFR-002 | Color contrast ratio | >= 4.5:1 (WCAG AA) |
| NFR-003 | Touch target size | >= 44x44px |
| NFR-004 | API response time | < 500ms for CRUD operations |
| NFR-005 | Test coverage | Backend pytest + Frontend vitest passing |

## 5. Technical Constraints

- Better Auth handles user registration, login, session management, and JWT issuance
- FastAPI backend verifies JWT tokens using PyJWT (already scaffolded)
- Shared JWT secret must be configured via environment variables
- Database: SQLite for development, Neon PostgreSQL for production
- Frontend: Next.js 15 App Router with React 19
- Tailwind CSS v4 for styling

## 6. Out of Scope

- Password reset / email verification flows
- OAuth/social login providers
- Dark mode (light glassmorphism only for Phase II)
- Real-time updates (polling or WebSocket)
- Neon PostgreSQL production deployment (dev uses SQLite)

## 7. Dependencies

- Existing backend API routes in `backend/src/api/routes/tasks.py`
- Existing backend services in `backend/src/services/task_service.py`
- Existing backend JWT verification in `backend/src/auth/dependencies.py`
- Existing frontend API client in `frontend/src/lib/api/tasks.ts`
- Existing frontend components in `frontend/src/components/tasks/`

## 8. Success Criteria

1. User can sign up, sign in, and sign out
2. Tasks CRUD operations work through the UI (not in-memory)
3. Multi-user isolation verified
4. Responsive glassmorphism UI renders correctly on mobile and desktop
5. Backend pytest tests pass
6. Frontend vitest tests pass
