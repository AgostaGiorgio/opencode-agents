#!/usr/bin/env python3
"""Create the next sequential yoyo migration file.

Usage (run from the project's `backend/` directory):
    python scripts/new_migration.py add_orders_created_at

Scans the migrations directory for `NNNN_` prefixes, creates the next file
`migrations/NNNN_<slug>.sql` with a header, and prints its path. Exit code 1 on
invalid slug or if the target already exists.
"""

import argparse
import re
import sys
from pathlib import Path

MIGRATIONS_DIR = Path("migrations")
NUMBER_RE = re.compile(r"^(\d+)_")
SLUG_RE = re.compile(r"[a-z0-9_]+")


def next_number(directory: Path) -> int:
    highest = 0
    for path in directory.glob("*.sql"):
        match = NUMBER_RE.match(path.name)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the next yoyo migration file.")
    parser.add_argument("slug", help="snake_case description, e.g. add_orders_created_at")
    args = parser.parse_args()

    slug = args.slug.strip().lower().replace(" ", "_").replace("-", "_")
    if not SLUG_RE.fullmatch(slug):
        print(f"Invalid slug {args.slug!r}: use snake_case [a-z0-9_].", file=sys.stderr)
        return 1

    if not MIGRATIONS_DIR.is_dir():
        print(f"Directory not found: {MIGRATIONS_DIR} (run from backend/).", file=sys.stderr)
        return 1

    number = next_number(MIGRATIONS_DIR)
    target = MIGRATIONS_DIR / f"{number:04d}_{slug}.sql"
    if target.exists():
        print(f"Already exists: {target}", file=sys.stderr)
        return 1

    target.write_text(
        f"-- {slug.replace('_', ' ')}\n"
        "-- Describe what changes and why. Keep it additive/backward-compatible\n"
        "-- when possible; put destructive changes in a later migration.\n\n"
    )
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
