from __future__ import annotations

import argparse
from typing import Sequence

from src.lib.errors import TaskError, ValidationError
from src.services.task_service import TaskService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add")
    add.add_argument("--title", required=True)
    add.add_argument("--description")

    subparsers.add_parser("list")

    update = subparsers.add_parser("update")
    update.add_argument("--id", type=int, required=True)
    update.add_argument("--title")
    update.add_argument("--description")

    complete = subparsers.add_parser("complete")
    complete.add_argument("--id", type=int, required=True)

    uncomplete = subparsers.add_parser("uncomplete")
    uncomplete.add_argument("--id", type=int, required=True)

    delete = subparsers.add_parser("delete")
    delete.add_argument("--id", type=int, required=True)
    return parser


def run_command(argv: Sequence[str], service: TaskService) -> str:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "add":
            task = service.create_task(title=args.title, description=args.description)
            return f"Created task #{task.id}: {task.title} (pending)"

        if args.command == "list":
            tasks = service.list_tasks()
            if not tasks:
                return "No tasks found. Use 'add --title <text>' to create your first task."
            return "\n".join(
                f"#{task['id']} [{str(task['status']).upper()}] {task['title']}"
                for task in tasks
            )

        if args.command == "update":
            if args.title is None and args.description is None:
                raise ValidationError("Provide at least one field to update.")
            task = service.update_task(
                args.id, title=args.title, description=args.description
            )
            return f"Updated task #{task.id}: {task.title}"

        if args.command == "complete":
            task = service.complete_task(args.id)
            return f"Marked complete task #{task.id}."

        if args.command == "uncomplete":
            task = service.uncomplete_task(args.id)
            return f"Marked pending task #{task.id}."

        if args.command == "delete":
            task = service.delete_task(args.id)
            return f"Deleted task #{task.id}."

        return f"Command '{args.command}' not implemented."
    except TaskError as exc:
        return f"Error: {exc}"
