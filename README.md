# hackathon2-todo-V2

## Phase I Todo Console Foundation

In-memory Python todo console supporting:
- add task
- list tasks
- update task
- complete/uncomplete task
- delete task

## Setup

```powershell
Set-Location D:\Haris\hackathons\hackathon2
uv sync --group dev
```

## Run Tests

```powershell
uv run pytest -q
```

Current result: `13 passed`

## Scripted Acceptance Evidence

Command transcript captured from an in-memory session:

```text
$ add --title Plan sprint --description Phase I
Created task #1: Plan sprint (pending)
$ add --title Write tests
Created task #2: Write tests (pending)
$ list
#1 [PENDING] Plan sprint
#2 [PENDING] Write tests
$ update --id 2 --description Pytest first
Updated task #2: Write tests
$ complete --id 2
Marked complete task #2.
$ list
#1 [PENDING] Plan sprint
#2 [COMPLETE] Write tests
$ uncomplete --id 2
Marked pending task #2.
$ delete --id 1
Deleted task #1.
$ list
#2 [PENDING] Write tests
```

## Key Files

- `src/models/task.py`
- `src/lib/validators.py`
- `src/lib/errors.py`
- `src/services/task_service.py`
- `src/cli/commands.py`
- `tests/unit/test_task_service.py`
- `tests/integration/test_cli_commands.py`
- `specs/001-phase1-todo-spec/tasks.md`
