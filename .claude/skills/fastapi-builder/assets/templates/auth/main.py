from fastapi import FastAPI
from app.api.routes import items, auth
from app.db.database import engine
from app.db import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI App with Authentication",
    description="FastAPI application with JWT authentication and database integration",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(items.router, prefix="/api/v1", tags=["items"])


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Standard Template"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}
