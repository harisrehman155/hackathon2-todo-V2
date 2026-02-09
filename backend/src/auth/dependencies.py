from dataclasses import dataclass

import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.errors import unauthorized
from src.config import Settings


security = HTTPBearer(auto_error=False)


@dataclass
class CurrentUser:
    user_id: str


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> CurrentUser:
    if not credentials:
        raise unauthorized("Missing bearer token")

    settings: Settings = request.app.state.settings
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
        )
    except jwt.PyJWTError as exc:
        raise unauthorized("Invalid token") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise unauthorized("Token missing subject")

    return CurrentUser(user_id=user_id)

