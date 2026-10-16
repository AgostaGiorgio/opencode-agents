#!/usr/bin/env python3
"""Scaffold a new FastAPI backend in the house style.

Copies the templates in ../templates into a target directory, substituting the
placeholders, then prints the next steps.

Usage:
    python scripts/scaffold_project.py \\
        --target ../my-service \\
        --name my-service \\
        --description "My service API" \\
        [--title "MyService API"] \\
        [--db-name my_service] \\
        [--port 8080] \\
        [--force]
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

TEMPLATES_DIR = (Path(__file__).resolve().parent.parent / "templates").resolve()

SKIP_NAMES = {"__pycache__", ".git", ".venv", "venv"}


def build_replacements(args: argparse.Namespace) -> dict[str, str]:
    title = args.title or args.name.replace("-", " ").replace("_", " ").title()
    db_name = args.db_name or args.name.replace("-", "_")
    return {
        "__PROJECT_NAME__": args.name,
        "__PROJECT_TITLE__": title,
        "__PROJECT_DESCRIPTION__": args.description,
        "__DB_NAME__": db_name,
        "__PORT__": str(args.port),
    }


def render(text: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def copy_templates(target: Path, replacements: dict[str, str], force: bool) -> tuple[int, list[str]]:
    written = 0
    skipped: list[str] = []

    for dirpath, dirnames, filenames in os.walk(TEMPLATES_DIR):
        dirnames[:] = [d for d in dirnames if d not in SKIP_NAMES]
        rel_dir = Path(dirpath).relative_to(TEMPLATES_DIR)
        (target / rel_dir).mkdir(parents=True, exist_ok=True)

        for filename in filenames:
            src = Path(dirpath) / filename
            dst = target / rel_dir / filename
            if dst.exists() and not force:
                skipped.append(str(rel_dir / filename))
                continue

            raw = src.read_bytes()
            try:
                content = raw.decode("utf-8")
            except UnicodeDecodeError:
                dst.write_bytes(raw)
            else:
                dst.write_text(render(content, replacements), encoding="utf-8")
            written += 1

    return written, skipped


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold a new FastAPI backend (house style).")
    parser.add_argument("--target", required=True, help="Directory to create (must not exist or use --force).")
    parser.add_argument("--name", required=True, help="Project / Poetry package name (e.g. my-service).")
    parser.add_argument("--description", default="FastAPI backend service.", help="One-line project description.")
    parser.add_argument("--title", default=None, help="OpenAPI title (defaults to the name, humanized).")
    parser.add_argument("--db-name", default=None, help="PostgreSQL database (defaults to the name with underscores).")
    parser.add_argument("--port", type=int, default=8080, help="HTTP port (default: 8080).")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    if not TEMPLATES_DIR.is_dir():
        print(f"error: templates directory not found: {TEMPLATES_DIR}", file=sys.stderr)
        return 1

    target = Path(args.target).expanduser().resolve()
    if target == TEMPLATES_DIR or TEMPLATES_DIR in target.parents:
        print("error: --target cannot be inside the skill templates directory.", file=sys.stderr)
        return 1

    replacements = build_replacements(args)
    written, skipped = copy_templates(target, replacements, args.force)

    print(f"Scaffolded '{args.name}' into {target}")
    print(f"  files written: {written}")
    if skipped:
        print(f"  files skipped (already exist, use --force): {len(skipped)}")
        for path in skipped:
            print(f"    - {path}")

    db_name = replacements["__DB_NAME__"]
    port = replacements["__PORT__"]
    print("\nNext steps:")
    print(f"  cd {target}")
    print("  poetry install")
    print("  cp .env.example .env        # then edit the PostgreSQL credentials")
    print(f"  yoyo apply --database postgresql://appuser:post-password@localhost:5432/{db_name} ./migrations")
    print("  poetry run python src/main.py")
    print(f"\n  Docs: http://localhost:{port}/docs")
    print("\nThe 'items' example slice is a working reference: replace it with your")
    print("first real entity (see AGENTS.md and the async-db-repository skill).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
