# ContextHub

A multi-tenant, AI-powered RAG (Retrieval Augmented Generation) platform. Users sign up, create organizations, invite teammates, build knowledge bases from uploaded documents, and query those knowledge bases for AI-generated, context-grounded answers.

Built as a **microservices monorepo** to explore service isolation, domain-driven boundaries, and production-grade backend architecture. See [CLAUDE.md](CLAUDE.md) for the full planned service breakdown (auth, organization, knowledge base, ingestion, query, billing, notification, API gateway).

---

## Status

| Component | Status |
|---|---|
| `auth_service` | Functional — registration, OTP, login, refresh, logout |
| `organization_service` | Functional — orgs, memberships, invitations, accept flow |
| `frontend` | Scaffolded — auth flow, dashboard, organization pages wired |
| All other services | Planned, not started |

---

## Monorepo layout

```
services/
  auth_service/          # user auth (register, OTP, login, refresh, logout)
  organization_service/  # orgs, memberships, invitations
frontend/                # React 18 + Vite SPA
bruno/                   # Bruno API test collections
```

Each backend service is an independently installable Python package (own `pyproject.toml`, own `.venv`) with its own README for service-specific details (env vars, run commands, endpoints).

---

## API reference

### Auth Service — `http://localhost:8000`

Public endpoints (`/api/v1/auth`):

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/auth/register` | Register a user; sends email-verification OTP |
| `POST` | `/api/v1/auth/verify_otp` | Verify OTP, mark user verified, issue access token + refresh cookie |
| `POST` | `/api/v1/auth/resend_otp` | Re-issue OTP for an unverified user |
| `POST` | `/api/v1/auth/login` | Email + password login; issues access token + refresh cookie |
| `POST` | `/api/v1/auth/logout` | Revoke refresh token and clear cookie |
| `POST` | `/api/v1/auth/refresh` | Exchange refresh cookie for a new access token (rotates token) |

Internal endpoints (`/internal/api/v1/user`) — service-to-service only, no user JWT required:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/internal/api/v1/user/batch` | Fetch multiple users by a list of IDs |
| `GET`  | `/internal/api/v1/user?email=...` | Fetch a single user by email address |
| `POST` | `/internal/api/v1/user/register` | Register a user via invitation (invitation-based sign-up) |

---

### Organization Service — `http://localhost:8001`

All routes require a valid Bearer access token unless noted.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/organization` | Create a new organization (caller becomes OWNER) |
| `GET` | `/api/v1/organization` | List all organizations the current user belongs to |
| `GET` | `/api/v1/organization/{org_id}` | Get full org details including all members and their roles |
| `DELETE` | `/api/v1/organization/{org_id}` | Soft-delete an organization (owner only) |
| `POST` | `/api/v1/organization/invitation` | Send an invitation to a user by email (ADMIN/OWNER only) |
| `GET` | `/api/v1/organization/invitation/{token}` | Check invitation status — resolves whether the invited email has an account |
| `POST` | `/api/v1/organization/invitation/{token}/accept` | Accept an invitation (registers user if new, adds to org membership) |

---

## Frontend

React 18 SPA located in `frontend/`. Built with Vite, Tailwind CSS, React Router v6, TanStack Query v5, Zustand, and Axios.

### Pages / client-side routes

| Path | Page | Notes |
|------|------|-------|
| `/login` | Login | Public |
| `/register` | Register | Public |
| `/verify-otp` | OTP verification | Public; redirects from register |
| `/invite/:token` | Invitation accept | Standalone page (no app shell); handles new and existing users |
| `/dashboard` | Dashboard | Protected |
| `/organization/:orgId` | Organization overview | Protected |
| `/organization/:orgId/members` | Members list | Protected |
| `/organization/:orgId/invite` | Send invitation | Protected |
| `/organization/:orgId/knowledge` | Knowledge base | Protected (stub) |

---

## Prerequisites

- Python 3.13
- [Poetry](https://python-poetry.org/) 2.x
- PostgreSQL (running locally)
- Node.js 18+ / npm (for the frontend)

---

## Dev environment setup

### Backend (one-time)

```bash
poetry config virtualenvs.in-project true
```

This makes Poetry create each service's virtualenv inside that service's own folder.

### Auth Service

```bash
cd services/auth_service
poetry install
cp .env.example .env
# generate RS256 keypair
openssl genrsa -out keys/jwt_private.pem 2048
openssl rsa -in keys/jwt_private.pem -pubout -out keys/jwt_public.pem
# copy public key to org service
cp keys/jwt_public.pem ../organization_service/keys/jwt_public.pem
# edit .env: DATABASE_URL, JWT_PRIVATE_KEY_PATH, JWT_PUBLIC_KEY_PATH, JWT_ALGORITHM=RS256
uvicorn auth_service.main:app --reload --app-dir src --port 8000
```

### Organization Service

```bash
cd services/organization_service
poetry install
cp .env.example .env
# edit .env: DATABASE_URL, JWT_PUBLIC_KEY_PATH, JWT_ALGORITHM=RS256, AUTH_SERVICE_INTERNAL_URL
uvicorn organization_service.main:app --reload --app-dir src --port 8001
```

See each service's README for full env var details.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:5173` by default.
