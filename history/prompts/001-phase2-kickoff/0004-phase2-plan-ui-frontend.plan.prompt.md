---
id: 0004
title: phase2-plan-ui-frontend
stage: plan
date: 2026-02-08T00:00:00Z
surface: codex-cli
model: gpt-5-codex
feature: 001-phase2-kickoff
branch: 001-phase2-kickoff
user: user
command: /sp.plan $ARGUMENTS
labels: [phase2, plan, sdd, ui, frontend]
links:
  spec: D:\Haris\hackathons\hackathon2\specs\001-phase2-kickoff\spec.md
  ticket: n/a
  adr: n/a
  pr: n/a
files:
  - path: specs/001-phase2-kickoff/plan.md
    change: updated
  - path: specs/001-phase2-kickoff/research.md
    change: updated
  - path: specs/001-phase2-kickoff/quickstart.md
    change: updated
  - path: AGENTS.md
    change: updated-by-script
tests:
  - name: current-next-step on active branch
    command: .codex/skills/hackathon2-sdd-phase-workflow/scripts/current-next-step.ps1
    result: PASS
  - name: detect-next-step on active branch
    command: .codex/skills/hackathon2-sdd-phase-workflow/scripts/detect-next-step.ps1
    result: PASS
  - name: update agent context
    command: .specify/scripts/powershell/update-agent-context.ps1 -AgentType codex
    result: PASS
---

## Prompt

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType codex`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.
update your plan, use ui-ux-pro skill to design ui frontend.

## Response snapshot

Updated the Phase II plan package on branch `001-phase2-kickoff` by rebuilding `plan.md` after template reset, preserving constitution gates, and adding a concrete frontend UI direction (typography, color system, layout, motion, component tokens). Updated `research.md` and `quickstart.md` to make UI decisions and validation explicit, ran agent-context sync, and created this PHR record.

## Outcome

- ✅ Impact: Phase II planning artifacts are complete, traceable, and include explicit frontend design direction for responsive UI implementation.
- 🧪 Tests: Stage detection scripts and context update script succeeded; no implementation tests were run in this plan stage.
- 📁 Files: Updated plan/research/quickstart plus generated PHR under feature history.
- 🔁 Next prompts: `/sp.tasks` for `001-phase2-kickoff` to generate test-first task mapping.
- 🧠 Reflection: Plan template resets can overwrite prior content; immediate reconstruction with constitution re-check avoids drift.

## Evaluation notes (flywheel)

- Failure modes observed: `setup-plan.ps1` recopied template over existing `plan.md`, requiring full refill.
- Graders run and results (PASS/FAIL): `current-next-step` PASS; `detect-next-step` PASS; agent-context update PASS.
- Prompt variant (if applicable): phase2-plan-ui-frontend-v1
- Next experiment (smallest change to try): Add a guard script that snapshots existing `plan.md` before running setup-plan.