from src.cli.commands import run_command
from src.services.task_service import TaskService


def test_add_command_returns_confirmation_with_new_id() -> None:
    service = TaskService()
    output = run_command(["add", "--title", "Buy milk"], service)
    assert "created task #1" in output.lower()
    assert "buy milk" in output.lower()


def test_list_command_returns_created_task_summary() -> None:
    service = TaskService()
    run_command(["add", "--title", "Pay bills"], service)
    output = run_command(["list"], service)
    assert "#1" in output
    assert "Pay bills" in output
    assert "pending" in output.lower()


def test_update_command_changes_existing_task() -> None:
    service = TaskService()
    run_command(["add", "--title", "Draft"], service)
    output = run_command(
        ["update", "--id", "1", "--title", "Final", "--description", "done"], service
    )
    assert "updated task #1" in output.lower()
    listing = run_command(["list"], service)
    assert "Final" in listing


def test_complete_and_uncomplete_commands_toggle_status() -> None:
    service = TaskService()
    run_command(["add", "--title", "Toggle me"], service)
    complete_output = run_command(["complete", "--id", "1"], service)
    assert "marked complete" in complete_output.lower()
    assert "[complete]" in run_command(["list"], service).lower()
    uncomplete_output = run_command(["uncomplete", "--id", "1"], service)
    assert "marked pending" in uncomplete_output.lower()
    assert "[pending]" in run_command(["list"], service).lower()


def test_delete_command_removes_task() -> None:
    service = TaskService()
    run_command(["add", "--title", "Delete me"], service)
    output = run_command(["delete", "--id", "1"], service)
    assert "deleted task #1" in output.lower()
    assert (
        "No tasks found. Use 'add --title <text>' to create your first task."
        == run_command(["list"], service)
    )


def test_unknown_task_id_returns_clear_error_message() -> None:
    service = TaskService()
    output = run_command(["delete", "--id", "999"], service)
    assert "not found" in output.lower()


def test_list_empty_state_message_is_explicit() -> None:
    service = TaskService()
    output = run_command(["list"], service)
    assert output == "No tasks found. Use 'add --title <text>' to create your first task."


def test_list_mixed_state_uses_consistent_status_labels() -> None:
    service = TaskService()
    run_command(["add", "--title", "Pending task"], service)
    run_command(["add", "--title", "Done task"], service)
    run_command(["complete", "--id", "2"], service)
    output = run_command(["list"], service)
    assert "#1 [PENDING] Pending task" in output
    assert "#2 [COMPLETE] Done task" in output
