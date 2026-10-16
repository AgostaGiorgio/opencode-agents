"""Closed catalog mirrored by a lookup table seeded in migrations.

Use for fixed sets (asset types, currencies, order sides...). The Rust-like
`str, Enum` lets the value be used directly as a DB code and in Pydantic models.
Keep in sync with the seed INSERT in the migration.
"""

from enum import Enum


class <Catalog>(str, Enum):
    """Fixed catalog; managed via migrations, not at runtime."""

    FIRST = "FIRST"
    SECOND = "SECOND"


# Optional: codes that behave a certain way (e.g. support orders).
<CATALOG>_CODES: frozenset[str] = frozenset(
    {
        <Catalog>.FIRST.value,
        <Catalog>.SECOND.value,
    }
)
