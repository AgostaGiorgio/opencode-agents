---
name: Yoyo SQL Migrations
description: Use when changing the database schema or the Pydantic data models in a project that uses yoyo-migrations with raw SQL (no ORM). Covers writing sequential `migrations/NNNN_name.sql` files, yoyo commands (apply/list/rollback) and yoyo.ini, and generating/updating Pydantic models under `src/db/models`. Trigger on requests like "migration", "migrazione", "yoyo", "nuova tabella", "add column", "alter table", "schema change", "genera modelli pydantic", "src/db/models", "SQL migration", "aggiungi colonna".
---

# Yoyo SQL migrations + Pydantic models (no ORM)

This project manages the database **without an ORM**:

- The schema is defined by **raw SQL files** in `migrations/`, applied with
  **yoyo-migrations**.
- Pydantic models in `src/db/models/` **mirror** tables/views for validation and
  transport. They are NOT SQLAlchemy models (no `DeclarativeBase`, no
  `mapped_column`, no relationships).
- Repositories run raw SQL (`text(...)` in `repositories/queries.py`) and build
  models from rows with `Model(**row)`. See the `async-db-repository` skill.

Direction of truth: **migration SQL defines the schema; Pydantic models follow it.**
When you change one, review the other.

## Layout

```
backend/
├── yoyo.ini                 # sources = migrations, database = ...
├── migrations/
│   ├── NNNN_initial_schema.sql
│   ├── ...
│   └── NNNN_<description>.sql           # next number = max + 1
└── src/db/models/
    ├── enums.py             # closed catalogs (str, Enum) mirrored by lookup tables
    └── <concept>.py         # one file per domain concept (asset, order, ...)
```

## Workflow (schema change)

1. **Create the migration file** with the next sequential number:
   - run `python scripts/new_migration.py <slug>` from `backend/` (the script in
     this skill scans `migrations/` and creates `NNNN_<slug>.sql`), or
   - manually copy the highest `NNNN_*` and increment, zero-padded to 4 digits.
2. **Write the SQL** (see `templates/migration.sql`): a short comment header
   (in the project's language) explaining what/why, then the `ALTER`/`CREATE`/seed
   statements.
   - Prefer **additive, backward-compatible** changes.
   - Put **destructive** changes (DROP COLUMN/TABLE) in a **later** migration.
   - Add indexes for new query columns.
   - Seed lookup/catalog tables idempotently (`ON CONFLICT ... DO NOTHING`).
3. **Apply and verify** the migration (see commands below).
4. **Generate/update the Pydantic models** in `src/db/models/` (see next section).
5. **If a query or repository must expose the new field**: update
   `repositories/queries.py` and the model, per the `async-db-repository` skill.

## Pydantic model generation (step 4)

For a new/changed table, add or update a **file per domain concept** in
`src/db/models/` (e.g. `order.py`, not `models.py`). Use
`templates/model.py`:

- One **entity** model named after the table concept (`Asset`, `AssetOrder`,
  `ExchangeRate`, `ReadingCreate`).
- A separate **Create/Update** model (`XCreate`, `XLabelUpdate`) for input
  payloads; include a `to_dict()` helper returning insert params, converting
  `UUID` -> `str`, `Decimal` -> `str`, and JSON fields with `json.dumps`.
- `Field(..., description="...")` on every field.
- `id`: required (`UUID`) when the row always comes from the DB; use
  `Optional[...] = None` when the model is also used before insert.
- Types: `UUID` for `uuid`, `datetime` for `timestamptz`, `Decimal` for
  `DECIMAL`, `str` for `TEXT/VARCHAR`, `dict` for `JSONB`.
- Keep field names **identical** to column names (rows are passed as `**row`).

If the change touches a **closed catalog** (e.g. `asset_types`, `currencies`):
- seed the new codes in the migration, and
- mirror them in `src/db/models/enums.py` as a `str, Enum`
  (see `templates/enum_catalog.py`).

If the change adds **type-specific JSON metadata**, follow the existing
`details.py` pattern: one sub-model per type with
`ConfigDict(extra="forbid")` plus a `parse_details(asset_type, raw)` dispatcher.

## Non-negotiable rules

- **No ORM.** Never add SQLAlchemy models, `DeclarativeBase`, `mapped_column`,
  `relationship`, or metadata reflection. Schema lives in SQL migrations.
- **Never edit an already-applied migration.** Add a new `NNNN_*` file instead;
  yoyo records applied files by hash and will refuse/flag changed ones.
- **Sequential numbering** `NNNN_snake_case_description.sql` (4 digits). yoyo
  applies in filename order. Do not use yoyo's timestamped `yoyo new` naming.
- **One concern per migration**; keep the filename descriptive of the change.
- **Models mirror the schema**, names 1:1 with columns. Do not invent shadow
  names; if you do, the `Model(**row)` construction breaks.
- **Money/quantity are `Decimal`**, ids `UUID`, timestamps `datetime`.
- **yoyo uses psycopg2, the app uses asyncpg**: keep `psycopg2-binary` and
  `yoyo-migrations` in the dev dependency group; runtime SQL uses asyncpg.

## Reference

- `references/migrations-and-models.md` — yoyo commands, naming/ordering,
  destructive-change strategy, lookup catalogs, SQL->Pydantic type map,
  end-to-end checklist.
- `templates/migration.sql`, `templates/model.py`,
  `templates/enum_catalog.py`, `templates/yoyo.ini`,
  `scripts/new_migration.py`.
