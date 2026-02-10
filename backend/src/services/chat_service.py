from dataclasses import dataclass
import logging
import os
import time
from uuid import uuid4

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from sqlmodel import Session, select

from src.config import get_settings
from src.db.models.conversation import Conversation
from src.db.models.message import Message

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class ChatServiceError(Exception):
    message: str
    code: str
    status_code: int
    conversation_id: str | None = None


def _safe_int(value: object) -> int | None:
    try:
        if value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _extract_usage(result: object) -> tuple[int | None, int | None, int | None]:
    usage = getattr(result, "usage", None)
    if usage is None:
        return (None, None, None)

    if isinstance(usage, dict):
        input_tokens = _safe_int(usage.get("input_tokens") or usage.get("prompt_tokens"))
        output_tokens = _safe_int(usage.get("output_tokens") or usage.get("completion_tokens"))
        total_tokens = _safe_int(usage.get("total_tokens"))
    else:
        input_tokens = _safe_int(getattr(usage, "input_tokens", None) or getattr(usage, "prompt_tokens", None))
        output_tokens = _safe_int(getattr(usage, "output_tokens", None) or getattr(usage, "completion_tokens", None))
        total_tokens = _safe_int(getattr(usage, "total_tokens", None))

    if total_tokens is None and input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens
    return (input_tokens, output_tokens, total_tokens)


def _estimate_cost_usd(model: str, input_tokens: int | None, output_tokens: int | None) -> float | None:
    # Best-effort estimate for quick observability; keep this map explicit and easy to update.
    # Values are USD per 1M tokens.
    pricing_per_million = {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    }
    pricing = pricing_per_million.get(model)
    if not pricing or input_tokens is None or output_tokens is None:
        return None
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    return round(input_cost + output_cost, 8)


def _extract_tool_call_count(result: object) -> int | None:
    new_items = getattr(result, "new_items", None)
    if not isinstance(new_items, list):
        return None
    count = 0
    for item in new_items:
        name = type(item).__name__.lower()
        if "tool" in name and "call" in name:
            count += 1
    return count


def _log_chat_observability(
    *,
    request_id: str,
    user_id: str,
    conversation_id: str,
    model: str,
    message: str,
    history_count: int,
    elapsed_ms: int,
    outcome: str,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    total_tokens: int | None = None,
    estimated_cost_usd: float | None = None,
    tool_calls: int | None = None,
    error: str | None = None,
) -> None:
    lines = [
        "",
        "========================== CHAT OBSERVABILITY ==========================",
        f"request_id      : {request_id}",
        f"outcome         : {outcome}",
        f"user_id         : {user_id}",
        f"conversation_id : {conversation_id}",
        f"model           : {model}",
        f"message_len     : {len(message)}",
        f"history_msgs    : {history_count}",
        f"latency_ms      : {elapsed_ms}",
        f"input_tokens    : {input_tokens if input_tokens is not None else 'N/A'}",
        f"output_tokens   : {output_tokens if output_tokens is not None else 'N/A'}",
        f"total_tokens    : {total_tokens if total_tokens is not None else 'N/A'}",
        f"est_cost_usd    : {estimated_cost_usd if estimated_cost_usd is not None else 'N/A'}",
        f"tool_calls      : {tool_calls if tool_calls is not None else 'N/A'}",
    ]
    if error:
        lines.append(f"error           : {error}")
    lines.append("=======================================================================")
    logger.info("\n".join(lines))


class ChatService:
    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_id: str | None,
        session: Session,
    ) -> dict[str, str]:
        request_id = str(uuid4())
        start_time = time.perf_counter()
        model_name = "gpt-4o-mini"

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

        result = None
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
                    model=model_name,
                )
                result = await Runner.run(agent, input_messages)
        except Exception as exc:
            # Some MCP transports can raise during shutdown after a successful tool run.
            # If we already have a model result, keep the user-facing response successful.
            if result is not None:
                logger.warning("Ignoring MCP cleanup error after successful run: %s", exc)
            else:
                elapsed_ms = int((time.perf_counter() - start_time) * 1000)
                _log_chat_observability(
                    request_id=request_id,
                    user_id=user_id,
                    conversation_id=conversation.id,
                    model=model_name,
                    message=message,
                    history_count=len(input_messages),
                    elapsed_ms=elapsed_ms,
                    outcome="error",
                    error=str(exc),
                )
                raise ChatServiceError(
                    message="Assistant is temporarily unavailable. Your message has been saved. Please try again.",
                    code="service_error",
                    status_code=500,
                    conversation_id=conversation.id,
                ) from exc

        if result is None:
            raise ChatServiceError(
                message="Assistant is temporarily unavailable. Your message has been saved. Please try again.",
                code="service_error",
                status_code=500,
                conversation_id=conversation.id,
            )

        assistant_text = str(result.final_output)
        assistant_message = Message(conversation_id=conversation.id, role="assistant", content=assistant_text)
        session.add(assistant_message)
        session.commit()

        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        input_tokens, output_tokens, total_tokens = _extract_usage(result)
        estimated_cost_usd = _estimate_cost_usd(model_name, input_tokens, output_tokens)
        tool_calls = _extract_tool_call_count(result)
        _log_chat_observability(
            request_id=request_id,
            user_id=user_id,
            conversation_id=conversation.id,
            model=model_name,
            message=message,
            history_count=len(input_messages),
            elapsed_ms=elapsed_ms,
            outcome="success",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=estimated_cost_usd,
            tool_calls=tool_calls,
        )

        return {"response": assistant_text, "conversation_id": conversation.id}
