#!/usr/bin/env python3
"""Generate a QR code SVG for each link given on the command line.

Usage:
    python qrcoder.py <url> [<url> ...] [-o OUTPUT_DIR]
"""
import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

import segno


def slug_for(url: str) -> str:
    """Build a filename from the URL's last path segment (e.g. the LinkedIn handle)."""
    parsed = urlparse(url)
    parts = [p for p in parsed.path.split("/") if p]
    name = parts[-1] if parts else parsed.netloc
    return re.sub(r"[^A-Za-z0-9_-]+", "-", name).strip("-") or "qr"


def make_svg(url: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{slug_for(url)}.svg"
    qr = segno.make(url, error="m")
    qr.save(path, scale=10, border=4, dark="#000000", light="#ffffff")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate QR code SVGs from links.")
    parser.add_argument("urls", nargs="+", help="links to encode")
    parser.add_argument("-o", "--output", default="qrcodes", help="output directory")
    args = parser.parse_args()

    for url in args.urls:
        print(f"{url} -> {make_svg(url, Path(args.output))}")


if __name__ == "__main__":
    main()
