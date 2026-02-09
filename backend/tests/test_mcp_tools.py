import os
from pathlib import Path

import pytest
from sqlmodel import Session, select

from src.db.database import make_engine
from src.db.models.task import Task


def _setup_env(tmp_path: Path) -> None:
    db_path = tmp_path / "mcp-tools.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path.as_posix()}"


async def test_mcp_tools_crud_and_isolation(tmp_path: Path):
    _setup_env(tmp_path)
    from src.mcp import server

    created = await server.add_task("user-a", "Buy milk", "2 liters")
    assert "created" in created.lower()

    list_a = await server.list_tasks("user-a")
    assert "Buy milk" in list_a

    list_b = await server.list_tasks("user-b")
    assert "no tasks" in list_b.lower()

    settings = server._get_settings()
    engine = make_engine(settings)
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.owner_user_id == "user-a")).first()
        assert task is not None
        task_id = task.id

    completed = await server.complete_task("user-a", task_id)
    assert "completed" in completed.lower()

    updated = await server.update_task("user-a", task_id, title="Buy oat milk")
    assert "updated" in updated.lower()
    assert "Buy oat milk" in updated

    denied = await server.delete_task("user-b", task_id)
    assert "not found" in denied.lower()

    deleted = await server.delete_task("user-a", task_id)
    assert "deleted" in deleted.lower()


test_mcp_tools_crud_and_isolation = pytest.mark.anyio(test_mcp_tools_crud_and_isolation)
