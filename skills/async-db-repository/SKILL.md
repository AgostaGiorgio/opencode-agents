---
name: Async DB Repository
description: Use when creating or modifying database-query code in Python/FastAPI projects that follow the PostgresClient + repositories + SQLAlchemy async + dependency-injector pattern (raw SQL in a `queries` module, repository classes injected into services via constructor). Trigger on requests like "add a repository", "query the database", "nuova query", "nuovo repository", "esegue query", "add endpoint che legge/scrive sul DB", "PostgresClient", "SQLAlchemy async", "dependency injection", "raw SQL query".
---

# Async DB Repository pattern

Canonical way to write database code in these projects:

```
router (FastAPI)  ->  service  ->  repository  ->  PostgresClient  ->  queries.py (raw SQL)
```

- `PostgresClient` owns the async engine and session factory. One instance per app.
- Repositories are **classes**, receive the client in `__init__`, and open a session per method.
- Raw SQL lives as `text(...)` constants in a `queries.py` module, referenced as `q.NAME`.
- Services are **classes**, receive repositories in `__init__`, hold zero DB knowledge.
- Everything is wired by `dependency-injector`: `postgres_client` (Singleton) ->
  repositories (Factory) -> services (Factory).
- Models are Pydantic (no SQLAlchemy ORM / no `DeclarativeBase`).
- Writes inside a single method are atomic (`async with session.begin()`).

Keep this pattern consistent across every service that adopts it.

## When to use

Use this skill whenever the task involves reading from or writing to PostgreSQL:
adding an endpoint that queries the DB, a new repository, a new SQL statement, a
new service that consumes a repository, wiring DI, or refactoring old
module-level `AsyncSessionLocal` / global engine code into this pattern.

## Workflow

1. **Locate the project layout.** Check where models and the repositories package live
   (the location may differ between projects). Match the existing layout; do not
   impose a new one. The paths below are the canonical convention.
2. **Define the SQL** in the existing `queries.py` (usually `src/repositories/queries.py`):
   uppercase constant names for statements, one `text(...)` each. Parameterized only
   (`:param`), never string interpolation of values.
3. **Add/​extend the repository** (`src/repositories/<entity>.py`) using
   `templates/repository.py`: class + `__init__(self, postgres_client: PostgresClient)`,
   `async with self.__postgres_client.async_session() as session:` per method.
4. **Add/​extend the service** (`src/services/<entity>.py`) using
   `templates/service.py`: `__init__(self, <entity>_repository)` and call
   `self.__<entity>_repository...`.
5. **Wire the graph** in `src/di.py` using `templates/di.py` (client Singleton,
   repository Factory, service Factory).
6. **Add the router endpoint** that depends on the service via
   `Depends(Provide[Container.<entity>_service]))`.
7. **Verify**: `python -m compileall src` + `python -c "import src.main"` and, if a DB
   is reachable, a smoke test of the relevant endpoint.

Templates live in `templates/` relative to this file. Read the ones you need; the
files are skeletons with `<placeholders>`.

## Non-negotiable rules

- **No global engine/session.** Never import a module-level `AsyncSessionLocal`.
  The session always comes from `self.__postgres_client.async_session()`.
- **No `@classmethod` repositories.** Repositories are instances so they can be
  injected and mocked; never call `SomeRepository.method()` statically.
- **Namespace the SQL module**: `from src.repositories import queries as q` and use
  `q.GET_THING`. Never `from queries import *`. This includes callables, not just
  constants: a helper such as `get_history_query(period)` must be `q.get_history_query(period)`.
  (Forgetting the prefix on lowercase helpers is the classic silent bug.)
- **Constructor injection only.** Repositories get the client; services get
  repositories. No service reaches for `Container` or globals.
- **Catch narrowly.** `except (SQLAlchemyError, ValidationError) as e:` and log with
  `exc_info=True`. Never `except Exception` — it hides `NameError`, `AttributeError`,
  `TypeError`, i.e. real bugs. Let unexpected errors bubble to a 500.
- **Parameterize.** All dynamic values via `session.execute(stmt, {...})`. UUIDs/dates
  passed as `str(...)`/native objects as the existing code does.
- **One session per repository method.** Do not share sessions across method calls.
- **Atomicity.** A write flow with multiple statements must run inside one
  `async with session.begin():` so it commits/rolls back as a unit.
- **Error contract.** Read methods return `[]` / `None`; write methods return
  `True/False` or the entity / `None`. Keep the project's existing contract.

## Anti-patterns (do not reintroduce)

- Module-level `engine = create_async_engine(...)` / `AsyncSessionLocal`.
- `class XRepository` with all `@classmethod`.
- `from src.repositories.queries import *`.
- `except Exception: return []`.
- Instantiating a repository directly inside a service instead of injecting it.
- Putting SQL inline in the repository instead of `queries.py`.
- Services importing `PostgresClient` or touching `session`.

## Reference

- `references/conventions.md` — rationale, transaction/error details, migration
  checklist from legacy global-session code, verification steps.
- `templates/postgres_client.py`, `templates/repository.py`, `templates/queries.py`,
  `templates/service.py`, `templates/di.py`, `templates/app_config.py`.
