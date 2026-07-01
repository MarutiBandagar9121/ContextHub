# Organization Service

Owns organizations, memberships, and invitations for the ContextHub platform. It never queries `auth_service`'s database directly — it trusts user identity from a JWT verified locally, and stores any reference to a user (`owner_id`, `user_id`) as a plain indexed column, not a database-level foreign key. See [Cross-Service Authentication](../../CLAUDE.md#cross-service-authentication) in the root `CLAUDE.md` for the full reasoning.

## Current status

Functional:
- Organization CRUD (create, list, get with member details, soft-delete)
- Member invitation flow — send invite, check invite status (resolves whether invited email already has an account), accept invite (handles new and existing users)
- Cross-service HTTP client to `auth_service` for user lookups
- JWT verification using `auth_service`'s RS256 public key
- Alembic migrations fully wired

Not implemented yet: role management beyond OWNER/ADMIN/MEMBER, member removal, org settings.

## Endpoints

All routes under `/api/v1/organization`. All require a valid Bearer access token unless noted.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/` | Create a new organization; caller becomes OWNER |
| `GET` | `/` | List all organizations the current user belongs to |
| `GET` | `/{org_id}` | Full org details with all members and their roles |
| `DELETE` | `/{org_id}` | Soft-delete an organization (owner only) |
| `POST` | `/invitation` | Send an invitation by email (ADMIN/OWNER only) |
| `GET` | `/invitation/{token}` | Check invitation status — resolves whether the invited email has an account |
| `POST` | `/invitation/{token}/accept` | Accept an invitation (registers new user or links existing, adds membership row) |

## Architectural decisions

- **No cross-database foreign keys**: `Organization.owner_id` and `OrganizationMembership.user_id` are plain `Integer` columns — never a SQLAlchemy `ForeignKey` into `auth_service`'s database.
- **Owner is also a membership row**: creating an org inserts both the `organizations` row and an `organization_memberships` row (`role=OWNER`) in one transaction. "Which orgs can this user see" is always a single query against `organization_memberships`.
- **Identity from JWT only**: `owner_id`/`user_id` are always derived from the verified JWT's `sub` claim, never accepted as a client-supplied field.
- **JWT verification only, no signing**: this service holds only `auth_service`'s public key (`keys/jwt_public.pem`) and verifies RS256 tokens. Expired/invalid token → `401`; refreshing is the client's responsibility.
- **Invitation status is lazily resolved**: `GET /invitation/{token}` calls `auth_service` to check whether the invited email has an account. The result (`is_new_user`, `invited_user_id`) is persisted on the invitation record so subsequent calls don't always need the cross-service lookup.

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

Copy the public key from `auth_service`:

```bash
cp ../auth_service/keys/jwt_public.pem keys/jwt_public.pem
```

Edit `.env` and set:
- `DATABASE_URL` — e.g. `postgresql://user:password@localhost:5432/organization_db`
- `JWT_PUBLIC_KEY_PATH` — e.g. `keys/jwt_public.pem`
- `JWT_ALGORITHM` — `RS256`
- `AUTH_SERVICE_INTERNAL_URL` — base URL of the running auth service (e.g. `http://localhost:8000`)

## Running

```bash
uvicorn organization_service.main:app --reload --app-dir src
```

Runs on `http://localhost:8001` by default.

## Project structure

```
src/organization_service/
  main.py                          # FastAPI app + startup DB check
  config/settings.py               # env-driven settings (pydantic-settings)
  api/v1/router.py                 # router aggregation
  api/v1/organization_routes.py    # organization HTTP routes
  services/organization_service.py # business logic
  schemas/organization_schema.py   # pydantic request/response models
  http_clients/
    base_client.py                 # shared httpx async base
    user_service_client.py         # calls auth_service internal endpoints
  db/base.py, db/session.py        # SQLAlchemy base, engine, session factory
  dependencies/db.py               # get_db() FastAPI dependency
  dependencies/user.py             # get_current_user_id() — JWT verification
  models/                          # Organization, OrganizationMembership, OrganizationInvitations
  const/                           # enums (OrganizationRoleEnum, OrganizationInvitationStatusEnum)
  alembic/versions/                # DB migrations
```
