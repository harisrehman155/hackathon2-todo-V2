---
id: 0001
title: create-hackathon2-workflow-skill
stage: general
date: 2026-02-08
surface: codex-cli
model: gpt-5-codex
feature: none
branch: 001-phase1-todo-spec
user: Haris Rehman
command: implement project skill plan
labels: [skill, workflow, governance, hackathon2]
links:
  spec: n/a
  ticket: n/a
  adr: n/a
  pr: n/a
files:
  - path: hackathon2-sdd-phase-workflow/SKILL.md
    change: created
  - path: hackathon2-sdd-phase-workflow/agents/openai.yaml
    change: created
  - path: hackathon2-sdd-phase-workflow/references/phase-1.md
    change: created
  - path: hackathon2-sdd-phase-workflow/references/phase-2.md
    change: created
  - path: hackathon2-sdd-phase-workflow/references/phase-3.md
    change: created
  - path: hackathon2-sdd-phase-workflow/references/phase-4.md
    change: created
  - path: hackathon2-sdd-phase-workflow/references/phase-5.md
    change: created
  - path: hackathon2-sdd-phase-workflow/references/branching-strategy.md
    change: created
  - path: hackathon2-sdd-phase-workflow/references/spec-quality-gates.md
    change: created
  - path: hackathon2-sdd-phase-workflow/references/docx-source-rules.md
    change: created
tests:
  - name: Required file presence checks
    result: PASS
  - name: Frontmatter regex validation
    result: PASS
  - name: Scenario phrase checks
    result: PASS
---

## Prompt

```text
PLEASE IMPLEMENT THIS PLAN:
Create one repo-local skill that standardizes how Codex/Claude work on this project using strict gates:
Specify -> Plan -> Tasks -> Implement, phase-by-phase branching, and pytest TDD enforcement.
Include all phases (I-V) with Phase I concrete and II-V scaffolded, with optional skill-validator + docx guidance.
```

## Response snapshot

Implemented repo-local skill `hackathon2-sdd-phase-workflow` with strict hard-stop gates,
phase/branch enforcement, pytest TDD policy, traceability requirements, and phase references.
Added agent metadata and reference files for branching, quality gates, and docx source handling.
Executed structural and scenario validations.

## Outcome

- ✅ Impact: Project now has a reusable governance skill for Codex/Claude workflows.
- 🧪 Tests: File presence, frontmatter, and scenario checks passed.
- 📁 Files: 10 files created in `hackathon2-sdd-phase-workflow/`.
- 🔁 Next prompts: Use `$hackathon2-sdd-phase-workflow` on phase tasks.
- 🧠 Reflection: Hard-stop gates reduce process drift and phase-skipping risk.

## Evaluation notes (flywheel)

- Failure modes observed: Native quick_validate.py could not run due missing PyYAML dependency.
- Graders run and results (PASS/FAIL): Manual structural checks PASS.
- Prompt variant (if applicable): workflow-skill-v1.
- Next experiment (smallest change to try): Add an optional script-based checker in skill `scripts/` for deterministic gate evaluation.
