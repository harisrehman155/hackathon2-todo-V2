from sqlmodel import Session, select

from mcp.server.fastmcp import FastMCP

from src.config import get_settings
from src.db.database import init_db, make_engine
from src.db.models.task import Task

mcp = FastMCP("Todo Tools")


def _get_settings():
    return get_settings()


def _get_engine():
    engine = make_engine(_get_settings())
    init_db(engine)
    return engine


@mcp.tool()
async def add_task(user_id: str, title: str, description: str = "") -> str:
    trimmed = title.strip()
    if not trimmed:
        return "Task title cannot be empty."
    with Session(_get_engine()) as session:
        task = Task(owner_user_id=user_id, title=trimmed, description=description or None)
        session.add(task)
        session.commit()
        session.refresh(task)
        return f"Task '{task.title}' has been created (id={task.id})."


@mcp.tool()
async def list_tasks(user_id: str, status: str = "all") -> str:
    with Session(_get_engine()) as session:
        statement = select(Task).where(Task.owner_user_id == user_id).order_by(Task.id)
        tasks = list(session.exec(statement))
        if status in {"completed", "pending"}:
            desired = status == "completed"
            tasks = [task for task in tasks if task.is_completed is desired]

        if not tasks:
            return "No tasks found."

        lines = []
        for task in tasks:
            task_status = "completed" if task.is_completed else "pending"
            lines.append(f"{task.id}. {task.title} ({task_status})")
        return "\n".join(lines)


@mcp.tool()
async def complete_task(user_id: str, task_id: int) -> str:
    with Session(_get_engine()) as session:
        task = session.get(Task, task_id)
        if not task or task.owner_user_id != user_id:
            return "Task not found."
        task.is_completed = True
        session.add(task)
        session.commit()
        return f"Task '{task.title}' has been completed."


@mcp.tool()
async def delete_task(user_id: str, task_id: int) -> str:
    with Session(_get_engine()) as session:
        task = session.get(Task, task_id)
        if not task or task.owner_user_id != user_id:
            return "Task not found."
        task_title = task.title
        session.delete(task)
        session.commit()
        return f"Task '{task_title}' has been deleted."


@mcp.tool()
async def update_task(user_id: str, task_id: int, title: str | None = None, description: str | None = None) -> str:
    with Session(_get_engine()) as session:
        task = session.get(Task, task_id)
        if not task or task.owner_user_id != user_id:
            return "Task not found."
        if title is not None:
            trimmed = title.strip()
            if not trimmed:
                return "Task title cannot be empty."
            task.title = trimmed
        if description is not None:
            task.description = description
        session.add(task)
        session.commit()
        return f"Task '{task.title}' has been updated."


if __name__ == "__main__":
    mcp.run()
