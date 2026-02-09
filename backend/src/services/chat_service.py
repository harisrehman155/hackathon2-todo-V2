from dataclasses import dataclass
import os

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from sqlmodel import Session, select

from src.config import get_settings
from src.db.models.conversation import Conversation
from src.db.models.message import Message


@dataclass
class ChatServiceError(Exception):
    message: str
    code: str
    status_code: int
    conversation_id: str | None = None


class ChatService:
    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_id: str | None,
        session: Session,
    ) -> dict[str, str]:
        if conversation_id:
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.owner_user_id != user_id:
                raise ChatServiceError("Conversation not found", "not_found", 403)
        else:
            conversation = Conversation(owner_user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        user_message = Message(conversation_id=conversation.id, role="user", content=message)
        session.add(user_message)
        session.commit()

        history = list(
            session.exec(
                select(Message)
                .where(Message.conversation_id == conversation.id)
                .order_by(Message.created_at, Message.id)
            )
        )
        input_messages = [{"role": item.role, "content": item.content} for item in history]

        settings = get_settings()
        if settings.openai_api_key:
            os.environ["OPENAI_API_KEY"] = settings.openai_api_key

        try:
            async with MCPServerStdio(
                name="Todo MCP",
                params={"command": "uv", "args": ["run", "-m", "src.mcp.server"]},
            ) as mcp_server:
                instructions = (
                    "You are a todo assistant. "
                    f"The current user ID is {user_id}. "
                    "Always pass this user_id to every tool call. "
                    "For successful actions use confirmation format: "
                    "\"Task 'X' has been created/completed/deleted/updated.\" "
                    "If a task cannot be found, explain clearly and suggest a corrective next step. "
                    "If the command is ambiguous, ask a short clarifying question before taking action."
                )
                agent = Agent(
                    name="Todo Assistant",
                    instructions=instructions,
                    mcp_servers=[mcp_server],
                    model="gpt-4o-mini",
                )
                result = await Runner.run(agent, input_messages)
        except Exception as exc:
            raise ChatServiceError(
                message="Assistant is temporarily unavailable. Your message has been saved. Please try again.",
                code="service_error",
                status_code=500,
                conversation_id=conversation.id,
            ) from exc

        assistant_text = str(result.final_output)
        assistant_message = Message(conversation_id=conversation.id, role="assistant", content=assistant_text)
        session.add(assistant_message)
        session.commit()

        return {"response": assistant_text, "conversation_id": conversation.id}
