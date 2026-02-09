# Implementation Plan: Phase II Full-Stack Todo Web App

**Branch**: `001-phase2-kickoff` | **Date**: 2026-02-08 | **Spec**: `D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\spec.md`  
**Input**: Feature specification from `D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\spec.md`

## Summary

Implement Phase II as a full-stack todo web app with Next.js frontend and FastAPI backend. The plan preserves Phase I lifecycle behavior while adding authenticated multi-user persistence (Neon Postgres), strict user isolation, and a responsive frontend with a defined UI direction for desktop and mobile task workflows.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript/Node.js 20+ (frontend)  
**Primary Dependencies**: FastAPI, SQLModel, Pydantic v2, Next.js App Router, Better Auth JWT flow  
**Storage**: Neon Serverless PostgreSQL  
**Testing**: `pytest` via `uv run pytest` for backend; scripted frontend acceptance checks for responsive lifecycle flows  
**Target Platform**: Web app (desktop + mobile browsers), Linux-hosted API/frontend deployments  
**Project Type**: web (frontend + backend split)  
**Performance Goals**: p95 API response <250ms for single-task operations at normal hackathon demo load; first meaningful task list render <2s on broadband  
**Constraints**: All task endpoints authenticated; ownership enforced per request; secrets from environment variables; no manual feature coding outside SDD artifacts  
**Scale/Scope**: Single-tenant app instance with multi-user isolation; core entities User/Task; scope limited to Phase II FR-001..FR-010  

## Frontend UI Direction

- Design language: clean editorial layout with high-contrast neutral surfaces plus a single teal accent for primary actions and status.
- Typography: `Space Grotesk` for headings and `Source Sans 3` for body text.
- Layout system: responsive 12-column desktop grid collapsing to stacked mobile cards at <=768px.
- Core screens: auth entry, task list, task detail/edit modal, and confirmation states for delete/toggle.
- Motion: short staged load-in for task items and optimistic toggle feedback; avoid decorative animation.
- Components: shared button/input/chip/card tokens in CSS variables to keep UI consistent across views.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Gate

| Principle | Status | Notes |
|---|---|---|
| Spec-Driven First | PASS | Uses approved `spec.md` and maintains `Specify -> Plan -> Tasks -> Implement`. |
| AI-Generated Implementation Only | PASS | Plan assumes implementation from approved tasks only; no manual coding path. |
| Phase-Gated Evolution | PASS | Scoped to Phase II on branch `001-phase2-kickoff` with Phase I behavior retained. |
| TDD with Pytest | PASS | Backend work requires Red-Green-Refactor with `uv run pytest`. |
| Traceability and Evidence | PASS | FR/user story mapping, validation, and evidence artifacts defined in this plan package. |
| Security and Isolation | PASS | JWT validation and per-user ownership checks required on all task routes. |
| Cloud-Native Portability | PASS (N/A for Phase II) | Kubernetes/Helm required in later phases; not a blocking Phase II requirement. |

### Post-Design Re-Check

| Principle | Status | Notes |
|---|---|---|
| Spec-Driven First | PASS | `research.md`, `data-model.md`, `contracts/`, and `quickstart.md` align to approved spec scope. |
| AI-Generated Implementation Only | PASS | Design artifacts remain implementation-agnostic and task-driven. |
| Phase-Gated Evolution | PASS | No Phase III+ concerns introduced. |
| TDD with Pytest | PASS | Test-first backend flow explicit in `quickstart.md`. |
| Traceability and Evidence | PASS | Requirements map into data model, contracts, and planned validation checklist. |
| Security and Isolation | PASS | Contract + model enforce auth and owner scoping semantics. |
| Cloud-Native Portability | PASS (N/A for Phase II) | Deferred to Phase IV/V planning artifacts. |

## Project Structure

### Documentation (this feature)

```text
D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts\
│   └── todo-api.openapi.yaml
└── tasks.md  # generated in /sp.tasks
```

### Source Code (repository root)

```text
D:\Haris\hackathons\hackathon2\
├── backend\
│   ├── src\
│   │   ├── api\
│   │   ├── auth\
│   │   ├── db\
│   │   └── schemas\
│   └── tests\
│       ├── contract\
│       ├── integration\
│       └── unit\
├── frontend\
│   ├── src\
│   │   ├── app\
│   │   ├── components\
│   │   ├── lib\
│   │   └── styles\
│   └── tests\
└── specs\
```

**Structure Decision**: Web split structure is selected to separate FastAPI and Next.js concerns while preserving explicit test ownership and contract-driven integration boundaries.

## Phase 0 Research Output

- `D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\research.md` resolves auth, ownership, persistence, routing, testing, and responsive UI direction decisions.

## Phase 1 Design Output

- Data model: `D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\data-model.md`
- API contract: `D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\contracts\todo-api.openapi.yaml`
- Quickstart and validation flow: `D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\quickstart.md`

## Complexity Tracking

No constitution violations requiring justification.
