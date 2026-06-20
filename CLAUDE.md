# AI.md

## Project Overview

This project is a multi-tenant AI-powered RAG (Retrieval Augmented Generation) platform built using a microservices architecture.

Users can:

- Register and authenticate
- Create organizations/workspaces
- Invite members into organizations
- Create and manage knowledge bases
- Upload and process documents
- Query their organization-specific knowledge bases using AI
- Receive contextual AI-generated answers grounded in uploaded data

The system is designed with scalability, service isolation, and production-grade architecture in mind.

---

# Core Architecture

The project follows:

- Microservices architecture
- Domain-driven service separation
- Monorepo structure
- API-first development
- Containerized deployment
- Event-driven extensibility (future)

---

# High-Level Services

## 1. Auth Service

Responsibilities:
- User registration
- Login/logout
- JWT token generation
- Refresh tokens
- RBAC/permissions
- Password reset
- OAuth integrations (future)

Database:
- auth_db

---

## 2. Organization Service

Responsibilities:
- Organization creation
- Member invitations
- Role management
- Team/workspace management
- Tenant isolation

Database:
- organization_db

---

## 3. Knowledge Base Service

Responsibilities:
- Knowledge base CRUD
- Document metadata management
- Chunk tracking
- Embedding orchestration
- Retrieval pipeline

Database:
- kb_db

---

## 4. Ingestion Service

Responsibilities:
- File uploads
- PDF/DOC/TXT parsing
- Chunking
- Embedding generation
- Vector DB insertion

Future:
- OCR support
- Async ingestion pipelines

---

## 5. Query Service

Responsibilities:
- Semantic search
- Retrieval pipelines
- Prompt construction
- LLM orchestration
- AI response generation

Future:
- Streaming responses
- Multi-model support
- Reranking

---

## 6. Billing Service

Responsibilities:
- Subscription management
- Usage tracking
- Quotas
- Payment integration

Future:
- Stripe integration
- Metered billing

---

## 7. Notification Service

Responsibilities:
- Emails
- Invite notifications
- System alerts
- Webhooks

Future:
- Queue-based async delivery

---

## 8. API Gateway

Responsibilities:
- Central entry point
- Routing
- Authentication middleware
- Rate limiting
- Request tracing
- Service aggregation

---

# Cross-Service Authentication

`auth_service` is the only service that signs tokens. Every other service only **verifies** them — none of them call back into `auth_service` to do it.

- **Algorithm**: `RS256` (asymmetric). `auth_service` holds the private key and signs access tokens with it. Every verifying service holds only the corresponding **public** key, so a compromised downstream service can never forge a token — it can only check signatures.
- **Key location**: each service keeps its key(s) in a local `keys/` folder (`services/<service>/keys/`), referenced by path via `JWT_PRIVATE_KEY_PATH` / `JWT_PUBLIC_KEY_PATH` env vars. `.pem` files are gitignored; each `keys/` folder has its own `README.md` with the `openssl` commands to generate/distribute them.
- **Refresh is never a cross-service concern**: only `auth_service` knows about refresh tokens (opaque, httpOnly cookie). A resource service that gets an expired/invalid access token just returns `401` — the client is responsible for hitting `auth_service`'s `/refresh` endpoint and retrying, not the resource service.
- **No cross-database foreign keys**: services never reference another service's tables via a DB-level `ForeignKey`. e.g. `organization_service.Organization.owner_id` is a plain indexed column holding an `auth_service` user id — trusted because it came from a verified JWT's `sub` claim, not enforced by a DB constraint (Postgres can't FK across separate databases, and a real FK here would violate database-per-service).
- **JWT payload stays minimal**: only `sub` (user id), `email`, `type`. No denormalized profile fields (name, etc.) added "just in case" — access tokens live up to their TTL without being refreshed mid-life, so embedding mutable data risks every verifying service reading stale values until reissue. If a service needs richer profile data without an extra call, that's a case for an event-driven local read cache, not for growing the token.

---