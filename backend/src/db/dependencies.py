from fastapi import Request
from sqlmodel import Session


def get_session(request: Request):
    with Session(request.app.state.engine) as session:
        yield session

