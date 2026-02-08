from __future__ import annotations

from typing import Optional

from src.lib.errors import ValidationError

MAX_TITLE_LENGTH = 120
MAX_DESCRIPTION_LENGTH = 500


def validate_title(title: str) -> str:
    cleaned = title.strip()
    if not cleaned:
        raise ValidationError("Title cannot be blank.")
    if len(cleaned) > MAX_TITLE_LENGTH:
        raise ValidationError(
            f"Title must be at most {MAX_TITLE_LENGTH} characters long."
        )
    return cleaned


def validate_description(description: Optional[str]) -> Optional[str]:
    if description is None:
        return None
    cleaned = description.strip()
    if len(cleaned) > MAX_DESCRIPTION_LENGTH:
        raise ValidationError(
            f"Description must be at most {MAX_DESCRIPTION_LENGTH} characters long."
        )
    return cleaned

