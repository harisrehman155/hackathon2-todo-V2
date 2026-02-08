# Authentication & Authorization Guide

## Table of Contents
- JWT Authentication (Included in Auth Template)
- OAuth2 Password Flow
- Role-Based Access Control (RBAC)
- API Key Authentication
- Social OAuth (Google, GitHub)
- Security Best Practices

## JWT Authentication (Default in Auth Template)

The auth template includes complete JWT authentication:

### Components

**1. Password Hashing (`app/auth/security.py`)**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

**2. JWT Token Creation**
```python
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

**3. Current User Dependency**
```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    username = payload.get("sub")
    user = db.query(models.User).filter(models.User.username == username).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
```

### Usage in Routes

```python
from app.auth.dependencies import get_current_active_user

@router.post("/items")
def create_item(
    item: ItemCreate,
    current_user: User = Depends(get_current_active_user)
):
    # Only authenticated users can create items
    return create_item(item)
```

## Role-Based Access Control (RBAC)

### 1. Add Roles to User Model

```python
# app/db/models.py
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String, default=UserRole.USER)  # Add role field
    is_active = Column(Boolean, default=True)
```

### 2. Create Role Checker Dependency

```python
# app/auth/dependencies.py
from fastapi import HTTPException, status

def require_role(required_role: UserRole):
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required"
            )
        return current_user
    return role_checker

# Or check multiple roles:
def require_roles(*required_roles: UserRole):
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions"
            )
        return current_user
    return role_checker
```

### 3. Protect Routes with Roles

```python
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin: User = Depends(require_role(UserRole.ADMIN))
):
    # Only admins can delete users
    pass

@router.post("/items")
def create_item(
    item: ItemCreate,
    user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MODERATOR))
):
    # Admins and moderators can create items
    pass
```

## API Key Authentication

### 1. Add API Key Model

```python
# app/db/models.py
import secrets

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    name = Column(String)  # Description of the key
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    @staticmethod
    def generate_key():
        return secrets.token_urlsafe(32)
```

### 2. Create API Key Security Scheme

```python
# app/auth/api_key.py
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db)
):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key required"
        )

    key = db.query(models.APIKey).filter(
        models.APIKey.key == api_key,
        models.APIKey.is_active == True
    ).first()

    if not key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )

    return key
```

### 3. Use API Key in Routes

```python
@router.get("/data")
def get_data(api_key: APIKey = Depends(get_api_key)):
    return {"data": "protected data", "key_name": api_key.name}
```

## OAuth2 Social Login (Google Example)

### 1. Install Dependencies

```bash
pip install authlib
pip install itsdangerous
```

### 2. Setup OAuth Client

```python
# app/auth/oauth.py
from authlib.integrations.starlette_client import OAuth
import os

oauth = OAuth()

oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
```

### 3. OAuth Routes

```python
from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter()

@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google")
async def auth_google(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')

    # Create or get user
    user = db.query(User).filter(User.email == user_info['email']).first()
    if not user:
        user = User(
            email=user_info['email'],
            username=user_info['email'].split('@')[0],
            hashed_password=""  # No password for OAuth users
        )
        db.add(user)
        db.commit()

    # Create JWT token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

## Refresh Tokens

### 1. Add Refresh Token to JWT

```python
def create_tokens(username: str):
    access_token = create_access_token(
        data={"sub": username, "type": "access"},
        expires_delta=timedelta(minutes=15)
    )
    refresh_token = create_access_token(
        data={"sub": username, "type": "refresh"},
        expires_delta=timedelta(days=7)
    )
    return {"access_token": access_token, "refresh_token": refresh_token}
```

### 2. Refresh Endpoint

```python
@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    username = payload.get("sub")
    access_token = create_access_token(data={"sub": username, "type": "access"})

    return {"access_token": access_token, "token_type": "bearer"}
```

## Security Best Practices

1. **Use HTTPS** in production (never send tokens over HTTP)
2. **Store secrets in environment** variables, never in code
3. **Use strong SECRET_KEY** (generate with `openssl rand -hex 32`)
4. **Implement rate limiting** to prevent brute force attacks
5. **Set short token expiration** times (15-30 minutes for access tokens)
6. **Use refresh tokens** for long-lived sessions
7. **Hash passwords** with bcrypt or argon2
8. **Validate email addresses** during registration
9. **Implement password requirements** (minimum length, complexity)
10. **Log authentication attempts** for security monitoring
11. **Use CORS properly** (don't allow all origins in production)
12. **Implement CSRF protection** for web applications
13. **Add email verification** for new accounts
14. **Implement password reset** functionality
15. **Consider 2FA** for sensitive applications

## Password Reset Flow

```python
# 1. Request password reset
@router.post("/password-reset/request")
def request_password_reset(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        # Generate reset token
        reset_token = create_access_token(
            data={"sub": user.email, "type": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        # Send email with reset link (implement email service)
        # send_email(email, f"Reset link: /reset?token={reset_token}")

    return {"message": "If email exists, reset link sent"}

# 2. Reset password
@router.post("/password-reset/confirm")
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    if not payload or payload.get("type") != "password_reset":
        raise HTTPException(status_code=400, detail="Invalid token")

    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if user:
        user.hashed_password = get_password_hash(new_password)
        db.commit()

    return {"message": "Password reset successful"}
```
