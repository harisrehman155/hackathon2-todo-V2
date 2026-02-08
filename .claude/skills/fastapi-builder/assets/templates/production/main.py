from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import items, auth
from app.db.database import engine
from app.db import models
import os

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Production App",
    description="Production-ready FastAPI application with authentication, testing, and Docker support",
    version="1.0.0"
)

# CORS middleware configuration
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
