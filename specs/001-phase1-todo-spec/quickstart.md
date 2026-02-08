# Quickstart: Phase I Todo Console Foundation

## Prerequisites
- Python 3.13+
- PowerShell or Bash shell

## Setup
```powershell
Set-Location D:\Haris\hackathons\hackathon2
uv sync --group dev
```

## Test-First Workflow (Required)
1. Write/adjust tests under `tests/unit/` and `tests/integration/` for targeted story requirements.
2. Run tests before implementation and confirm failing state (Red):
```powershell
uv run pytest -q
```
3. Implement minimum code to satisfy failing tests (Green).
4. Refactor with tests still green (Refactor).
5. Re-run full suite:
```powershell
uv run pytest
```

## Expected Command Surface
- `add --title <text> [--description <text>]`
- `list`
- `update --id <int> [--title <text>] [--description <text>]`
- `complete --id <int>`
- `uncomplete --id <int>`
- `delete --id <int>`

## Validation Evidence Checklist
- Story 1: Add/list behavior validated by tests and command transcript.
- Story 2: Update/toggle/delete behavior validated by tests and command transcript.
- Story 3: Mixed-state and empty-state list behavior validated by tests.
- Invalid-ID and input-validation paths verified via negative tests.

## Traceability Pointers
- Requirements: `D:\Haris\hackathons\hackathon2\specs\001-phase1-todo-spec\spec.md`
- Data model: `D:\Haris\hackathons\hackathon2\specs\001-phase1-todo-spec\data-model.md`
- Contract: `D:\Haris\hackathons\hackathon2\specs\001-phase1-todo-spec\contracts\todo-api.openapi.yaml`
- Next stage artifact: `D:\Haris\hackathons\hackathon2\specs\001-phase1-todo-spec\tasks.md`
