# Specification and Quality Gates

## Stage gates

1. Specify gate
- `spec.md` exists.
- User stories, acceptance scenarios, edge cases, assumptions, and measurable outcomes are complete.

2. Plan gate
- `plan.md` exists.
- Constitution checks are explicit.
- Phase scope and risk handling are documented.

3. Tasks gate
- `tasks.md` exists.
- Tasks map to stories and requirements.
- Validation tasks exist for each story.

4. Implement gate
- Implementation only starts after tasks approval.
- Traceability from requirement -> task -> validation is preserved.

## TDD gate for Python

- Tests written first with `pytest`.
- Failing state confirmed before implementation.
- Passing state confirmed before merge.

## Evidence gate

- Validation outputs recorded.
- Phase deliverables and submission artifacts updated for completed scope.

## Hard-stop conditions

- Missing required stage artifact.
- No test evidence for changed behavior.
- Missing traceability mapping.

## Output checklist

- Stage completion summary
- Files updated
- Validation result
- Remaining blockers

## Checker JSON Contracts

`detect-next-step.ps1`:

```json
{
  "phase": "phase1",
  "branch_type": "phase|feature|invalid",
  "active_feature": "001-phase1-todo-spec",
  "detected_step": "Specify|Plan|Tasks|Implement|Blocked",
  "missing_artifacts": ["spec.md", "plan.md", "tasks.md"],
  "reason": "human-readable reason",
  "can_proceed": true
}
```

`current-next-step.ps1`:

```json
{
  "phase": "phase1",
  "branch_type": "feature|phase|invalid",
  "active_feature": "001-phase1-todo-spec",
  "current_step": "Specify|Plan|Tasks|None|Unknown",
  "current_step_done": true,
  "next_step": "Specify|Plan|Tasks|Implement|Blocked",
  "next_command": "/sp.specify|/sp.plan|/sp.tasks|/sp.implement",
  "can_proceed": true,
  "missing_artifacts": [],
  "reason": "human-readable reason",
  "message": "Current step and next step summary"
}
```

`check-phase-complete.ps1`:

```json
{
  "phase": "phase1",
  "status": "complete|incomplete|blocked",
  "gates": {
    "spec_gate": "pass|fail",
    "plan_gate": "pass|fail",
    "tasks_gate": "pass|fail",
    "implementation_gate": "pass|fail",
    "pytest_gate": "pass|fail",
    "evidence_gate": "pass|fail"
  },
  "missing_items": ["..."],
  "recommendation": "self_test|phase_transition_prep|fix_blockers"
}
```

## Command execution mapping

- `next_step = Specify` -> run `/sp.specify`
- `next_step = Plan` -> run `/sp.plan`
- `next_step = Tasks` -> run `/sp.tasks`
- `next_step = Implement` -> run `/sp.implement`
- `next_step = Blocked` -> do not execute `sp.*`
