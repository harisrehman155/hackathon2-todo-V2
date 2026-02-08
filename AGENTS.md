# AGENTS.md

## Purpose
This project uses Spec-Driven Development for Hackathon 2.
All agent work MUST follow:
`Specify -> Plan -> Tasks -> Implement`

No feature implementation starts without an approved spec and task mapping.

## Source of Truth
1. `.specify/memory/constitution.md`
2. Current feature spec files under `/specs/`
3. Plan and task artifacts generated from specs

If conflicts exist, follow the order above.

## Non-Negotiable Rules
1. No manual feature coding:
Implementation for scoped features MUST be AI-generated from approved specs/tasks.
If output is wrong, refine spec/plan/tasks and regenerate.

2. Phase order is mandatory:
Work progresses in this order only:
Phase I -> Phase II -> Phase III -> Phase IV -> Phase V

3. TDD with `pytest` is required for Python scope:
Use Red-Green-Refactor.
Write tests first, confirm failing state, implement, then pass tests.

4. `uv` is mandatory for Python environment and package management:
Do not use `pip`/`venv` directly for project setup or dependency install.
Use `uv` commands (`uv sync`, `uv add`, `uv run pytest`) in docs and execution.

5. Traceability is required:
Every task MUST reference user story/requirements.
Every requirement MUST have at least one validation method.

6. Security baseline:
Authenticated APIs MUST enforce user-level data isolation.
JWT validation and secret handling MUST be explicit in implementation plans.

7. Cloud-native portability:
For distributed concerns, prefer config-driven infrastructure abstraction.
Phase IV-V artifacts MUST include Kubernetes and Helm assets.

8. Reusable intelligence update loop:
When a durable, reusable workflow improvement is discovered, update both
`AGENTS.md` and the relevant skill file(s) in the same change so future runs
inherit the improvement.

## Required Workflow Per Feature
1. Confirm target phase and prerequisites.
2. Write/update spec with:
user stories, acceptance criteria, edge cases, measurable success criteria.
3. Create/update plan with constitution checks.
4. Create/update tasks with test tasks first.
5. Implement only authorized task scope.
6. Run validations and collect evidence.

## Definition of Done
A feature/change is done only when all are true:
- Constitution checks pass.
- `pytest` tests exist and pass for Python changes (run via `uv run pytest`).
- Spec -> tasks -> code traceability is explicit.
- Required evidence artifacts are updated (docs/demo/deploy links as applicable).

## Operational Notes for Codex
- Prefer minimal, reviewable increments.
- Keep changes within current phase scope unless a spec amendment is approved.
- Do not silently bypass failed tests or missing requirements.
- If required context is missing, stop implementation and request spec updates.
- If a new useful pattern/rule is found during execution, persist it by updating
  this file and the applicable skill instructions immediately.
