# Branching Strategy Rules

## Canonical branch model

- Keep one active phase branch: `phase1` -> `phase2` -> `phase3` -> `phase4` -> `phase5`.
- Create feature branches as `NNN-short-name` from the active phase branch.
- Merge feature branches back into the same active phase branch.

## Validation checks

1. Current branch check
- Allowed branches for active work: phase branch or feature branch.

2. Feature branch naming check
- Must match: `^[0-9]{3}-[a-z0-9-]+$`

3. Base branch check
- Feature branch must be cut from active phase branch.

4. Merge target check
- Merge target must be active phase branch.

5. Phase transition check
- Do not create/activate next phase branch until current phase done criteria pass.
- Run `scripts/check-phase-complete.ps1` first and require `status = complete`.

## Hard-stop conditions

- Branch naming invalid.
- Feature branch based on wrong phase branch.
- Merge target outside active phase branch.
- Attempt to begin next phase with incomplete current phase gates.

## Unblock actions

- Checkout active phase branch.
- Recreate feature branch from correct base.
- Complete missing phase gates before branch transition.
