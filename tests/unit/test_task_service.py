from src.services.task_service import TaskService


def test_create_task_assigns_incremental_id_and_pending_status() -> None:
    service = TaskService()
    task = service.create_task(title="Write tests", description="Start with red")
    assert task.id == 1
    assert task.title == "Write tests"
    assert task.description == "Start with red"
    assert task.status.value == "pending"


def test_list_tasks_returns_created_tasks_in_id_order() -> None:
    service = TaskService()
    service.create_task(title="B task")
    service.create_task(title="A task")
    rows = service.list_tasks()
    assert [row["id"] for row in rows] == [1, 2]
    assert rows[0]["title"] == "B task"
    assert rows[0]["status"] == "pending"


def test_update_task_changes_title_and_description() -> None:
    service = TaskService()
    task = service.create_task("Old", "Old description")
    updated = service.update_task(task.id, title="New", description="New description")
    assert updated.title == "New"
    assert updated.description == "New description"


def test_complete_and_uncomplete_transitions_status() -> None:
    service = TaskService()
    task = service.create_task("Status")
    service.complete_task(task.id)
    assert service.list_tasks()[0]["status"] == "complete"
    service.uncomplete_task(task.id)
    assert service.list_tasks()[0]["status"] == "pending"


def test_delete_task_removes_target_task() -> None:
    service = TaskService()
    first = service.create_task("First")
    service.create_task("Second")
    service.delete_task(first.id)
    rows = service.list_tasks()
    assert len(rows) == 1
    assert rows[0]["title"] == "Second"
