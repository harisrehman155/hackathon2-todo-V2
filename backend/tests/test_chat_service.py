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


@pytest.fixture
def engine():
    test_engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(test_engine)
    return test_engine


@pytest.fixture
def patch_runner(monkeypatch):
    captured = {"messages": None}

    async def fake_run(agent, messages):
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
    async def fake_run(agent, messages):
        return SimpleNamespace(final_output="Task 'Buy milk' has been created.")

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)

    service = ChatService()
    with Session(engine) as session:
        result = await service.process_message("user-a", "add buy milk", None, session)

    assert "has been created" in result["response"]


@pytest.mark.anyio
async def test_non_existent_task_returns_helpful_error_text(engine, monkeypatch):
    async def fake_run(agent, messages):
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
    async def failing_run(agent, messages):
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

    async def fake_run(agent, messages):
        captured["instructions"] = agent.instructions
        return SimpleNamespace(final_output="ok")

    monkeypatch.setattr("src.services.chat_service.MCPServerStdio", DummyMCP)
    monkeypatch.setattr("src.services.chat_service.Runner.run", fake_run)

    service = ChatService()
    with Session(engine) as session:
        await service.process_message("user-xyz", "list tasks", None, session)

    assert "user-xyz" in captured["instructions"]


@pytest.mark.anyio
async def test_cleanup_error_after_successful_run_is_ignored(engine, monkeypatch):
    async def fake_run(agent, messages):
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
    async def fake_run(agent, messages):
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

    assert "CHAT OBSERVABILITY" in caplog.text
    assert "outcome         : success" in caplog.text
    assert "model           : gpt-4o-mini" in caplog.text
