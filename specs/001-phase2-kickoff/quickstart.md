# Quickstart: Phase II Full-Stack Todo Web App

## Prerequisites

- Python 3.13+
- Node.js 20+
- `uv` installed
- Access to Neon Postgres and auth secrets via environment variables

## Repository Root

`D:\Haris\hackathons\hackathon2`

## Backend Setup (Python with uv)

```powershell
Set-Location D:\Haris\hackathons\hackathon2
uv sync --group dev
```

## TDD Workflow for Backend (Required)

1. Write or update failing tests first under backend test directories.
2. Confirm failing state (Red):

```powershell
uv run pytest -q
```

3. Implement minimum backend changes (Green).
4. Refactor while preserving pass state.
5. Re-run full backend tests:

```powershell
uv run pytest
```

## Frontend Setup (planned Phase II structure)

```powershell
Set-Location D:\Haris\hackathons\hackathon2\frontend
npm install
npm run dev
```

## Backend Run (planned Phase II structure)

```powershell
Set-Location D:\Haris\hackathons\hackathon2\backend
uv run fastapi dev src/main.py
```

## Acceptance Validation Checklist

- Authenticated user can create/list/detail/update/delete/toggle tasks.
- Unauthenticated task requests return `401`.
- User A cannot access/modify User B tasks.
- Desktop and mobile viewport runs complete full lifecycle actions.
- Refresh preserves persisted task state.

## Frontend UI Validation Checklist

- Typography renders as planned (`Space Grotesk` headings, `Source Sans 3` body).
- Primary action color and task-status chips follow shared design tokens.
- Desktop layout uses grid spacing consistently; mobile layout stacks cards without clipped actions.
- Load and toggle animations complete within 200ms and do not block interactions.

## Traceability Pointers

- Spec: `D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\spec.md`
- Plan: `D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\plan.md`
- Research: `D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\research.md`
- Data model: `D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\data-model.md`
- Contract: `D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\contracts\todo-api.openapi.yaml`
