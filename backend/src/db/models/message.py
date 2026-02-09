from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, Column, String
from sqlmodel import Field, SQLModel

from src.lib_time import utcnow


class Message(SQLModel, table=True):
    __table_args__ = (CheckConstraint("role IN ('user', 'assistant')", name="message_role_check"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    role: str = Field(sa_column=Column(String(10), nullable=False))
    content: str
    created_at: datetime = Field(default_factory=utcnow)
