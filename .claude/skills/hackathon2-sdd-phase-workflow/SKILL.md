---
name: hackathon2-sdd-phase-workflow
description: Enforce Hackathon 2 spec-driven delivery for Codex and Claude across Phases I-V. Use when planning, specifying, tasking, implementing, reviewing, or gating work in this project, especially when validating `Specify -> Plan -> Tasks -> Implement`, phase-branch rules, and uv+pytest TDD evidence.
---

# Hackathon2 SDD Phase Workflow

## Before Implementation

Gather project context before taking any action:

- Read `.specify/memory/constitution.md`.
- Read active feature spec/plan/tasks under `specs/<feature>/`.
- Read `AGENTS.md` and `CLAUDE.md`.
- Confirm current git branch and intended target branch.
- Confirm current phase from branch context and feature scope.
- Apply branch-first detection order:
  1) detect current git branch,
  2) resolve matching `specs/<feature>/` directory,
  3) then evaluate current SDD step.
- Run `scripts/current-next-step.ps1` at invocation start.
- Run `scripts/detect-next-step.ps1` before giving stage advice.
- Run `scripts/check-phase-complete.ps1` when evaluating phase transition readiness.
- Confirm `uv` is available and use `uv` for Python environment/dependency/test execution.

## Branch-First State Detection (Mandatory)

Resolve workflow state in this exact sequence:

1. Detect current branch with `git branch --show-current`.
2. Branch classification:
- `phaseN`: phase context only; no feature-stage continuation unless a Phase N feature is explicitly active.
- `NNN-short-name`: feature context; expected active feature is exactly that branch name.
3. Resolve feature directory under `specs/`:
- For feature branch `NNN-short-name`, require `specs/NNN-short-name/`.
- If missing, block and require `/sp.specify` (or feature scaffold creation) before stage guidance.
- For `phaseN` branch, do not reuse previous-phase feature directories as active scope.
4. After branch + feature resolution, run:
- `scripts/current-next-step.ps1`
- `scripts/detect-next-step.ps1`
5. Use checker output only after steps 1-4 pass.

## Python Tooling Baseline (Mandatory)

For Python scope in this repository:

- Use `uv` only for environment and dependency management.
- Do not use `pip`, `python -m pip`, or direct `venv` setup commands.
- Use `uv sync` for project dependency sync.
- Use `uv add <package>` for dependency changes.
- Use `uv run pytest` for all test execution evidence.

## Hard-Stop Gates (Mandatory)

Do not proceed to a later stage if any required artifact is missing.

1. Branch gate:
- Require active phase branch context (`phase1`, `phase2`, `phase3`, `phase4`, `phase5`) or an approved feature branch (`NNN-short-name`) cut from the active phase branch.
- Block if branch context is missing or inconsistent with requested phase.

2. SDD order gate:
- `Specify` must exist before `Plan`.
- `Plan` must exist before `Tasks`.
- `Tasks` must exist before `Implement`.
- Block and return the exact missing artifact if violated.

3. Artifact gate:
- Require spec file for requested feature.
- Require plan file for requested implementation.
- Require tasks file that maps to user stories.
- Block implementation when mappings are absent.

4. Phase scope gate:
- Block any Phase N+1 implementation while Phase N completion criteria are unmet.
- Block direct phase skipping.
- On `phaseN` branch, block reuse of prior-phase feature artifacts as active scope.
- If active feature naming/content maps to earlier phase, require new Phase N feature and restart at `Specify`.

## Deterministic Checkers (Required)

Use these scripts before guidance:

1. `scripts/current-next-step.ps1`
- Purpose: provide current step completion state, next step, and mapped command.
- Output: JSON only with `current_step`, `current_step_done`, `next_step`,
  `next_command`, `can_proceed`, `reason`, and `message`.

1. `scripts/detect-next-step.ps1`
- Purpose: detect the next valid SDD stage from branch and artifact state.
- Output: JSON only with `phase`, `branch_type`, `active_feature`,
  `detected_step`, `missing_artifacts`, `reason`, `can_proceed`.

2. `scripts/check-phase-complete.ps1`
- Purpose: evaluate strict phase completion status and gate-by-gate results.
- Output: JSON only with `phase`, `status`, `gates`, `missing_items`,
  `recommendation`.

Do not provide stage recommendations until these checks are run.

## Invocation Behavior (Required)

When this skill is invoked:

1. Detect current branch and classify branch type (`phaseN` or `NNN-short-name`).
2. Resolve feature directory alignment in `specs/` from branch context.
3. Run `scripts/current-next-step.ps1`.
4. Validate phase-scoped feature alignment:
- If current branch is `phaseN`, active feature must be a Phase N feature.
- If misaligned (for example `phase2` with `phase1` feature), treat workflow as reset state.
- Force next action to `Specify` for a new/current Phase N feature scope.
5. Tell the user:
- `Current step is: <current_step> (done: <true|false>)`
- `Next step is: <next_step>`
6. Ask:
- `Do you want to enhance the current step or move to the next step?`
7. If user chooses next step and `next_command` exists:
- Execute the mapped command directly:
  - `Specify` -> `/sp.specify`
  - `Plan` -> `/sp.plan`
  - `Tasks` -> `/sp.tasks`
  - `Implement` -> `/sp.implement`
8. If user chooses enhancement:
- stay in current step and apply requested refinements.
9. If checker returns blocked:
- return failed gate details and do not run any `sp.*` command.
10. After successful `/sp.implement` completion:
- Ask: `Should we move on to the next feature/phase?`
- If user says `yes`, bootstrap next scope using the same feature naming convention:
  - compute next available `NNN` for chosen short name,
  - create/switch to `NNN-short-name`,
  - create matching `specs/NNN-short-name/` with `spec.md`,
  - restart at `/sp.specify`.
- If user says `no`, remain on current branch and report completion evidence only.

## Branching Strategy Enforcement

Follow these branch rules exactly:

- Keep one active phase branch at a time (`phase1` -> `phase5` lifecycle).
- Create feature branches as `NNN-short-name` from active phase branch.
- Merge feature branches back into the active phase branch.
- Do not target unrelated branches for feature merges.
- Open next phase branch only after current phase done criteria are met.
- For Phase N execution, feature naming should include phase scope (example: `NNN-phaseN-short-name`) to preserve deterministic gating.

For concrete checks, read `references/branching-strategy.md`.

## Phase Workflow

### Global flow

1. Specify
- Build or update `specs/<feature>/spec.md` from project requirements.
- Ensure user stories, acceptance scenarios, edge cases, assumptions, and measurable success criteria.
- Create/update `specs/<feature>/checklists/requirements.md` and validate.

2. Plan
- Produce `specs/<feature>/plan.md`.
- Enforce constitution checks and phase constraints.
- Declare testing and evidence strategy.

3. Tasks
- Produce `specs/<feature>/tasks.md` with explicit story mapping.
- Require validation tasks per story.
- Require Python test tasks with `pytest` before implementation tasks, executed via `uv run pytest`.

4. Implement
- Execute only approved tasks.
- Preserve traceability from requirement -> task -> validation evidence.

### Phase-specific references

- Phase I detailed criteria: `references/phase-1.md`
- Phase II scaffold criteria: `references/phase-2.md`
- Phase III scaffold criteria: `references/phase-3.md`
- Phase IV scaffold criteria: `references/phase-4.md`
- Phase V scaffold criteria: `references/phase-5.md`

## Test-Driven Development Policy

For Python scope:

- Use Red-Green-Refactor.
- Write tests first using `pytest`.
- Confirm tests fail before writing implementation changes.
- Confirm tests pass before merge.
- Block merge when relevant tests are missing or failing.
- Execute all Python test commands as `uv run pytest ...`.

Use `references/spec-quality-gates.md` for acceptance and evidence checks.

## Evidence and Traceability Policy

Require all of the following:

- Requirements map to tasks.
- Tasks map to validation evidence.
- Story-level acceptance checks are recorded.
- Phase submission evidence is prepared for completed scope.

If any mapping is missing, block implementation and return a remediation list.

## Docx Source Rules (Optional Integration)

Use `references/docx-source-rules.md` when requirements are updated from `Hackathon 2.docx`.

Rules:

- Extract requirements first, then update specs.
- Prefer stable requirement statements over narrative text.
- Capture conflicts and mark them for explicit resolution.

## Skill Integrations

Use optional local skills only when relevant:

1. `skill-validator` integration
- Use to audit this skill quality and enforce structural checks.
- Use after major skill edits or before sharing.

2. `docx` integration
- Use only when reading or reconciling requirement changes from `.docx` sources.
- Do not depend on it for normal phase execution.

No other skill imports are required by default.

## Reusable Intelligence Rule (Mandatory)

When execution reveals a durable, reusable project rule or workflow
improvement:

- Update `AGENTS.md` and this skill in the same change.
- Keep the new rule explicit and testable.
- Apply the updated rule immediately in the active workflow.
- Phase-scoped reset rule: when branch phase changes, start a new feature lifecycle at `Specify` for that phase instead of continuing previous-phase feature artifacts.
- Branch-first rule: always derive active feature from current branch before checking artifact stage.

## Required Responses on Gate Failure

When blocked, respond with:

- What gate failed.
- Why it failed.
- Exact files/branches missing or invalid.
- Minimal next actions to unblock.

## Output Contract for Successful Progress

For every completed stage, return:

- Stage completed (`Specify`, `Plan`, `Tasks`, or `Implement`).
- Files created/updated.
- Validation summary.
- Remaining blockers, if any.

For `Implement` completion specifically, also return:
- `Transition prompt shown: yes`
- `User decision: next feature/phase | stay`
- If transitioned: new branch name and new spec path.

When phase completion check returns `status = complete`, return exactly:

1. `Phase 1 completion status: PASS`
2. `Choose next action:`
- `A) Test workflow yourself now (recommended first)`
- `B) Proceed to Phase 2 transition prep`

If user selects `A`, provide self-test checklist and commands from
`references/workflow-test-checklist.md`.
If user selects `B`, provide phase transition checklist:
1. Confirm all Phase 1 gates locked.
2. Create/switch to `phase2`.
3. Start first Phase 2 feature branch `NNN-*`.
4. Begin with `/sp.specify` on Phase 2 scope.

## Validation Scenarios

Use these scenario checks after skill updates.

| Prompt | Expected Behavior |
|---|---|
| implement phase 2 feature directly | Block with phase scope gate when Phase I is incomplete. |
| create tasks without plan | Block with SDD order gate and require `plan.md`. |
| start phase3 while still in phase1 | Block with phase transition gate. |
| create Phase I spec from docs | Allow Specify stage and require checklist validation. |
| plan from approved spec | Allow Plan stage and enforce constitution checks. |
| implement from tasks | Allow only when tasks exist and `uv run pytest` TDD evidence is enforced. |

## Quick Trigger Examples

- "Use $hackathon2-sdd-phase-workflow to create Phase I spec from docs."
- "Use $hackathon2-sdd-phase-workflow to gate this plan against constitution."
- "Use $hackathon2-sdd-phase-workflow to block implementation until tasks exist."

## Anti-Patterns to Reject

- Implementing features without spec/plan/tasks.
- Phase skipping.
- Feature branches not cut from active phase branch.
- Using `pip`/direct `venv` for project Python workflow instead of `uv`.
- Merging with failing or missing `uv run pytest` evidence.
- Producing non-traceable changes.
- Ending workflow after `Implement` without asking about next feature/phase transition.
