# Conventions & reference

Deep detail behind the `async-db-repository` skill. Read when the task is a
migration, a review, or when something behaves differently than expected.

## Layer responsibilities

| Layer | Knows about | Must not |
| --- | --- | --- |
| `queries.py` | SQL text and `text()` objects | application objects |
| repository | `PostgresClient`, `queries`, Pydantic models | business rules, HTTP |
| service | repositories, business rules | SQL, sessions, `PostgresClient` |
| router | service, request/response models | SQL, repositories, sessions |
| `di.py` | wiring only | any logic |
| `app_config` | settings + connection URI | engine/session creation |

## Why client + injected repositories (vs global session)

- **Testability**: inject a fake/stub `PostgresClient` (or repository) without
  monkeypatching module globals.
- **Single owner of the engine**: the engine lives in one Singleton, not in every
  module that imports a session factory.
- **Explicit dependencies**: a repository's `__init__` documents that it needs a DB;
  a service's `__init__` documents which repositories it uses.
- **Consistency**: same shape across projects, so generated code drops in.

## Sessions & transactions

- Read methods: `async with self.__postgres_client.async_session() as session:` and
  no explicit commit. The context manager closes the session.
- Write methods: wrap statements in `async with session.begin():`. On normal exit
  it commits; on exception it rolls back. Requires a running transaction, so do not
  call `session.commit()` inside it.
- **Multi-statement atomic flows** (e.g. insert an order then recompute a position)
  go inside one `begin()` block. Never commit between steps.
- Do not open a session and then call another repository method that opens its own
  session *inside the same transaction* expecting shared state; each method is its
  own unit of work.
- Keep `expire_on_commit=False` on the sessionmaker so returned objects stay usable.

## Error handling

- Catch only what you can handle: `except (SQLAlchemyError, ValidationError) as e:`.
- Always log with `exc_info=True` to capture the traceback.
- Let unexpected exceptions propagate. `except Exception` hides programming errors
  (`NameError`, `AttributeError`, `TypeError`) and turns bugs into silent empty
  results — exactly the failure mode that makes "history returns []" hard to debug.
- Return contract (keep it stable):
  - reads: `[]` / `None`
  - writes: `True`/`False` or the entity / `None`
  - routers map `None`/`False` to 404/400.
- `NoResultFound` / `MultipleResultsFound` (from `.one()`) are `SQLAlchemyError`
  subclasses and stay handled.

## The `q.` namespace rule

`from src.repositories import queries as q`, then `q.GET_THING`.
Do **not** use `from ... import *`.

This applies to callables too. A helper function in `queries.py` (e.g.
`get_history_query(period)`) is a bare name if you forget the prefix, raising
`NameError` that a broad catch would swallow. Signature of the bug: an endpoint
returns an empty/default result with no visible error.

## UUID / Decimal / datetime params

Follow the surrounding code: UUIDs are passed as `str(uuid)`, JSONB as a JSON
string cast in SQL (`(:details)::jsonb`), rates/amounts as `str(decimal)` when the
driver expects it. Do not invent a new convention per file.

## Migration checklist (legacy global session -> this pattern)

1. Create `src/clients/postgres_client.py` (copy `templates/postgres_client.py`).
2. Move query constants into `src/repositories/queries.py`; import callables too.
3. Move the repository into `src/repositories/<entity>.py`:
   - remove every `@classmethod`, add `__init__(self, postgres_client: PostgresClient)`;
   - replace `AsyncSessionLocal()` with `self.__postgres_client.async_session()`;
   - prefix all SQL names with `q.` (constants **and** helper functions);
   - internal calls `SomeRepository.foo()` become `self.foo()`.
4. Service: add `__init__(self, <entity>_repository)`; replace static calls with
   `self.__<entity>_repository...`.
5. `di.py`: `postgres_client` Singleton -> repositories Factory -> services Factory.
6. Delete the old global engine/session module; remove stale `__pycache__`.
7. `grep -rn "AsyncSessionLocal\|from src.*db.db\|import \*" src/` must be empty
   (except unrelated `import *`, if any).

## Verification

- Syntax/import:
  - `python -m compileall -q src`
  - `python -c "import src.main"`
- DI graph resolves:
  - `python -c "from src.di import Container; c=Container(); c.<entity>_service()"`
- Routes registered: `python -c "from src.main import app; print(len(app.routes))"`
- With a live DB, smoke-test the read and write endpoints, especially any
  multi-statement transaction endpoint.

