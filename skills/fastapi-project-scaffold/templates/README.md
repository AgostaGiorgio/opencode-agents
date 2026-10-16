# __PROJECT_NAME__ — Backend

FastAPI REST API for **__PROJECT_TITLE__**. __PROJECT_DESCRIPTION__

## Tech stack

| Technology | Notes |
| --- | --- |
| Python | `^3.10.12` |
| FastAPI | `^0.110.0` |
| SQLAlchemy 2.0 (async) + asyncpg | PostgreSQL access with raw SQL |
| Pydantic / pydantic-settings | Models and configuration |
| dependency-injector | DI container |
| Poetry | Dependency management (`create = false`) |
| yoyo-migrations | SQL migrations (dev) |
| Uvicorn | ASGI server |

## Project structure

```
.
├── src/
│   ├── main.py                  # FastAPI app, DI wiring, router include
│   ├── di.py                    # dependency-injector container
│   ├── config/app_config.py     # pydantic-settings + YAML
│   ├── clients/postgres_client.py
│   ├── db/models/               # Pydantic models (mirror the schema)
│   ├── repositories/            # queries.py (raw SQL) + data access
│   ├── services/                # business logic
│   └── routers/                 # API endpoints
├── migrations/                  # yoyo SQL migrations
├── pyproject.toml / poetry.toml
├── .env.example
└── Dockerfile
```

## Configuration

Copy `.env.example` to `.env` and fill in the values:

| Variable | Description |
| --- | --- |
| `POSTGRESQL_USER` / `POSTGRESQL_PASSWORD` | PostgreSQL credentials |
| `POSTGRESQL_HOST` / `POSTGRESQL_PORT` | PostgreSQL host and port |
| `POSTGRESQL_DATABASE` | Database name |
| `APP_URL` | *(optional)* public URL of this service |
| `ORBIT_API_URL` | *(optional)* Orbit registration endpoint; empty disables it |

## Local development

```sh
poetry install
cp .env.example .env
yoyo apply --database <db_url> ./migrations
poetry run python src/main.py
```

OpenAPI docs are available at `http://localhost:__PORT__/docs`.

## API

All endpoints are prefixed with `/api/v1`.

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/items` | List items |
| `GET` | `/items/{item_id}` | Get an item |
| `POST` | `/items` | Create an item |
| `PUT` | `/items/{item_id}` | Update an item |
| `DELETE` | `/items/{item_id}` | Delete an item |

> The `items` resource is a placeholder example. Replace it with your domain.

## Migrations

```sh
yoyo apply  --database <db_url> ./migrations   # apply
yoyo list   --database <db_url> ./migrations   # show status
yoyo rollback --database <db_url> ./migrations # roll back the last one
```

## Docker

```sh
docker buildx build --platform linux/amd64 -t registry/__PROJECT_NAME___be:0.1.0 .
```

The image runs `uvicorn src.main:app --port __PORT__ --host 0.0.0.0`.
