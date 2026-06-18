# ContextHub

A multi-tenant, AI-powered RAG (Retrieval Augmented Generation) platform. Users sign up, create organizations, invite teammates, build knowledge bases from uploaded documents, and query those knowledge bases for AI-generated, context-grounded answers.

Built as a **microservices monorepo** to explore service isolation, domain-driven boundaries, and production-grade backend architecture. See [CLAUDE.md](CLAUDE.md) for the full planned service breakdown (auth, organization, knowledge base, ingestion, query, billing, notification, API gateway).

## Status

Only `services/auth_service` is implemented so far (in progress). Everything else in CLAUDE.md is planned, not built yet.

## Monorepo layout

```
services/
  auth_service/   # user auth — see services/auth_service/README.md
  user_service/    # stub, not started
```

Each service is an independently installable Python package (own `pyproject.toml`, own `.venv`) with its own README for service-specific details (env vars, run commands, endpoints).

## Prerequisites

- Python 3.13
- [Poetry](https://python-poetry.org/) 2.x
- PostgreSQL (running locally)

## Dev environment setup

From the repo root, one-time:

```bash
poetry config virtualenvs.in-project true
```

This makes Poetry create each service's virtualenv inside that service's own folder (`services/<service>/.venv`) instead of a shared global location.

Then, per service, `cd` into it and run `poetry install`. See each service's README for how to run it.

## Running a service

For now, only `auth_service` is runnable:

```bash
cd services/auth_service
poetry install
uvicorn auth_service.main:app --reload --app-dir src
```

See [services/auth_service/README.md](services/auth_service/README.md) for env var setup and details.
