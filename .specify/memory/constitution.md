<!--
Sync Impact Report
- Version change: template reset by init -> 1.1.0
- Modified principles:
  - Template Principle 1 -> I. Spec-Driven Development First
  - Template Principle 2 -> II. AI-Generated Implementation Only (No Manual Coding)
  - Template Principle 3 -> III. Phase-Gated Evolution Delivery
  - Template Principle 4 -> IV. Test-Driven Development with Pytest
  - Template Principle 5 -> V. End-to-End Traceability and Evidence
  - Template Principle 6 -> VI. Security and Multi-User Data Isolation
  - Added explicit VII. Cloud-Native Portability by Design
- Added sections:
  - Mandatory Stack and Deliverables
  - Development Workflow and Quality Gates
- Removed sections:
  - None
- Templates requiring updates:
  - ✅ updated `.specify/templates/plan-template.md`
  - ✅ updated `.specify/templates/spec-template.md`
  - ✅ updated `.specify/templates/tasks-template.md`
  - ⚠ pending `.specify/templates/commands/*.md` (directory not present in repository)
- Follow-up TODOs:
  - None
-->

# Hackathon 2 Todo Constitution

## Core Principles

### I. Spec-Driven Development First
Every change MUST begin with an approved specification before implementation starts.
Work MUST follow the sequence `Specify -> Plan -> Tasks -> Implement`, and each
specification MUST include user stories, acceptance scenarios, edge cases, and
measurable success criteria.
Rationale: Prevents scope drift and enforces consistent decision quality.

### II. AI-Generated Implementation Only (No Manual Coding)
Production code for scoped features MUST be generated through the approved AI workflow
(Claude Code with Spec-Kit Plus). Contributors MUST refine the specification or tasks
when output is incorrect instead of bypassing the process with manual feature coding.
Rationale: This hackathon evaluates specification quality and agentic execution,
not ad-hoc coding speed.

### III. Phase-Gated Evolution Delivery
Implementation MUST follow the five project phases in order:
1. In-memory Python console app.
2. Full-stack web app (Next.js + FastAPI + SQLModel + Neon + Better Auth).
3. AI chatbot (OpenAI ChatKit + Agents SDK + MCP SDK).
4. Local Kubernetes deployment (Docker + Minikube + Helm + kubectl-ai/kagent).
5. Advanced cloud deployment with event-driven architecture (Kafka + Dapr + DOKS).
A phase is complete only when its deliverables are demonstrable and documented.
Rationale: Later phases depend on verified behavior and artifacts from earlier phases.

### IV. Test-Driven Development with Pytest
All Python backend and service logic MUST follow Red-Green-Refactor with `pytest` as
the default framework. For each user story, tests MUST be written first, MUST fail
before implementation, and MUST pass before merge or phase sign-off. When behavior is
changed, corresponding tests MUST be updated in the same change.
Rationale: TDD with `pytest` provides fast, reproducible quality checks and guards
against regressions across phase evolution.

### V. End-to-End Traceability and Evidence
All implementation tasks MUST map back to specification requirements, and all
requirements MUST map to tests or acceptance checks. Each phase submission MUST include
required evidence: public repository, deployment links when applicable, and a demo video
not exceeding 90 seconds.
Rationale: Traceability ensures reviewability and defensible scoring.

### VI. Security and Multi-User Data Isolation
All authenticated APIs MUST enforce user-level data isolation and ownership checks.
JWT-based authentication MUST be validated server-side for protected routes, and secrets
MUST be managed through environment variables or approved secret stores.
Rationale: Multi-user todo behavior and cloud deployments are invalid without tenant
isolation and basic secret hygiene.

### VII. Cloud-Native Portability by Design
Distributed concerns (pub/sub, state, secrets, invocation, scheduling) SHOULD be
abstracted through portable interfaces (for example Dapr components) so infrastructure
swaps are config-first, not code-first. Kubernetes manifests and Helm charts MUST be
versioned with the application.
Rationale: Portability and operability are explicit learning goals for Phases IV and V.

## Mandatory Stack and Deliverables

The project baseline MUST use the stack and outputs defined by the hackathon brief.

- Runtime and backend baseline: Python 3.13+, FastAPI, SQLModel.
- Frontend baseline: Next.js App Router.
- Persistence baseline: Neon Serverless PostgreSQL.
- Auth baseline: Better Auth with JWT verification in backend.
- AI baseline (Phases III-V): OpenAI ChatKit, OpenAI Agents SDK, official MCP SDK.
- Cloud baseline (Phases IV-V): Docker, Minikube, Helm, Kubernetes, DigitalOcean DOKS.
- Event-driven baseline (Phase V): Kafka and Dapr.

Required repository artifacts for each phase:

- `README.md` with setup and run instructions.
- `CLAUDE.md` with agent workflow guidance.
- Constitution and spec history under `.specify/`.
- Source code and deployment configuration for completed phase scope.

## Development Workflow and Quality Gates

Every feature and phase MUST pass the following gates:

1. Constitution Gate: plan explicitly confirms compliance with all principles.
2. Specification Gate: spec includes testable user stories and measurable outcomes.
3. TDD Gate: `pytest` test cases are defined before implementation and run in CI/local
   verification for each user story affecting Python code.
4. Task Gate: tasks are traceable to stories and include validation steps.
5. Validation Gate: at least one automated or scripted verification per user story,
   plus phase-level acceptance checks.
6. Evidence Gate: submission artifacts are present and reproducible.

Implementation and review expectations:

- Pull requests or review notes MUST cite relevant spec sections.
- Deviations from scope or stack MUST be documented in plan complexity tracking.
- Missing acceptance evidence blocks phase completion.

## Governance

This constitution overrides conflicting local conventions for this repository.

Amendment process:

1. Propose change with rationale and affected principles/sections.
2. Classify version bump using semantic policy below.
3. Update dependent templates and guidance docs in the same change.
4. Record sync impact in the constitution header comment.

Versioning policy:

- MAJOR: incompatible governance changes or principle removals/redefinitions.
- MINOR: new principle or materially expanded mandatory guidance.
- PATCH: wording clarifications, typo fixes, or non-semantic refinements.

Compliance review expectations:

- Every plan MUST include a Constitution Check with pass/fail gates.
- Every task list MUST preserve requirement-to-task traceability.
- Periodic audits MUST verify submissions still match phase scope and evidence rules.

**Version**: 1.1.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08
