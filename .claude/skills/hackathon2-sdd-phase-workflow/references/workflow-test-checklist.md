# Workflow Self-Test Checklist

Use this when Phase 1 completion status is `PASS` and user selects:
`A) Test workflow yourself now`.

## Self-test steps

1. Branch and context
- Confirm current branch is `phase1` or Phase 1 feature branch.
- Confirm active feature path is correct under `specs/<feature>/`.

2. SDD artifacts
- Confirm `spec.md`, `plan.md`, `tasks.md` all exist.
- Confirm checklists are present and updated.

3. TDD workflow
- Confirm tests were authored first for changed behavior.
- Run `pytest` and capture output in `checklists/pytest-evidence.md`.

4. Feature behavior
- Verify Add/View/Update/Delete/Complete flows end-to-end in Phase I app.
- Confirm failures are handled without crashing.

5. Evidence and traceability
- Confirm requirement -> task -> validation mapping is explicit.
- Confirm phase completion checklist has no unchecked items.

6. Step detection behavior
- Run `current-next-step.ps1` and verify `current_step`, `next_step`,
  and `next_command` are consistent with repository artifacts.
- Confirm blocked states do not produce a runnable `next_command`.

## Suggested commands

```powershell
pwsh .codex/skills/hackathon2-sdd-phase-workflow/scripts/current-next-step.ps1
pwsh .codex/skills/hackathon2-sdd-phase-workflow/scripts/detect-next-step.ps1
pwsh .codex/skills/hackathon2-sdd-phase-workflow/scripts/check-phase-complete.ps1
pytest
```
