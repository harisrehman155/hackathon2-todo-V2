from datetime import timedelta

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, SQLModel, create_engine, select

from src.db.models.conversation import Conversation
from src.db.models.message import Message
from src.lib_time import utcnow


def test_message_crud_and_ordering_by_created_at():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        conv = Conversation(owner_user_id="user-a")
        session.add(conv)
        session.commit()
        session.refresh(conv)

        first = Message(
            conversation_id=conv.id,
            role="user",
            content="first",
            created_at=utcnow() - timedelta(seconds=2),
        )
        second = Message(
            conversation_id=conv.id,
            role="assistant",
            content="second",
            created_at=utcnow() - timedelta(seconds=1),
        )
        session.add(first)
        session.add(second)
        session.commit()

        rows = list(
            session.exec(
                select(Message)
                .where(Message.conversation_id == conv.id)
                .order_by(Message.created_at)
            )
        )

    assert len(rows) == 2
    assert rows[0].content == "first"
    assert rows[1].content == "second"
    assert rows[0].created_at <= rows[1].created_at


def test_message_role_validation():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        conv = Conversation(owner_user_id="user-a")
        session.add(conv)
        session.commit()
        session.refresh(conv)

        with pytest.raises(IntegrityError):
            invalid = Message(conversation_id=conv.id, role="system", content="bad-role")
            session.add(invalid)
            session.commit()
