# Auth Service

Handles user authentication for the ContextHub platform. Other services will eventually call this service (or validate its tokens) rather than implementing their own auth.

## Current status

Core auth flow is functional. Implemented so far:
- FastAPI app with a `/api/v1/health` endpoint
- DB connectivity check on startup (via SQLAlchemy)
- SQLAlchemy models: `User`, `Organization`, `OrganizationMembership`, `Otp`, `RefreshToken` (Alembic migrations wired up)
- Registration with email OTP verification, login, refresh, logout (see [Endpoints](#endpoints) and [Architectural decisions](#architectural-decisions) below)

Not implemented yet: password reset, OAuth, RBAC/permissions, actually sending OTP emails (notification service isn't wired up — OTPs are just persisted to the DB for now).

## Endpoints

Public — `/api/v1/auth`:

- `POST /register` — create a user (or re-issue an OTP for an existing, unverified one) and send an email-verification OTP
- `POST /verify_otp` — verify the OTP, mark the user verified, issue an access token + refresh token cookie
- `POST /resend_otp` — re-issue an OTP for an unverified user; does not issue any tokens, since the user hasn't proven anything yet at this point — only `verify_otp` does that
- `POST /login` — email + password login, issues an access token + refresh token cookie
- `POST /refresh` — exchange the refresh token cookie for a new access token (rotates the refresh token)
- `POST /logout` — revoke the refresh token cookie's DB record and clear the cookie

Internal — `/internal/api/v1/user` (service-to-service only, no user JWT):

- `POST /batch` — fetch multiple users by a list of IDs; used by `organization_service` to hydrate member lists
- `GET /?email=<email>` — fetch a single user by email address; returns 404 if not found; used by `organization_service` to resolve whether an invited email already has an account
- `POST /register` — register a user via an organization invitation (invitation-based sign-up flow)

## Architectural decisions

- **Access tokens**: short-lived JWTs (`ACCESS_TOKEN_EXPIRE_MINUTES`, default 30 min), returned in the response body. Intended to be kept in client memory only (not `localStorage`) since this is a browser-only client — minimizes the XSS exposure window.
- **Signed with RS256, not a shared secret**: this service holds the private key (`keys/jwt_private.pem`) and is the only one that ever signs a token. Other services verify using only the public key — they can check a token's validity but can never forge one. See [keys/README.md](keys/README.md).
- **Refresh tokens**: opaque, long-lived (`REFRESH_TOKEN_EXPIRE_DAYS`, default 7 days), stored hashed (SHA-256, not bcrypt — lookups need a deterministic hash) in the `refresh_tokens` table. Never returned in a response body; transported only via an `httpOnly`, `Secure`, `SameSite=Lax` cookie (`refresh_token`) so XSS can't read it. The `COOKIE_SECURE` setting controls the `Secure` flag — set it to `false` in `.env` for local HTTP development, since browsers drop `Secure` cookies sent over plain `http://`.
- **One active refresh token per user**: every place that issues a refresh token (`/login`, `/verify_otp`, `/resend_otp`, `/refresh`) first revokes (`revoked_at`) any of the user's previously active refresh tokens. `/refresh` also rotates the token on every call (old one revoked, new one issued) rather than reusing the same one for its whole lifetime.
- **Logout is lenient**: if the refresh-token cookie is missing or already invalid, `/logout` still succeeds (just clears the cookie) — the goal is "client ends up logged out," not validating what they sent.
- **OTPs**: 10-minute expiry, typed via `OtpTypesEnum` (currently just `EMAIL_VERIFICATION`). On resend, the previous unused OTP is soft-invalidated (`expires_at` set to now) rather than deleted, to keep a row for audit/abuse-tracking purposes.

## Prerequisites

- Python 3.13
- Poetry 2.x
- A running PostgreSQL instance with a database for this service (e.g. `auth_db`)

## Setup

```bash
cd services/auth_service
poetry config virtualenvs.in-project true   # if not already set globally
poetry install
cp .env.example .env
```

Generate the RS256 keypair used to sign access tokens (see [keys/README.md](keys/README.md) for details and key rotation notes):

```bash
openssl genrsa -out keys/jwt_private.pem 2048
openssl rsa -in keys/jwt_private.pem -pubout -out keys/jwt_public.pem
```

Copy `keys/jwt_public.pem` into every other service that needs to verify this service's tokens (e.g. `services/organization_service/keys/jwt_public.pem`).

Edit `.env` and set:
- `DATABASE_URL` — must point at a Postgres database you've already created (e.g. `postgresql://user:password@localhost:5432/auth_db`)
- `JWT_PRIVATE_KEY_PATH` / `JWT_PUBLIC_KEY_PATH` — paths to the keys generated above (e.g. `keys/jwt_private.pem`, `keys/jwt_public.pem`)
- `JWT_ALGORITHM` — `RS256`

## Running

```bash
uvicorn auth_service.main:app --reload --app-dir src
```

Then check `http://127.0.0.1:8000/api/v1/health`.

## Project structure

```
src/auth_service/
  main.py                      # FastAPI app + startup DB check
  config/settings.py           # env-driven settings (pydantic-settings)
  api/v1/router.py             # router aggregation
  api/v1/auth.py                # auth HTTP routes (register/verify_otp/resend_otp/login/refresh/logout)
  services/user_serivice.py     # auth business logic
  schemas/user_schema.py        # pydantic request/response models
  db/base.py, db/session.py     # SQLAlchemy base, engine, session factory
  dependencies/db.py            # get_db() FastAPI dependency
  models/                       # SQLAlchemy ORM models (User, Otp, RefreshToken, Organization, ...)
  const/                        # shared enums
  utils/security.py             # password hashing, refresh-token hashing
  utils/jwt.py                  # JWT creation/decoding
  utils/cookies.py               # refresh-token cookie helpers
  utils/otp.py                   # OTP code generation
```
