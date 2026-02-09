from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session, select

from src.api.errors import not_found
from src.db.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def list_tasks(self, session: Session, owner_user_id: str) -> list[Task]:
        statement = select(Task).where(Task.owner_user_id == owner_user_id).order_by(Task.id)
        return list(session.exec(statement))

    def create_task(self, session: Session, owner_user_id: str, payload: TaskCreate) -> Task:
        task = Task(owner_user_id=owner_user_id, title=payload.title, description=payload.description)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    def get_task(self, session: Session, owner_user_id: str, task_id: int) -> Task:
        task = session.get(Task, task_id)
        if not task or task.owner_user_id != owner_user_id:
            raise not_found()
        return task

    def update_task(self, session: Session, owner_user_id: str, task_id: int, payload: TaskUpdate) -> Task:
        task = self.get_task(session, owner_user_id, task_id)
        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(task, key, value)
        task.updated_at = datetime.now(task.updated_at.tzinfo)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    def delete_task(self, session: Session, owner_user_id: str, task_id: int) -> None:
        task = self.get_task(session, owner_user_id, task_id)
        session.delete(task)
        session.commit()

    def toggle_complete(self, session: Session, owner_user_id: str, task_id: int) -> Task:
        task = self.get_task(session, owner_user_id, task_id)
        task.is_completed = not task.is_completed
        task.updated_at = datetime.now(task.updated_at.tzinfo)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

