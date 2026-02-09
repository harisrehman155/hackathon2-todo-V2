# Testing Guide for FastAPI

## Table of Contents
- Test Setup (Included in Production Template)
- Unit Testing
- Integration Testing
- Testing with Authentication
- Database Testing
- Testing Best Practices

## Test Setup (Production Template)

The production template includes complete pytest setup:

**pytest.ini:**
```ini
[pytest]
testpaths = tests
addopts = -v --tb=short --cov=app --cov-report=term-missing
```

**tests/conftest.py:**
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_login

# Run with verbose output
pytest -v

# Run and stop at first failure
pytest -x
```

## Unit Testing

Test individual functions in isolation:

```python
# tests/test_security.py
from app.auth.security import verify_password, get_password_hash

def test_password_hashing():
    password = "testpassword123"
    hashed = get_password_hash(password)

    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_password_hash_is_different():
    password = "testpassword123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    # Each hash should be unique (due to salt)
    assert hash1 != hash2
    # But both should verify correctly
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)
```

## Integration Testing

Test complete API endpoints:

```python
# tests/test_items.py
def test_create_and_get_item(client, auth_token):
    # Create item
    response = client.post(
        "/api/v1/items",
        json={"name": "Test Item", "price": 10.99},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    item = response.json()
    item_id = item["id"]

    # Get item
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"
```

## Testing with Authentication

### 1. Create Auth Fixture

```python
# tests/conftest.py
@pytest.fixture
def test_user(client):
    """Create a test user"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    return response.json()

@pytest.fixture
def auth_token(client, test_user):
    """Get authentication token"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    return response.json()["access_token"]
```

### 2. Use in Tests

```python
def test_protected_endpoint(client, auth_token):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_protected_endpoint_without_auth(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
```

## Database Testing

### 1. Test Database Isolation

Each test should have a clean database:

```python
@pytest.fixture
def db_session(test_db):
    """Provide transactional database session"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

### 2. Test CRUD Operations

```python
def test_create_user_in_db(db_session):
    from app.db.models import User
    from app.auth.security import get_password_hash

    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("password")
    )
    db_session.add(user)
    db_session.commit()

    # Query back
    db_user = db_session.query(User).filter(User.email == "test@example.com").first()
    assert db_user is not None
    assert db_user.username == "testuser"
```

## Parametrized Testing

Test multiple scenarios efficiently:

```python
import pytest

@pytest.mark.parametrize("email,username,password,expected_status", [
    ("valid@example.com", "validuser", "password123", 201),
    ("invalid-email", "validuser", "password123", 422),  # Invalid email
    ("valid@example.com", "ab", "password123", 422),  # Username too short
    ("valid@example.com", "validuser", "short", 422),  # Password too short
])
def test_registration_validation(client, email, username, password, expected_status):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "username": username, "password": password}
    )
    assert response.status_code == expected_status
```

## Mocking External Services

```python
from unittest.mock import patch, MagicMock

def test_send_email_on_registration(client):
    with patch('app.utils.email.send_email') as mock_send_email:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123"
            }
        )

        assert response.status_code == 201
        mock_send_email.assert_called_once()
        call_args = mock_send_email.call_args
        assert call_args[0][0] == "test@example.com"  # First argument
```

## Async Testing

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
```

## Testing Best Practices

1. **Test naming**: Use descriptive names (`test_user_can_create_item_when_authenticated`)
2. **Arrange-Act-Assert**: Structure tests clearly
3. **One assertion per test**: Makes failures easier to debug
4. **Use fixtures**: Reuse common setup code
5. **Test edge cases**: Empty inputs, invalid data, boundary values
6. **Test error handling**: Verify error responses
7. **Mock external dependencies**: Don't hit real APIs in tests
8. **Keep tests fast**: Use in-memory databases
9. **Run tests before commit**: Catch issues early
10. **Aim for high coverage**: But don't sacrifice quality for numbers
11. **Test both happy and sad paths**
12. **Use parametrize**: Test multiple scenarios efficiently

## Common Test Patterns

### Test 401 Unauthorized
```python
def test_endpoint_requires_auth(client):
    response = client.post("/api/v1/items", json={"name": "Item"})
    assert response.status_code == 401
```

### Test 404 Not Found
```python
def test_get_nonexistent_item(client):
    response = client.get("/api/v1/items/99999")
    assert response.status_code == 404
```

### Test 400 Bad Request
```python
def test_create_item_invalid_data(client, auth_token):
    response = client.post(
        "/api/v1/items",
        json={"name": ""},  # Empty name
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422
```

### Test Pagination
```python
def test_list_items_pagination(client, auth_token):
    # Create 15 items
    for i in range(15):
        client.post(
            "/api/v1/items",
            json={"name": f"Item {i}", "price": 10.0},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    # Get first page
    response = client.get("/api/v1/items?skip=0&limit=10")
    assert len(response.json()) == 10

    # Get second page
    response = client.get("/api/v1/items?skip=10&limit=10")
    assert len(response.json()) == 5
```

## Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Open in browser
open htmlcov/index.html
```

Target 80%+ coverage for production applications.
