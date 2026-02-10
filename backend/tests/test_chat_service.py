from types import SimpleNamespace

import pytest
import logging
from sqlmodel import Session, SQLModel, create_engine, select

from src.db.models.conversation import Conversation
from src.db.models.message import Message
from src.services.chat_service import ChatService, ChatServiceError


class DummyMCP:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class DummyMCPExitRaises:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        raise RuntimeError("cleanup failure")


class DummyToolCallItem:
    def __init__(self, tool_name: str):
        self.raw_item = SimpleNamespace(name=tool_name)


@pytest.fixture
def engine():
    test_engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(test_engine)
    return test_engine


@pytest.fixture
def patch_runner(monkeypatch):
    captured = {"messages": None}

    async def fake_run(agent, messages, **kwargs):
        captured["messages"] = messages
        return SimpleNamespace(final_output="assistant reply")

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)
    return captured


@pytest.mark.anyio
async def test_new_conversation_created_when_missing_conversation_id(engine, patch_runner):
    service = ChatService()
    with Session(engine) as session:
        result = await service.process_message("user-a", "hello", None, session)

        conversation = session.get(Conversation, result["conversation_id"])
        messages = list(
            session.exec(
                select(Message)
                .where(Message.conversation_id == result["conversation_id"])
                .order_by(Message.created_at, Message.id)
            )
        )

    assert conversation is not None
    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[1].role == "assistant"


@pytest.mark.anyio
async def test_existing_conversation_loads_history(engine, patch_runner):
    with Session(engine) as session:
        conv = Conversation(owner_user_id="user-a")
        session.add(conv)
        session.commit()
        session.refresh(conv)
        session.add(Message(conversation_id=conv.id, role="user", content="older user"))
        session.add(Message(conversation_id=conv.id, role="assistant", content="older assistant"))
        session.commit()
        conversation_id = conv.id

    service = ChatService()
    with Session(engine) as session:
        await service.process_message("user-a", "new user msg", conversation_id, session)

    history = patch_runner["messages"]
    assert history is not None
    assert history[0]["content"] == "older user"
    assert history[1]["content"] == "older assistant"
    assert history[2]["content"] == "new user msg"


@pytest.mark.anyio
async def test_conversation_persists_across_service_restart(engine, patch_runner):
    service_one = ChatService()
    with Session(engine) as session:
        first = await service_one.process_message("user-a", "first", None, session)
        conversation_id = first["conversation_id"]

    service_two = ChatService()
    with Session(engine) as session:
        second = await service_two.process_message("user-a", "second", conversation_id, session)

        messages = list(
            session.exec(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at, Message.id)
            )
        )

    assert second["conversation_id"] == conversation_id
    assert len(messages) == 4


@pytest.mark.anyio
async def test_conversation_ownership_rejects_wrong_user(engine, patch_runner):
    with Session(engine) as session:
        conv = Conversation(owner_user_id="user-a")
        session.add(conv)
        session.commit()
        session.refresh(conv)
        conversation_id = conv.id

    service = ChatService()
    with Session(engine) as session:
        with pytest.raises(ChatServiceError) as err:
            await service.process_message("user-b", "hello", conversation_id, session)

    assert err.value.status_code == 403
    assert err.value.code == "not_found"


@pytest.mark.anyio
async def test_successful_actions_include_confirmation_text(engine, monkeypatch):
    async def fake_run(agent, messages, **kwargs):
        return SimpleNamespace(final_output="Task 'Buy milk' has been created.")

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)

    service = ChatService()
    with Session(engine) as session:
        result = await service.process_message("user-a", "add buy milk", None, session)

    assert "has been created" in result["response"]


@pytest.mark.anyio
async def test_non_existent_task_returns_helpful_error_text(engine, monkeypatch):
    async def fake_run(agent, messages, **kwargs):
        return SimpleNamespace(final_output="Task not found. Please provide a valid task id.")

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)

    service = ChatService()
    with Session(engine) as session:
        result = await service.process_message("user-a", "complete task 999", None, session)

    assert "Task not found" in result["response"]
    assert "valid task id" in result["response"]


@pytest.mark.anyio
async def test_openai_failure_returns_user_friendly_error_and_persists_user_message(engine, monkeypatch):
    async def failing_run(agent, messages, **kwargs):
        raise RuntimeError("OpenAI timeout")

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", failing_run)

    service = ChatService()
    with Session(engine) as session:
        with pytest.raises(ChatServiceError) as err:
            await service.process_message("user-a", "add task", None, session)
        conv_id = err.value.conversation_id
        stored = list(
            session.exec(
                select(Message)
                .where(Message.conversation_id == conv_id)
                .order_by(Message.created_at, Message.id)
            )
        )

    assert err.value.status_code == 500
    assert err.value.code == "service_error"
    assert "temporarily unavailable" in err.value.message
    assert len(stored) == 1
    assert stored[0].role == "user"


@pytest.mark.anyio
async def test_agent_instructions_include_user_id_context(engine, monkeypatch):
    captured = {}

    async def fake_run(agent, messages, **kwargs):
        captured["instructions"] = agent.instructions
        return SimpleNamespace(final_output="ok")

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)

    service = ChatService()
    with Session(engine) as session:
        await service.process_message("user-xyz", "list tasks", None, session)

    assert "user-xyz" in captured["instructions"]


@pytest.mark.anyio
async def test_agent_instructions_enforce_task_tool_workflow(engine, monkeypatch):
    captured = {}

    async def fake_run(agent, messages, **kwargs):
        captured["instructions"] = agent.instructions
        return SimpleNamespace(final_output="ok")

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)

    service = ChatService()
    with Session(engine) as session:
        await service.process_message("user-abc", "delete the meeting task", None, session)

    instructions = captured["instructions"]
    assert "Never claim a task mutation succeeded unless a tool returned success" in instructions
    assert "Delete by name flow: first call list_tasks" in instructions
    assert "Mark complete by title flow: first call list_tasks" in instructions


@pytest.mark.anyio
async def test_task_commands_require_tool_choice(engine, monkeypatch):
    captured = {}

    async def fake_run(agent, messages, **kwargs):
        captured["agent"] = agent
        return SimpleNamespace(final_output="ok")

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)

    service = ChatService()
    with Session(engine) as session:
        await service.process_message("user-abc", "Add a task to buy groceries", None, session)

    agent = captured["agent"]
    assert agent.model_settings.tool_choice == "required"


@pytest.mark.anyio
async def test_non_task_messages_keep_auto_tool_choice(engine, monkeypatch):
    captured = {}

    async def fake_run(agent, messages, **kwargs):
        captured["agent"] = agent
        return SimpleNamespace(final_output="ok")

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)

    service = ChatService()
    with Session(engine) as session:
        await service.process_message("user-abc", "Hello there", None, session)

    agent = captured["agent"]
    assert agent.model_settings.tool_choice == "auto"


@pytest.mark.anyio
async def test_runner_receives_tracing_api_key_from_settings(engine, monkeypatch):
    captured = {}

    async def fake_run(agent, messages, **kwargs):
        captured["run_config"] = kwargs.get("run_config")
        return SimpleNamespace(final_output="ok")

    monkeypatch.setenv("OPENAI_API_KEY_TRACING", "trace-key-123")
    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)

    service = ChatService()
    with Session(engine) as session:
        await service.process_message("user-abc", "hello", None, session)

    run_config = captured["run_config"]
    assert run_config is not None
    assert run_config.tracing == {"api_key": "trace-key-123"}


@pytest.mark.anyio
async def test_cleanup_error_after_successful_run_is_ignored(engine, monkeypatch):
    async def fake_run(agent, messages, **kwargs):
        return SimpleNamespace(final_output="Task 'Buy milk' has been created.")

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCPExitRaises)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)

    service = ChatService()
    with Session(engine) as session:
        result = await service.process_message("user-a", "add task", None, session)

        stored = list(
            session.exec(
                select(Message)
                .where(Message.conversation_id == result["conversation_id"])
                .order_by(Message.created_at, Message.id)
            )
        )

    assert "has been created" in result["response"]
    assert len(stored) == 2
    assert stored[1].role == "assistant"


@pytest.mark.anyio
async def test_chat_observability_log_emits_formatted_block(engine, monkeypatch, caplog):
    async def fake_run(agent, messages, **kwargs):
        return SimpleNamespace(
            final_output="Task 'Buy milk' has been created.",
            usage={"input_tokens": 120, "output_tokens": 42, "total_tokens": 162},
            new_items=[],
        )

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)

    service = ChatService()
    caplog.set_level(logging.INFO, logger="src.services.chat_service")

    with Session(engine) as session:
        await service.process_message("user-a", "add task", None, session)

    assert "CHAT_METRICS" in caplog.text
    assert "model=gpt-4o-mini" in caplog.text
    assert "tokens_in=120" in caplog.text
    assert "tokens_out=42" in caplog.text


@pytest.mark.anyio
async def test_chat_response_includes_tool_names_from_raw_items(engine, monkeypatch):
    async def fake_run(agent, messages, **kwargs):
        return SimpleNamespace(
            final_output="Task 'Buy milk' has been created.",
            usage={"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
            new_items=[DummyToolCallItem("add_task")],
        )

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)

    service = ChatService()
    with Session(engine) as session:
        result = await service.process_message("user-a", "add task", None, session)

    assert result["tool_count"] == 1
    assert result["tool_names"] == ["add_task"]

