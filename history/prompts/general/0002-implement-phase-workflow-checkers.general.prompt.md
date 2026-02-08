---
id: 0002
title: implement-phase-workflow-checkers
stage: general
date: 2026-02-08
surface: codex-cli
model: gpt-5-codex
feature: none
branch: 001-phase1-todo-spec
user: Haris Rehman
command: implement skill checker plan
labels: [skill, phase-gates, sdd, powershell]
links:
  spec: n/a
  ticket: n/a
  adr: n/a
  pr: n/a
files:
  - path: .codex/skills/hackathon2-sdd-phase-workflow/SKILL.md
    change: updated
  - path: .codex/skills/hackathon2-sdd-phase-workflow/references/phase-1.md
    change: updated
  - path: .codex/skills/hackathon2-sdd-phase-workflow/references/spec-quality-gates.md
    change: updated
  - path: .codex/skills/hackathon2-sdd-phase-workflow/references/branching-strategy.md
    change: updated
  - path: .codex/skills/hackathon2-sdd-phase-workflow/references/workflow-test-checklist.md
    change: created
  - path: .codex/skills/hackathon2-sdd-phase-workflow/scripts/detect-next-step.ps1
    change: created
  - path: .codex/skills/hackathon2-sdd-phase-workflow/scripts/check-phase-complete.ps1
    change: created
tests:
  - name: detect-next-step on current repo
    result: PASS
  - name: check-phase-complete on current repo
    result: PASS
  - name: detect-next-step scenario matrix in temp repo
    result: PASS
  - name: check-phase-complete full-pass scenario in temp repo
    result: PASS
---

## Prompt

```text
PLEASE IMPLEMENT THIS PLAN:
Plan: Phase-Step Detection and Phase-Completion Handoff for `hackathon2-sdd-phase-workflow`.
Implement deterministic phase-step detection and strict phase-completion gating with two-option handoff:
A) Test workflow yourself now
B) Proceed to Phase 2 transition prep
Add scripts detect-next-step.ps1 and check-phase-complete.ps1 and update skill references/contracts.
```

## Response snapshot

Implemented deterministic checkers inside the skill, updated SKILL and references with required JSON contracts and handoff policy, added workflow self-test checklist, and validated outputs on real and synthetic repositories.

## Outcome

- ✅ Impact: Skill can now deterministically detect next SDD stage and strict Phase 1 completion.
- 🧪 Tests: Scenario checks for Plan/Tasks/Implement/Blocked/Complete all passed.
- 📁 Files: 7 skill files changed or added.
- 🔁 Next prompts: invoke checker scripts before advice in every phase discussion.
- 🧠 Reflection: Scripted gating removes ambiguity and supports consistent branch/phase transitions.

## Evaluation notes (flywheel)

- Failure modes observed: none in checker logic tests.
- Graders run and results (PASS/FAIL): PASS.
- Prompt variant (if applicable): phase-gate-checker-v1.
- Next experiment (smallest change to try): add optional phase2-complete checker contract once phase2 starts.
