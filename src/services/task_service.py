from __future__ import annotations

from src.lib.errors import TaskNotFoundError
from src.lib.validators import validate_description, validate_title
from src.models.task import Task, TaskStatus, utc_now_iso


class TaskService:
    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id = 1

    def _get_task(self, task_id: int) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"Task with id {task_id} was not found.")

    def create_task(self, title: str, description: str | None = None) -> Task:
        task = Task(
            id=self._next_id,
            title=validate_title(title),
            description=validate_description(description),
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self) -> list[dict[str, str | int]]:
        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description or "",
                "status": task.status.value,
            }
            for task in self._tasks
        ]

    def update_task(
        self, task_id: int, title: str | None = None, description: str | None = None
    ) -> Task:
        task = self._get_task(task_id)
        if title is not None:
            task.title = validate_title(title)
        if description is not None:
            task.description = validate_description(description)
        task.updated_at = utc_now_iso()
        return task

    def complete_task(self, task_id: int) -> Task:
        task = self._get_task(task_id)
        task.status = TaskStatus.COMPLETE
        task.updated_at = utc_now_iso()
        return task

    def uncomplete_task(self, task_id: int) -> Task:
        task = self._get_task(task_id)
        task.status = TaskStatus.PENDING
        task.updated_at = utc_now_iso()
        return task

    def delete_task(self, task_id: int) -> Task:
        task = self._get_task(task_id)
        self._tasks = [item for item in self._tasks if item.id != task_id]
        return task
