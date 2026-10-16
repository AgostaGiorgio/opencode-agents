"""Raw SQL statements for the repository.

Conventions:
- one uppercase `text(...)` constant per statement;
- always parameterized (`:param`), never interpolate values;
- RETURNING for inserts/updates when the caller needs the row;
- small helper functions allowed (e.g. building a query for a period), but they
  MUST be called through the module namespace (`q.get_history_query(...)`), never
  imported with `*` into the repository.
"""

from sqlalchemy import text, TextClause


GET_<ENTITIES> = text("""
SELECT id, name, created_at
FROM <table>
ORDER BY created_at DESC
""")

GET_<ENTITY> = text("""
SELECT id, name, created_at
FROM <table>
WHERE id = :id
""")

NEW_<ENTITY> = text("""
INSERT INTO <table> (name)
VALUES (:name)
RETURNING id
""")

UPDATE_<ENTITY> = text("""
UPDATE <table>
SET name = :name
WHERE id = :id
""")

DELETE_<ENTITY> = text("""
DELETE FROM <table>
WHERE id = :id
""")


def get_history_query(period: str) -> tuple[TextClause, dict]:
    """Example helper: dynamic statements still live here, called via q.<name>."""
    if period == "all":
        return text("""
        SELECT record_date, total
        FROM history
        ORDER BY record_date
        """), {}
    return text("""
    SELECT record_date, total
    FROM history
    WHERE record_date >= CURRENT_DATE - (:months * INTERVAL '1 month')
    ORDER BY record_date
    """), {"months": 12}
