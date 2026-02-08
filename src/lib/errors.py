class TaskError(Exception):
    """Base task domain error."""


class ValidationError(TaskError):
    """Raised when user input fails validation."""


class TaskNotFoundError(TaskError):
    """Raised when the given task ID does not exist."""

