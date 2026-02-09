from fastapi import APIRouter, Depends, Response
from sqlmodel import Session

from src.auth.dependencies import CurrentUser, get_current_user
from src.db.dependencies import get_session
from src.schemas.task import TaskCreate, TaskRead, TaskUpdate
from src.services.task_service import TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])
service = TaskService()


@router.get("", response_model=list[TaskRead])
def list_tasks(current_user: CurrentUser = Depends(get_current_user), session: Session = Depends(get_session)):
    return service.list_tasks(session, current_user.user_id)


@router.post("", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate, current_user: CurrentUser = Depends(get_current_user), session: Session = Depends(get_session)):
    return service.create_task(session, current_user.user_id, payload)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, current_user: CurrentUser = Depends(get_current_user), session: Session = Depends(get_session)):
    return service.get_task(session, current_user.user_id, task_id)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, current_user: CurrentUser = Depends(get_current_user), session: Session = Depends(get_session)):
    return service.update_task(session, current_user.user_id, task_id, payload)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, current_user: CurrentUser = Depends(get_current_user), session: Session = Depends(get_session)):
    service.delete_task(session, current_user.user_id, task_id)
    return Response(status_code=204)


@router.post("/{task_id}/toggle-complete", response_model=TaskRead)
def toggle_complete(task_id: int, current_user: CurrentUser = Depends(get_current_user), session: Session = Depends(get_session)):
    return service.toggle_complete(session, current_user.user_id, task_id)

