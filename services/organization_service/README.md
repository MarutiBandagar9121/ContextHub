# Organization Service

Owns organizations, memberships, and roles for the ContextHub platform. It never queries `auth_service`'s database directly — it trusts user identity from a JWT verified locally, and stores any reference to a user (`owner_id`, `user_id`) as a plain indexed column, not a database-level foreign key. See [Cross-Service Authentication](../../CLAUDE.md#cross-service-authentication) in the root `CLAUDE.md` for the full reasoning.

## Current status

Scaffolded, not yet feature-complete:
- FastAPI app with DB connectivity check on startup
- SQLAlchemy models: `Organization`, `OrganizationMembership` (Alembic migrations wired up)
- `POST /api/v1/organizations` route stubbed (schema defined, body unimplemented)
- JWT verification (`get_current_user` in `dependencies/user.py`) stubbed, not wired to RS256 yet

Not implemented yet: actually creating an org + owner membership row, listing orgs visible to the current user, JWT verification logic, member invitations, role management.

## Architectural decisions

- **No cross-database foreign keys**: `Organization.owner_id` and `OrganizationMembership.user_id` are plain `Integer` columns referencing `auth_service`'s `users` table by id only — never a SQLAlchemy `ForeignKey`, since that table lives in a separate database this service can't reach.
- **Owner is also a membership row**: creating an org will insert both the `organizations` row and an `organization_memberships` row (`role=OWNER`) for the creator in the same transaction. This means "which orgs can this user see" is always one query against `organization_memberships` — never an `OR owner_id = ?` special case.
- **Identity never comes from the request body**: `owner_id`/`user_id` are derived from the verified JWT's `sub` claim, never accepted as a client-supplied field — otherwise any authenticated user could create an org owned by someone else.
- **JWT verification only, no signing**: this service holds only `auth_service`'s public key (`keys/jwt_public.pem`) and verifies `RS256`-signed tokens. It cannot mint tokens and never calls `auth_service` to validate or refresh one — an expired/invalid token just gets a `401`; refreshing is strictly a client ↔ `auth_service` concern.

## Prerequisites

- Python 3.13
- Poetry 2.x
- A running PostgreSQL instance with a database for this service (e.g. `organization_db`)
- `auth_service`'s public key, copied into `keys/jwt_public.pem` (see [keys/README.md](keys/README.md))

## Setup

```bash
cd services/organization_service
poetry config virtualenvs.in-project true   # if not already set globally
poetry install
cp .env.example .env
```

Copy the public key from `auth_service` (see [keys/README.md](keys/README.md)):

```bash
cp ../auth_service/keys/jwt_public.pem keys/jwt_public.pem
```

Edit `.env` and set:
- `DATABASE_URL` — must point at a Postgres database you've already created (e.g. `postgresql://user:password@localhost:5432/organization_db`)
- `JWT_PUBLIC_KEY_PATH` — path to the public key copied above (e.g. `keys/jwt_public.pem`)
- `JWT_ALGORITHM` — `RS256`

## Running

```bash
uvicorn organization_service.main:app --reload --app-dir src
```

## Project structure

```
src/organization_service/
  main.py                          # FastAPI app + startup DB check
  config/settings.py               # env-driven settings (pydantic-settings)
  api/v1/router.py                 # router aggregation
  api/v1/organization_routes.py    # organization HTTP routes
  schemas/organization_schema.py   # pydantic request/response models
  db/base.py, db/session.py        # SQLAlchemy base, engine, session factory
  dependencies/db.py               # get_db() FastAPI dependency
  dependencies/user.py             # get_current_user() — JWT verification dependency
  models/                          # SQLAlchemy ORM models (Organization, OrganizationMembership)
  const/                           # shared enums (OrganizationRoleEnum)
```
