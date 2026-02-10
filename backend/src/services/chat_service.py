from dataclasses import dataclass
import logging
import os
import re
import time
from uuid import uuid4

from agents import Agent, ModelSettings, RunConfig, Runner
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
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None

    if usage is not None:
        if isinstance(usage, dict):
            input_tokens = _safe_int(usage.get("input_tokens") or usage.get("prompt_tokens"))
            output_tokens = _safe_int(usage.get("output_tokens") or usage.get("completion_tokens"))
            total_tokens = _safe_int(usage.get("total_tokens"))
        else:
            input_tokens = _safe_int(getattr(usage, "input_tokens", None) or getattr(usage, "prompt_tokens", None))
            output_tokens = _safe_int(getattr(usage, "output_tokens", None) or getattr(usage, "completion_tokens", None))
            total_tokens = _safe_int(getattr(usage, "total_tokens", None))

    if input_tokens is None or output_tokens is None:
        raw_responses = getattr(result, "raw_responses", None)
        if isinstance(raw_responses, list):
            agg_input = 0
            agg_output = 0
            seen = False
            for response in raw_responses:
                raw_usage = getattr(response, "usage", None)
                if raw_usage is None:
                    continue
                seen = True
                this_input = _safe_int(getattr(raw_usage, "input_tokens", None))
                this_output = _safe_int(getattr(raw_usage, "output_tokens", None))
                if this_input is not None:
                    agg_input += this_input
                if this_output is not None:
                    agg_output += this_output
            if seen:
                input_tokens = agg_input
                output_tokens = agg_output
                total_tokens = agg_input + agg_output

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


_TASK_COMMAND_PATTERNS = [
    r"\badd\b",
    r"\bcreate\b",
    r"\blist\b",
    r"\bshow\b",
    r"\bpending\b",
    r"\bcompleted?\b",
    r"\bcomplete\b",
    r"\bmark\b",
    r"\bdelete\b",
    r"\bremove\b",
    r"\bupdate\b",
    r"\bchange\b",
    r"\btask\b",
    r"\btodo\b",
]


def _looks_like_task_command(message: str) -> bool:
    lowered = message.lower()
    return any(re.search(pattern, lowered) for pattern in _TASK_COMMAND_PATTERNS)


def _extract_tool_call_count(result: object) -> int | None:
    names = _extract_tool_names(result)
    if names is None:
        return None
    return len(names)


def _extract_tool_names(result: object) -> list[str] | None:
    new_items = getattr(result, "new_items", None)
    if not isinstance(new_items, list):
        return None
    names: list[str] = []
    for item in new_items:
        name = type(item).__name__.lower()
        if "tool" not in name or "call" not in name:
            continue

        for attr in ("tool_name", "name"):
            value = getattr(item, attr, None)
            if isinstance(value, str) and value.strip():
                names.append(value.strip())
                break
        else:
            raw_item = getattr(item, "raw_item", None)
            resolved = False
            for raw_attr in ("name", "tool_name"):
                raw_value = getattr(raw_item, raw_attr, None)
                if isinstance(raw_value, str) and raw_value.strip():
                    names.append(raw_value.strip())
                    resolved = True
                    break
            if resolved:
                continue

            if not resolved:
                action = getattr(raw_item, "action", None)
                action_type = getattr(action, "type", None)
                if isinstance(action_type, str) and action_type.strip():
                    names.append(action_type.strip())
                    continue

            if isinstance(raw_item, dict):
                candidate = raw_item.get("name") or raw_item.get("tool_name")
                if isinstance(candidate, str) and candidate.strip():
                    names.append(candidate.strip())
                    continue
            names.append("unknown_tool")
    return names


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
    tool_names: list[str] | None = None,
    error: str | None = None,
) -> None:
    joined_tools = ",".join(tool_names) if tool_names else "none"
    line = (
        "CHAT_METRICS "
        f"model={model} "
        f"tools={tool_calls if tool_calls is not None else 'N/A'}[{joined_tools}] "
        f"tokens_in={input_tokens if input_tokens is not None else 'N/A'} "
        f"tokens_out={output_tokens if output_tokens is not None else 'N/A'} "
        f"cost_usd={estimated_cost_usd if estimated_cost_usd is not None else 'N/A'}"
    )
    logger.info(line)


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
        if settings.openai_api_key_tracing:
            os.environ["OPENAI_API_KEY_TRACING"] = settings.openai_api_key_tracing

        result = None
        try:
            async with MCPServerStdio(
                name="Todo MCP",
                params={"command": "uv", "args": ["run", "-m", "src.mcp.server"]},
                client_session_timeout_seconds=30,
                max_retry_attempts=1,
                retry_backoff_seconds_base=0.5,
            ) as mcp_server:
                instructions = (
                    "You are a todo assistant. "
                    f"The current user ID is {user_id}. "
                    "Always pass this user_id to every tool call. "
                    "For any task mutation request (add, complete, update, delete), you must call the MCP tools. "
                    "Never claim a task mutation succeeded unless a tool returned success. "
                    "If a tool returns 'Task not found.', tell the user it failed and ask for a valid id/title context. "
                    "Mark complete by title flow: first call list_tasks, find a single exact or best match, then call complete_task with task_id. "
                    "Delete by name flow: first call list_tasks, resolve a single matching task, then call delete_task with task_id. "
                    "If multiple matches exist, ask a clarifying question before mutating. "
                    "If no match exists, do not fabricate success. "
                    "When asked for pending/completed/all tasks, call list_tasks with the matching status filter. "
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
                    model_settings=ModelSettings(
                        tool_choice="required" if _looks_like_task_command(message) else "auto"
                    ),
                )
                run_config = (
                    RunConfig(tracing={"api_key": settings.openai_api_key_tracing})
                    if settings.openai_api_key_tracing
                    else None
                )
                result = await Runner.run(agent, input_messages, run_config=run_config)
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
                    tool_names=[],
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
        tool_names = _extract_tool_names(result) or []
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
            tool_names=tool_names,
        )

        return {
            "response": assistant_text,
            "conversation_id": conversation.id,
            "tool_count": len(tool_names),
            "tool_names": tool_names,
        }
