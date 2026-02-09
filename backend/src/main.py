from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.api.routes.debug import router as debug_router
from src.db.database import init_db, make_engine
from src.api.routes.chat import router as chat_router
from src.api.routes.tasks import router as tasks_router


def create_app() -> FastAPI:
    app = FastAPI(title="Phase III Todo AI Chatbot", version="0.3.0")
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
    app.include_router(chat_router)
    app.include_router(debug_router)
    return app


app = create_app()
