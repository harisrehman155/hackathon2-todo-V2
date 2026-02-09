from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.auth.dependencies import CurrentUser, get_current_user
from src.db.dependencies import get_session
from src.db.models.conversation import Conversation
from src.schemas.chat import ChatErrorResponse, ChatRequest, ChatResponse
from src.services.chat_service import ChatService, ChatServiceError


router = APIRouter(prefix="/api", tags=["chat"])
service = ChatService()


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ChatErrorResponse},
        401: {"model": ChatErrorResponse},
        403: {"model": ChatErrorResponse},
        500: {"model": ChatErrorResponse},
    },
)
async def chat(
    payload: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    message = payload.message.strip()
    if not message or len(message) > 2000:
        raise HTTPException(status_code=400, detail={"error": "Message must be between 1 and 2000 characters", "code": "bad_request"})

    conversation_id: str | None = None
    if payload.conversation_id:
        try:
            parsed = UUID(payload.conversation_id)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail={"error": "Invalid conversation_id", "code": "bad_request"}) from exc
        conversation_id = str(parsed)
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.owner_user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail={"error": "Conversation not found", "code": "not_found"})

    try:
        result = await service.process_message(current_user.user_id, message, conversation_id, session)
        return ChatResponse(**result)
    except ChatServiceError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail={"error": exc.message, "code": exc.code, "conversation_id": exc.conversation_id},
        ) from exc
