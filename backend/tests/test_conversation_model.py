from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select

from src.db.models.conversation import Conversation


def test_conversation_crud_and_query_by_owner():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        first = Conversation(owner_user_id="user-a")
        second = Conversation(owner_user_id="user-a")
        third = Conversation(owner_user_id="user-b")
        session.add(first)
        session.add(second)
        session.add(third)
        session.commit()

        rows = list(
            session.exec(
                select(Conversation)
                .where(Conversation.owner_user_id == "user-a")
                .order_by(Conversation.created_at)
            )
        )

    assert len(rows) == 2
    assert rows[0].owner_user_id == "user-a"
    assert rows[1].owner_user_id == "user-a"
    assert rows[0].id
    assert rows[0].created_at is not None


def test_conversation_table_is_auto_created_via_metadata(tmp_path: Path):
    db_path = tmp_path / "conversation.db"
    engine = create_engine(f"sqlite:///{db_path.as_posix()}")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        created = Conversation(owner_user_id="owner-1")
        session.add(created)
        session.commit()

        fetched = session.get(Conversation, created.id)

    assert fetched is not None
    assert fetched.owner_user_id == "owner-1"
