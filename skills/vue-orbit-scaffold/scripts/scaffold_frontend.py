#!/usr/bin/env python3
"""Scaffold a new Vue 3 + Vite + Tailwind (Orbit theme) frontend.

Copies the templates in ../templates into a target directory, substituting the
placeholders and generating placeholder PWA icons, then prints the next steps.

Usage:
    python scripts/scaffold_frontend.py \\
        --target ../my-app-frontend \\
        --name MyApp \\
        --slug my-app \\
        --description "My app" \\
        [--api-url http://localhost:8000] \\
        [--force]
"""

from __future__ import annotations

import argparse
import os
import struct
import sys
import zlib
from pathlib import Path

TEMPLATES_DIR = (Path(__file__).resolve().parent.parent / "templates").resolve()

SKIP_NAMES = {"__pycache__", ".git", "node_modules", "dist"}
BRAND_PRIMARY = (0x8B, 0x5C, 0xF6)  # #8b5cf6, matches orbit-ecosystem-preset.js
ICONS = {"favicon.png": 48, "icon-192.png": 192, "icon-512.png": 512}


def build_replacements(args: argparse.Namespace) -> dict[str, str]:
    return {
        "__APP_NAME__": args.name,
        "__APP_SLUG__": args.slug,
        "__APP_DESCRIPTION__": args.description,
        "__API_URL__": args.api_url,
    }


def render(text: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def write_solid_png(path: Path, size: int, rgb: tuple[int, int, int]) -> None:
    """Write a solid-color RGBA PNG without external dependencies."""
    r, g, b = rgb
    row = b"\x00" + bytes((r, g, b, 255)) * size
    raw = row * size

    def chunk(ctype: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + ctype
            + data
            + struct.pack(">I", zlib.crc32(ctype + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)  # 8-bit RGBA
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(png)


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


def generate_icons(public_dir: Path, force: bool) -> list[str]:
    public_dir.mkdir(parents=True, exist_ok=True)
    generated = []
    for name, size in ICONS.items():
        path = public_dir / name
        if path.exists() and not force:
            continue
        write_solid_png(path, size, BRAND_PRIMARY)
        generated.append(name)
    return generated


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold a new Vue frontend (Orbit theme).")
    parser.add_argument("--target", required=True, help="Directory to create.")
    parser.add_argument("--name", required=True, help="App display name (e.g. MyApp).")
    parser.add_argument("--slug", default=None, help="Package/Docker slug (defaults to the name, lowercased).")
    parser.add_argument("--description", default="Vue + Tailwind app.", help="One-line description.")
    parser.add_argument("--api-url", default="http://localhost:8000", help="Backend base URL.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not args.slug:
        args.slug = args.name.lower().replace(" ", "-")

    if not TEMPLATES_DIR.is_dir():
        print(f"error: templates directory not found: {TEMPLATES_DIR}", file=sys.stderr)
        return 1

    target = Path(args.target).expanduser().resolve()
    if target == TEMPLATES_DIR or TEMPLATES_DIR in target.parents:
        print("error: --target cannot be inside the skill templates directory.", file=sys.stderr)
        return 1

    replacements = build_replacements(args)
    written, skipped = copy_templates(target, replacements, args.force)
    icons = generate_icons(target / "public", args.force)

    print(f"Scaffolded '{args.name}' into {target}")
    print(f"  files written: {written}")
    if icons:
        print(f"  icons generated: {', '.join(icons)} (solid brand color placeholders)")
    if skipped:
        print(f"  files skipped (already exist, use --force): {len(skipped)}")

    print("\nNext steps:")
    print(f"  cd {target}")
    print("  npm install")
    print("  npm run dev            # http://localhost:5173")
    print("\nReplace the placeholder icons in public/ with the real logo, and edit")
    print("the sample views in src/views/ (see AGENTS.md and the vue-orbit-ui skill).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
