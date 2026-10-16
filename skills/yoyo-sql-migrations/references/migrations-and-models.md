# Migrations & models reference

## Why no ORM

- Schema is explicit SQL, reviewable in diffs, portable to plain `psql`.
- No hidden lazy-loading/N+1; queries are hand-written and grouped.
- Pydantic is the single validation layer for both API and DB rows.

Consequence: the **schema** (migration SQL) and the **models** (`src/db/models`)
must be kept in sync by hand. Whenever you change one, update the other.

## yoyo commands

Config: `yoyo.ini` (`sources = migrations`). Or pass everything on the CLI.
Run from `backend/`.

```sh
# apply all pending migrations (interactive prompts unless --batch)
yoyo apply --database <db_url> ./migrations

# non-interactive (CI / docker entrypoint)
yoyo apply --database <db_url> ./migrations --batch

# list applied / pending migrations
yoyo list --database <db_url> ./migrations

# rollback the last applied migration (only if it has a rollback step;
# plain SQL migrations are forward-only, so prefer new migrations over rollback)
yoyo rollback --database <db_url> ./migrations
```

- With `yoyo.ini` present you can omit `--database` and the source path.
- yoyo records each applied file (name + hash). **Editing an applied migration**
  makes the recorded hash mismatch and yoyo will flag it; never edit history,
  add a new file.
- `psycopg2-binary` is what yoyo uses to talk to Postgres; the app itself uses
  `asyncpg`. Both belong in the dependency groups (`psycopg2-binary` and
  `yoyo-migrations` are dev dependencies).

## Naming & ordering

- Format: `NNNN_snake_case_description.sql`, 4-digit zero-padded, sequential.
  yoyo applies in **filename order**, so numbering is the ordering.
- One concern per file. Descriptive name (`add_orders_created_at`, not `fix`).
- Do not use yoyo's timestamped `yoyo new` naming: this project uses sequential
  numbers. Use `scripts/new_migration.py <slug>` to get the next one.
- Determine the next number as `max(existing numeric prefix) + 1`.

## Destructive changes

- Prefer additive: `ADD COLUMN ... NOT NULL DEFAULT ...` is backward compatible.
- To remove/rename: deploy a migration that stops using the column first, then a
  **later** migration that drops it. Example: rename a catalog code with
  `UPDATE ... ON UPDATE CASCADE`, then drop an unused flag in a later migration.
- For enum type changes, use `ALTER TYPE ... RENAME VALUE` / `ADD VALUE`.

## Lookup / catalog tables

- Closed sets live in lookup tables (e.g. `currencies`, `asset_types`) seeded via
  migrations with `ON CONFLICT (code) DO NOTHING` for idempotency.
- Mirror them as `str, Enum` in `src/db/models/enums.py`.
- They are **not** creatable at runtime (catalog is fixed).

## SQL type -> Pydantic field

| Postgres | Pydantic |
| --- | --- |
| `uuid` | `UUID` |
| `timestamptz` / `timestamp` | `datetime` |
| `DECIMAL(n,m)` / `NUMERIC` | `Decimal` |
| `TEXT` / `VARCHAR` | `str` |
| `BOOLEAN` | `bool` |
| `JSONB` / `JSON` | `dict` (or a typed sub-model) |
| nullable column | `Optional[...] = None` |

## Pydantic model conventions

- File per concept under `src/db/models/` (never one big `models.py`).
- Entity model named after the concept; separate `XCreate` / `XUpdate` inputs.
- Every field: `Field(..., description="...")` (see `lookup.py`, `price.py`).
- `id`: `UUID` when always from DB; `Optional[UUID] = None` when used pre-insert.
- Insert helpers: `to_dict()` converting `UUID`->`str`, `Decimal`->`str`, JSON via
  `json.dumps` (see `asset.py`, `reading.py`).
- `extra="forbid"` + per-type sub-models for JSON details (`details.py`).
- Models are built from DB rows with `Model(**row)`, so **field names == column
  names**. Extra `SELECT` columns must match the model fields exactly.

## End-to-end checklist

1. `python scripts/new_migration.py <slug>` -> new `migrations/NNNN_<slug>.sql`.
2. Fill in SQL (additive; index new columns; seed catalogs idempotently).
3. `yoyo apply --database <db_url> ./migrations [--batch]`, then `yoyo list`.
4. Add/update Pydantic model file(s) in `src/db/models/` mirroring columns.
5. Mirror any closed catalog in `enums.py`.
6. Update `repositories/queries.py` + repository if the field must be read/written.
7. Restart the service and smoke-test the affected endpoint.
8. Update any project docs that track migration state, if needed.

