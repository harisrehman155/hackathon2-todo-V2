import os
from pathlib import Path

import jwt
import pytest
from fastapi.testclient import TestClient

from src.main import create_app

TEST_JWT_SECRET = "test-secret-key-with-32-plus-chars"


@pytest.fixture
def client(tmp_path: Path):
    db_path = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path.as_posix()}"
    os.environ["JWT_SECRET"] = TEST_JWT_SECRET
    os.environ["JWT_ALGORITHM"] = "HS256"
    os.environ["JWT_AUDIENCE"] = "hackathon2"
    os.environ["JWT_ISSUER"] = "better-auth"

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_header() -> dict[str, str]:
    token = jwt.encode(
        {"sub": "user-a", "aud": "hackathon2", "iss": "better-auth"},
        TEST_JWT_SECRET,
        algorithm="HS256",
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_auth_header() -> dict[str, str]:
    token = jwt.encode(
        {"sub": "user-b", "aud": "hackathon2", "iss": "better-auth"},
        TEST_JWT_SECRET,
        algorithm="HS256",
    )
    return {"Authorization": f"Bearer {token}"}
