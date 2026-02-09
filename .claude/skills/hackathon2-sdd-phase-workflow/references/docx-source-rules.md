# DOCX Source Rules for Requirement Updates

Use this only when requirements are extracted or reconciled from `Hackathon 2.docx`.

## Workflow

1. Extract source statements from `.docx`.
2. Normalize into requirement language.
3. Update feature spec sections first, then plan/tasks artifacts.
4. Record assumptions for ambiguous narrative text.

## Conflict handling

- If two source statements conflict, do not merge silently.
- Surface conflict and choose one via explicit decision note.

## Scope control

- Keep extraction focused on active phase.
- Avoid importing future-phase implementation details into current-phase scope.

## Evidence expectations

- Keep a short mapping from source statement to spec requirement.
- Ensure updated requirements remain testable and measurable.
