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

9. Phase-scoped feature reset is mandatory:
When working on `phaseN` branch, active feature scope MUST be Phase N.
Do not continue `Plan`/`Tasks`/`Implement` from a previous phase feature folder.
Start a new Phase N feature and rerun:
`Specify -> Plan -> Tasks -> Implement`.

10. Branch-first stage detection is mandatory:
Always resolve workflow state in this order:
`current git branch -> matching specs/<feature> directory -> current SDD step`.
Do not infer the next step from artifacts alone without branch context.

11. Post-Implement transition prompt is mandatory:
After `/sp.implement` completes all scoped tasks, the agent MUST ask:
`Should we move on to the next feature/phase?`
If user confirms, the agent MUST bootstrap the next scope by creating:
- a new branch using the same naming convention (`NNN-short-name`)
- a matching `specs/NNN-short-name/` directory and `spec.md` scaffold
Then restart SDD at `Specify`.

## Required Workflow Per Feature
1. Confirm target phase and prerequisites.
2. Confirm active feature folder matches current phase scope.
If not, create/select a Phase-scoped feature first and start at `Specify`.
3. Write/update spec with:
user stories, acceptance criteria, edge cases, measurable success criteria.
4. Create/update plan with constitution checks.
5. Create/update tasks with test tasks first.
6. Implement only authorized task scope.
7. Run validations and collect evidence.

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
- Detection order to enforce each run:
1. Read current branch (`git branch --show-current`).
2. If on `NNN-*`, require `specs/NNN-*/` to exist and use it as active feature.
3. If on `phaseN`, treat as phase context only and start/continue with a Phase N
   feature at `Specify` unless a matching Phase N feature branch is already active.
4. After branch and feature are resolved, run checker scripts to determine current step.
- After `/sp.implement` completion:
1. Ask whether to proceed to next feature/phase.
2. If yes, run feature bootstrap flow (next available `NNN` number + short name).
3. Create/switch branch and create matching `specs/` folder.
4. Resume at `Specify`.
