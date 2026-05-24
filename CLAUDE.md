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