import pytest
from sqlmodel import Session

from src.db.models.conversation import Conversation


def test_chat_api_success(client, auth_header, monkeypatch):
    async def fake_process_message(user_id, message, conversation_id, session):
        assert user_id == "user-a"
        assert message == "Add task to buy eggs"
        assert conversation_id is None
        return {"response": "Done", "conversation_id": "conv-1"}

    import src.api.routes.chat as chat

    monkeypatch.setattr(chat.service, "process_message", fake_process_message)
    response = client.post("/api/chat", headers=auth_header, json={"message": "Add task to buy eggs"})
    assert response.status_code == 200
    assert response.json()["response"] == "Done"
    assert response.json()["conversation_id"] == "conv-1"


@pytest.mark.parametrize("payload", [{"message": ""}, {"message": " " * 5}, {"message": "x" * 2001}])
def test_chat_api_bad_request_validation(client, auth_header, payload):
    response = client.post("/api/chat", headers=auth_header, json=payload)
    assert response.status_code == 400


def test_chat_api_unauthorized(client):
    response = client.post("/api/chat", json={"message": "hello"})
    assert response.status_code == 401


def test_chat_api_forbidden_for_foreign_conversation(client, other_auth_header):
    with Session(client.app.state.engine) as session:
        conv = Conversation(owner_user_id="user-a")
        session.add(conv)
        session.commit()
        session.refresh(conv)
        conversation_id = conv.id

    response = client.post(
        "/api/chat",
        headers=other_auth_header,
        json={"message": "continue", "conversation_id": conversation_id},
    )
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "not_found"


def test_chat_api_service_error_returns_500_with_conversation_id(client, auth_header, monkeypatch):
    import src.api.routes.chat as chat
    from src.services.chat_service import ChatServiceError

    async def fake_process_message(user_id, message, conversation_id, session):
        raise ChatServiceError(
            message="Assistant is temporarily unavailable. Your message has been saved. Please try again.",
            code="service_error",
            conversation_id="conv-500",
            status_code=500,
        )

    monkeypatch.setattr(chat.service, "process_message", fake_process_message)
    response = client.post("/api/chat", headers=auth_header, json={"message": "Add task"})
    assert response.status_code == 500
    assert response.json()["detail"]["code"] == "service_error"
    assert response.json()["detail"]["conversation_id"] == "conv-500"
