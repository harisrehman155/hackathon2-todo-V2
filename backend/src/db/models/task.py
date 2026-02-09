from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from src.lib_time import utcnow


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_user_id: str = Field(index=True)
    title: str = Field(max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

