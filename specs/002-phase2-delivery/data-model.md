# Data Model: Phase 2 Delivery

**Feature:** 002-phase2-delivery

---

## Backend Task Model (unchanged from Phase 2 kickoff)

```
Task (SQLModel, table=True)
├── id: int (PK, auto-increment)
├── owner_user_id: str (indexed, FK to Better Auth user.id)
├── title: str (max 120 chars)
├── description: str? (max 500 chars)
├── is_completed: bool (default: false)
├── created_at: datetime (UTC)
└── updated_at: datetime (UTC)
```

## Better Auth Tables (auto-managed by Better Auth)

```
user
├── id: str (PK)
├── name: str
├── email: str (unique)
├── emailVerified: bool
├── image: str?
├── createdAt: datetime
└── updatedAt: datetime

session
├── id: str (PK)
├── userId: str (FK → user.id)
├── token: str (unique)
├── expiresAt: datetime
├── ipAddress: str?
├── userAgent: str?
├── createdAt: datetime
└── updatedAt: datetime

account
├── id: str (PK)
├── userId: str (FK → user.id)
├── accountId: str
├── providerId: str
├── password: str (hashed)
├── createdAt: datetime
└── updatedAt: datetime

verification
├── id: str (PK)
├── identifier: str
├── value: str
├── expiresAt: datetime
├── createdAt: datetime
└── updatedAt: datetime

jwks
├── id: str (PK)
├── publicKey: str
├── privateKey: str
├── createdAt: datetime
└── updatedAt: datetime
```

## JWT Token Payload

```json
{
  "sub": "<user.id>",
  "email": "<user.email>",
  "name": "<user.name>",
  "iss": "better-auth",
  "aud": "hackathon2",
  "iat": <unix_timestamp>,
  "exp": <unix_timestamp + 3600>
}
```

Algorithm: HS256
Shared secret: `BETTER_AUTH_SECRET` (frontend) = `JWT_SECRET` (backend)
