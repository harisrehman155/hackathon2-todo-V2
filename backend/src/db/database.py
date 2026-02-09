from sqlmodel import SQLModel, create_engine

from src.config import Settings


def make_engine(settings: Settings):
    connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
    return create_engine(settings.database_url, echo=False, connect_args=connect_args)


def init_db(engine) -> None:
    SQLModel.metadata.create_all(engine)

