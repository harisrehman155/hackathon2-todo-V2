---
name: fastapi-builder
description: Progressive FastAPI development skill for building REST APIs from hello world to production-ready applications. Use when the user wants to create a new FastAPI project, learn FastAPI concepts, add features to existing FastAPI apps, implement authentication, set up databases (PostgreSQL, MongoDB, SQLite), write tests, or deploy FastAPI applications. Includes 4 templates (minimal, standard, auth, production), helper scripts for project initialization and CRUD generation, and comprehensive guides for databases, authentication, testing, and deployment.
---

# FastAPI Builder

Build REST APIs with FastAPI from hello world to production-ready applications.

## When to Use This Skill

Use this skill when the user:
- Wants to create a new FastAPI project
- Needs to learn FastAPI or build their first API
- Wants to add features (database, auth, tests, Docker) to a FastAPI app
- Asks about FastAPI best practices, patterns, or architecture
- Needs help with authentication, database setup, testing, or deployment

## Progressive Learning Path

This skill follows a 4-level progression:

1. **Level 1: Minimal** - Hello world, understand basics
2. **Level 2: Standard** - Add database, CRUD operations
3. **Level 3: Auth** - Add JWT authentication
4. **Level 4: Production** - Add Docker, tests, deployment-ready

## Quick Start

### Create a New Project

Use the init_project.py script to create a project from any template:

```bash
# Level 1: Hello world
python3 scripts/init_project.py my-app --template minimal

# Level 2: With database
python3 scripts/init_project.py my-app --template standard

# Level 3: With authentication
python3 scripts/init_project.py my-app --template auth

# Level 4: Production-ready
python3 scripts/init_project.py my-app --template production
```

### Run the Project

```bash
cd my-app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
fastapi dev main.py
```

Visit http://127.0.0.1:8000/docs for interactive API documentation.

## Level 1: Minimal Template

**What's included:**
- Basic FastAPI application
- Two simple endpoints (/, /health)
- Automatic API documentation

**Files:**
- `main.py` - Application entry point
- `requirements.txt` - Dependencies

**What you'll learn:**
- FastAPI basics
- Path operations
- Automatic API docs (Swagger UI)

**Example usage:**
```python
from fastapi import FastAPI

app = FastAPI(title="My API")

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

**Next steps:** Add database integration → Use Standard template

## Level 2: Standard Template

**What's included:**
- SQLAlchemy database integration (SQLite by default)
- Complete CRUD operations for Items
- Pydantic schemas for validation
- Proper project structure

**Project structure:**
```
my-app/
├── main.py
├── requirements.txt
├── .env.example
└── app/
    ├── __init__.py
    ├── schemas.py           # Pydantic models
    ├── db/
    │   ├── database.py      # Database connection
    │   └── models.py        # SQLAlchemy models
    └── api/
        └── routes/
            └── items.py     # CRUD endpoints
```

**What you'll learn:**
- Database integration (SQLAlchemy)
- CRUD operations (Create, Read, Update, Delete)
- Request/response validation (Pydantic)
- Project organization
- Dependency injection

**Switch databases:**
- See [references/database-patterns.md](references/database-patterns.md)
- PostgreSQL, MongoDB, or async SQLAlchemy

**Generate CRUD for new models:**
```bash
python3 scripts/generate_crud.py Product --fields "name:str,price:float,stock:int"
```

**Next steps:** Add authentication → Use Auth template

## Level 3: Auth Template

**What's included:**
- Everything from Standard template
- JWT authentication
- User registration and login
- Protected endpoints
- Password hashing (bcrypt)

**New components:**
- `app/auth/security.py` - JWT and password hashing
- `app/auth/dependencies.py` - Current user dependency
- `app/api/routes/auth.py` - Auth endpoints
- User model with authentication fields

**Authentication flow:**
1. User registers: POST `/api/v1/auth/register`
2. User logs in: POST `/api/v1/auth/login` → Receives JWT token
3. User accesses protected endpoints with token in header

**What you'll learn:**
- JWT authentication
- Password hashing
- Protected routes
- OAuth2 password flow

**Example protected endpoint:**
```python
from app.auth.dependencies import get_current_active_user

@router.post("/items")
def create_item(
    item: ItemCreate,
    current_user: User = Depends(get_current_active_user)
):
    # Only authenticated users can create items
    return create_item_in_db(item)
```

**Advanced auth features:**
- See [references/auth-guide.md](references/auth-guide.md)
- Role-based access control (RBAC)
- API key authentication
- OAuth2 social login (Google, GitHub)
- Refresh tokens
- Password reset

**Next steps:** Prepare for production → Use Production template

## Level 4: Production Template

**What's included:**
- Everything from Auth template
- Docker and docker-compose
- Complete pytest test suite
- CORS configuration
- Environment configuration
- .gitignore
- Production-ready Dockerfile

**New components:**
- `Dockerfile` - Container image
- `docker-compose.yml` - Multi-container setup (app + PostgreSQL)
- `pytest.ini` - Test configuration
- `.dockerignore` - Docker build exclusions
- `tests/` - Complete test suite
  - `conftest.py` - Test fixtures
  - `test_auth.py` - Authentication tests
  - `test_items.py` - CRUD tests

**What you'll learn:**
- Docker containerization
- Testing with pytest
- Test fixtures and mocking
- Production configuration
- CORS setup

**Run with Docker:**
```bash
docker-compose up --build
```

**Run tests:**
```bash
pytest
pytest --cov=app --cov-report=html  # With coverage
```

**Deploy to cloud:**
- See [references/deployment.md](references/deployment.md)
- AWS (ECS, Elastic Beanstalk)
- Google Cloud Run
- Azure Container Apps
- Heroku

## Helper Scripts

### 1. Initialize Project (`scripts/init_project.py`)

Create a new FastAPI project from any template:

```bash
python3 scripts/init_project.py <project-name> --template <minimal|standard|auth|production>

# Examples:
python3 scripts/init_project.py blog-api --template standard
python3 scripts/init_project.py ecommerce --template production
```

### 2. Generate CRUD (`scripts/generate_crud.py`)

Generate complete CRUD endpoints for a new model:

```bash
python3 scripts/generate_crud.py <ModelName> --fields "field1:type1,field2:type2,..."

# Examples:
python3 scripts/generate_crud.py Product --fields "name:str,price:float,stock:int"
python3 scripts/generate_crud.py BlogPost --fields "title:str,content:str,published:bool"
```

The script generates:
- SQLAlchemy model code
- Pydantic schemas (Create, Update, Response)
- Complete CRUD routes
- Instructions for adding to your project

## Reference Documentation

### Database Patterns

**File:** [references/database-patterns.md](references/database-patterns.md)

**Contents:**
- SQLite, PostgreSQL, MongoDB setup
- Database migrations with Alembic
- Connection pooling
- Async database operations
- Best practices

**When to read:** Setting up or switching databases

### Authentication Guide

**File:** [references/auth-guide.md](references/auth-guide.md)

**Contents:**
- JWT authentication (included in templates)
- Role-based access control (RBAC)
- API key authentication
- OAuth2 social login (Google, GitHub)
- Refresh tokens
- Password reset flow
- Security best practices

**When to read:** Adding authentication features beyond JWT

### Testing Guide

**File:** [references/testing-guide.md](references/testing-guide.md)

**Contents:**
- Test setup (included in production template)
- Unit testing
- Integration testing
- Testing with authentication
- Database testing
- Mocking
- Coverage reports

**When to read:** Writing tests or improving test coverage

### Deployment Guide

**File:** [references/deployment.md](references/deployment.md)

**Contents:**
- Docker deployment (included in production template)
- Cloud deployment (AWS, GCP, Azure, Heroku)
- Environment configuration
- HTTPS/SSL setup
- Load balancing
- Monitoring
- Production checklist

**When to read:** Deploying to production

## Common Tasks

### Add a New Endpoint

1. Define Pydantic schema in `app/schemas.py`
2. Create SQLAlchemy model in `app/db/models.py` (if needed)
3. Add route in `app/api/routes/`
4. Include router in `main.py`

Or use the CRUD generator: `python3 scripts/generate_crud.py ModelName --fields "..."`

### Protect an Endpoint

```python
from app.auth.dependencies import get_current_active_user

@router.post("/protected")
def protected_endpoint(current_user: User = Depends(get_current_active_user)):
    return {"message": f"Hello {current_user.username}"}
```

### Switch from SQLite to PostgreSQL

1. Install driver: `pip install psycopg2-binary`
2. Update `.env`: `DATABASE_URL=postgresql://user:pass@localhost:5432/dbname`
3. No code changes needed!

See [references/database-patterns.md](references/database-patterns.md) for details.

### Add a New Model with CRUD

```bash
python3 scripts/generate_crud.py Task --fields "title:str,description:str,completed:bool"
```

Follow the printed instructions to add code to your project.

### Run Tests

```bash
pytest                                    # Run all tests
pytest tests/test_auth.py                # Run specific file
pytest --cov=app --cov-report=html       # With coverage
```

### Deploy with Docker

```bash
docker-compose up --build
```

Visit http://localhost:8000

## Template Comparison

| Feature | Minimal | Standard | Auth | Production |
|---------|---------|----------|------|------------|
| Basic API | ✓ | ✓ | ✓ | ✓ |
| Database | ✗ | ✓ (SQLite) | ✓ (SQLite) | ✓ (PostgreSQL) |
| CRUD endpoints | ✗ | ✓ | ✓ | ✓ |
| Authentication | ✗ | ✗ | ✓ (JWT) | ✓ (JWT) |
| Protected routes | ✗ | ✗ | ✓ | ✓ |
| Docker | ✗ | ✗ | ✗ | ✓ |
| Tests | ✗ | ✗ | ✗ | ✓ |
| CORS | ✗ | ✗ | ✗ | ✓ |
| Production-ready | ✗ | ✗ | ✗ | ✓ |

## Best Practices

1. **Start simple**: Begin with minimal template, add features as needed
2. **Use type hints**: FastAPI leverages Python types for validation
3. **Pydantic for schemas**: Separates validation logic from models
4. **Dependency injection**: Use Depends() for shared logic
5. **Environment variables**: Never hardcode secrets
6. **Test your code**: Use production template's test setup
7. **API versioning**: Use `/api/v1/` prefix (included in templates)
8. **Error handling**: Let FastAPI handle validation errors
9. **Documentation**: Automatic at `/docs`, keep it updated
10. **Security**: Use HTTPS, validate inputs, follow auth-guide.md

## Troubleshooting

### Import errors
- Ensure you're in the correct directory
- Check that `app/` has `__init__.py` files

### Database errors
- Check DATABASE_URL in `.env`
- Verify database is running (for PostgreSQL/MongoDB)
- Run `models.Base.metadata.create_all(bind=engine)` creates tables

### Authentication not working
- Verify SECRET_KEY is set in `.env`
- Check token format: `Authorization: Bearer <token>`
- Ensure user exists and is active

### Tests failing
- Run from project root directory
- Check test database is separate from dev database
- Verify all dependencies installed: `pip install -r requirements.txt`

## Learning Resources

- **Official FastAPI docs**: https://fastapi.tiangolo.com
- **SQLAlchemy docs**: https://docs.sqlalchemy.org
- **Pydantic docs**: https://docs.pydantic.dev
- **Pytest docs**: https://docs.pytest.org
- **Docker docs**: https://docs.docker.com

## Getting Help

When asking for help with FastAPI:

1. Specify which template you're using
2. Include relevant code snippets
3. Share error messages
4. Mention what you've already tried
5. Reference the appropriate guide (database-patterns.md, auth-guide.md, etc.)
