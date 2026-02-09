from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.db.database import init_db, make_engine
from src.api.routes.tasks import router as tasks_router


def create_app() -> FastAPI:
    app = FastAPI(title="Phase II Todo Web API", version="0.2.0")
    settings = get_settings()
    engine = make_engine(settings)
    init_db(engine)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    app.state.settings = settings
    app.state.engine = engine
    app.include_router(tasks_router)
    return app


app = create_app()

