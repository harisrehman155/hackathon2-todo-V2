from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


class ChatErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: str
    code: str
    conversation_id: Optional[str] = None
