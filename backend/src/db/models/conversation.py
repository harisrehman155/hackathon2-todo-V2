import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel

from src.lib_time import utcnow


class Conversation(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    owner_user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=utcnow)
