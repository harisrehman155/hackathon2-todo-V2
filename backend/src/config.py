from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

_env_file = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(_env_file)


@dataclass(frozen=True)
class Settings:
    database_url: str
    openai_api_key: str
    app_env: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_audience: str
    jwt_issuer: str
    cors_origins: list[str]


def get_settings() -> Settings:
    origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    return Settings(
        database_url=os.getenv("DATABASE_URL", "sqlite:///./backend.db"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        app_env=os.getenv("APP_ENV", "development"),
        jwt_secret=os.getenv("JWT_SECRET", "dev-secret"),
        jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        jwt_audience=os.getenv("JWT_AUDIENCE", "hackathon2"),
        jwt_issuer=os.getenv("JWT_ISSUER", "better-auth"),
        cors_origins=[o.strip() for o in origins.split(",")],
    )
