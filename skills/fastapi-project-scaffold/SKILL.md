---
name: FastAPI Project Scaffold
description: Use when creating a brand-new Python/FastAPI backend from scratch in the house style (router -> service -> repository -> PostgresClient, Pydantic models, Poetry, dependency-injector, PostgreSQL via async SQLAlchemy, yoyo SQL migrations). Trigger on requests like "crea un nuovo progetto", "new FastAPI project", "scaffold/boilerplate backend", "init a new service", "nuova API", "bootstrap backend", "struttura router-service-repository", "setup poetry fastapi", "nuovo microservizio".
---

# FastAPI project scaffold (house style)

Creates a new backend that follows the same architecture used across myInves,
MTrack and Orbit:

```
HTTP -> router (FastAPI + DI) -> service (business logic)
     -> repository (data access) -> PostgresClient -> queries.py (raw SQL)

                                   src/db/models/ (Pydantic) mirror the SQL schema
                                   migrations/ (yoyo, raw SQL)
```

- **Layers**: `routers/` -> `services/` -> `repositories/` -> `clients/postgres_client.py`.
  Each layer only knows the one below it. See `references/architecture.md`.
- **Pydantic** for models and settings; **no ORM** (raw SQL + `text()`).
- **Poetry** for dependencies with `create = false` (install into the active env).
- **dependency-injector** wires `postgres_client` (Singleton) -> repositories
  (Factory) -> services (Factory); routers use `@inject` + `Depends(Provide[...])`.
- **Project layout is the myInves-style**: `src/db/models/` + `migrations/`.

This skill produces a *backend* project (no frontend, no monorepo tooling). For
the day-to-day conventions of each layer, defer to the sibling skills:

| Concern | Skill |
| --- | --- |
| repositories / services / queries / DI / config | `async-db-repository` |
| SQL migrations + Pydantic model generation | `yoyo-sql-migrations` |
| Orbit self-registration (heartbeat) | `orbit-registration` |

## When to use

Use this skill to bootstrap a **new** FastAPI backend: new service, new microservice,
a fresh repo in the house style, or a throwaway reference project. Do **not** use it
to add features to an existing project (that is `async-db-repository` /
`yoyo-sql-migrations`).

## Workflow

1. **Collect the metadata** (ask if unknown):
   - `name` — project / package name, kebab or snake (e.g. `my-service`).
   - `description` — one line.
   - `db_name` — PostgreSQL database (defaults to `name` with `_`).
   - `title` — OpenAPI title (defaults to `Name`).
   - `port` — HTTP port (default `8080`).
2. **Generate the tree** with the bundled script (preferred):
   ```sh
   python scripts/scaffold_project.py \
       --target ../<name> \
       --name <name> \
       --description "<description>"
   ```
   Add `--db-name`, `--title`, `--port`, `--force` as needed. The script copies
   `templates/` and substitutes `__PLACEHOLDERS__`. Manual fallback: copy
   `templates/` yourself and replace the placeholders listed below.
3. **Install & configure**:
   ```sh
   cd <target>
   poetry install
   cp .env.example .env          # then edit the PostgreSQL credentials
   yoyo apply --database <db_url> ./migrations
   ```
4. **Run** (dev): `poetry run python src/main.py`.
5. **Verify** (see `references/architecture.md` for the full checklist):
   ```sh
   python -m compileall -q src
   python -c "import src.main"
   python -c "from src.di import Container; Container().item_service()"
   python -c "from src.main import app; print(len(app.routes))"
   ```
6. **Make it yours**: the scaffold ships a working end-to-end **`items`** example
   slice (model, queries, repository, service, router, migration `0001`). When you
   add the first real entity, delete/replace the `items` files and update
   `src/repositories/queries.py`, `src/di.py` and `src/routers/router.py`.
   For a multi-resource API, split `routers/router.py` into
   `routers/<entity>.py` modules and include them with `prefix=`/`tags=` in
   `main.py` (see `references/architecture.md`).
7. **Optional**: apply the `orbit-registration` skill to register the service in
   Orbit. `app_config` already exposes `app_url` / `orbit_api_url`, and
   `.env.example` already has the variables.

## Placeholders (used by the script)

| Placeholder | Meaning | Example |
| --- | --- | --- |
| `__PROJECT_NAME__` | Poetry package name | `my-service` |
| `__PROJECT_TITLE__` | OpenAPI title | `MyService API` |
| `__PROJECT_DESCRIPTION__` | One-line description | `My service API` |
| `__DB_NAME__` | PostgreSQL database | `my_service` |
| `__PORT__` | HTTP port | `8080` |

## Non-negotiable rules

- **Poetry with `create = false`** (`poetry.toml`). Do not create an in-project venv.
- **No `__init__.py`** in `src/**`: the packages rely on implicit namespace
  packages (same as myInves / MTrack). Top-level modules are imported as
  `src.<module>`.
- **Version comes from `pyproject.toml`** (`[tool.poetry].version`) read with
  `tomli`; `tomli` must stay a runtime dependency.
- **DI only, no globals.** `postgres_client` is a Singleton; repositories and
  services are Factories with constructor injection. Never instantiate a
  repository inside a service by hand.
- **No global engine/session** anywhere. Sessions always come from
  `self.__postgres_client.async_session()`.
- **Raw SQL** lives in `src/repositories/queries.py` as `text(...)` constants
  referenced as `q.NAME`. Parameterize all values.
- **Pydantic models mirror the schema**, names identical to columns, so rows can be
  built with `Model(**row)`.
- **Routers** declare `response_model` + `status_code`, inject the service with
  `@inject` + `Depends(Provide[Container.<x>_service]))`, and map `None`/`False`
  results to `HTTPException` 404/400.
- **App prefix** is `/api/v1`; version is served from `pyproject.toml`.
- **CORS is configurable** via `app_config` (defaults to permissive `["*"]`).

## Reference & assets

- `references/architecture.md` — directory tree, layer responsibilities, DI wiring,
  single- vs multi-router, config/version handling, verification checklist.
- `templates/` — a complete, runnable project skeleton (project files, `src/`,
  the `items` example slice, `migrations/0001`, `AGENTS.md`, `README.md`).
- `scripts/scaffold_project.py` — copies `templates/` and fills the placeholders.
