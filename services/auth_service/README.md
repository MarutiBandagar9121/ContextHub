# Auth Service

Handles user authentication for the ContextHub platform. Other services will eventually call this service (or validate its tokens) rather than implementing their own auth.

## Current status

Skeleton only — not yet functional auth. Implemented so far:
- FastAPI app with a `/api/v1/health` endpoint
- DB connectivity check on startup (via SQLAlchemy)
- SQLAlchemy models: `User`, `Organization`, `OrganizationMembership` (no migrations generated yet — Alembic is installed but not initialized)

Not implemented yet: signup, signin, OTP verification, JWT issuance, password reset.

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

Edit `.env` and set:
- `DATABASE_URL` — must point at a Postgres database you've already created (e.g. `postgresql://user:password@localhost:5432/auth_db`)
- `JWT_SECRET_KEY` — any secret string for now

## Running

```bash
uvicorn auth_service.main:app --reload --app-dir src
```

Then check `http://127.0.0.1:8000/api/v1/health`.

## Project structure

```
src/auth_service/
  main.py                  # FastAPI app + startup DB check
  config/settings.py        # env-driven settings (pydantic-settings)
  api/v1/router.py           # HTTP routes
  db/base.py, db/session.py  # SQLAlchemy base, engine, session factory
  dependencies/db.py          # get_db() FastAPI dependency
  models/                      # SQLAlchemy ORM models
  const/                        # shared enums
```
