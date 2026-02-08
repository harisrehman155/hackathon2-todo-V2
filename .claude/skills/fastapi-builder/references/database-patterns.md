# Database Patterns for FastAPI

## Table of Contents
- SQLAlchemy with SQLite (Default)
- PostgreSQL Setup
- MongoDB Setup
- Database Migrations with Alembic
- Connection Pooling
- Async Database Operations

## SQLAlchemy with SQLite (Default)

All templates use SQLite by default for quick setup:

```python
# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## PostgreSQL Setup

### 1. Install Driver

```bash
pip install psycopg2-binary
# or for production:
pip install psycopg2
```

### 2. Update Database URL

```python
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)  # No check_same_thread for PostgreSQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### 3. Docker PostgreSQL

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=myuser
      - POSTGRES_PASSWORD=mypassword
      - POSTGRES_DB=mydb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## MongoDB Setup

### 1. Install Driver

```bash
pip install motor  # Async MongoDB driver
# or
pip install pymongo  # Sync MongoDB driver
```

### 2. Setup MongoDB Connection

```python
# app/db/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("MONGODB_DB", "mydatabase")

class MongoDB:
    client: AsyncIOMotorClient = None

mongodb = MongoDB()

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(MONGODB_URL)

async def close_mongo_connection():
    mongodb.client.close()

def get_database():
    return mongodb.client[DATABASE_NAME]
```

### 3. MongoDB Models (Pydantic only)

```python
# app/models/user.py
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    email: str
    username: str
    is_active: bool = True

    class Config:
        json_encoders = {ObjectId: str}
```

### 4. MongoDB CRUD Operations

```python
# app/api/routes/users.py (MongoDB)
from fastapi import APIRouter, HTTPException
from app.db.mongodb import get_database

router = APIRouter()

@router.post("/users")
async def create_user(user: UserModel):
    db = get_database()
    result = await db.users.insert_one(user.dict(exclude={"id"}))
    user.id = result.inserted_id
    return user

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    db = get_database()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Database Migrations with Alembic

### 1. Install Alembic

```bash
pip install alembic
```

### 2. Initialize Alembic

```bash
alembic init alembic
```

### 3. Configure Alembic

```python
# alembic/env.py
from app.db.database import Base
from app.db.models import *  # Import all models

target_metadata = Base.metadata
```

```python
# alembic.ini
sqlalchemy.url = postgresql://user:password@localhost:5432/dbname
# or use environment variable in env.py:
# config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
```

### 4. Create Migrations

```bash
# Auto-generate migration
alembic revision --autogenerate -m "Add users table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Connection Pooling

### SQLAlchemy Connection Pool

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,          # Number of connections to keep open
    max_overflow=10,      # Max connections to create beyond pool_size
    pool_timeout=30,      # Timeout for getting a connection from pool
    pool_recycle=3600,    # Recycle connections after 1 hour
    pool_pre_ping=True    # Verify connections before using
)
```

## Async Database Operations

### 1. Install Async SQLAlchemy

```bash
pip install sqlalchemy[asyncio]
pip install asyncpg  # For PostgreSQL
```

### 2. Async Database Setup

```python
# app/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### 3. Async Routes

```python
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

@router.get("/items")
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Item))
    items = result.scalars().all()
    return items

@router.post("/items")
async def create_item(item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
```

## Best Practices

1. **Use environment variables** for database URLs
2. **Never commit** credentials to version control
3. **Use connection pooling** for better performance
4. **Implement database migrations** for schema changes
5. **Handle connection errors** gracefully
6. **Use transactions** for multi-step operations
7. **Close connections** properly (use context managers)
8. **Index frequently queried** columns
9. **Use async** for high-concurrency applications
10. **Monitor database** performance in production
