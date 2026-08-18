#!/usr/bin/env python3
"""Assemble index.html from src/page.html.

The published page has to be a single self-contained file: the host blocks
external requests, so the two webfonts and all four case screenshots are
inlined as data URIs. This script does that substitution.

    python3 build.py
"""
import base64
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src" / "page.html"
FONTS = ROOT / "src" / "fonts.css"
OUT = ROOT / "index.html"

SHOTS = {
    "/*SHOT_FINFLOW*/": "keys1.jpg",
    "/*SHOT_LUMIO*/": "keys2.jpg",
    "/*SHOT_ATLAS*/": "keys3.jpg",
    "/*SHOT_GREENNEST*/": "keys4.jpg",
}

FONT_NOTE = ("  /* Unbounded + Inter Tight (SIL OFL 1.1), subset to "
             "latin/cyrillic/cyrillic-ext, inlined as data URIs */\n")


def data_uri(path: pathlib.Path) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()


def main() -> int:
    html = SRC.read_text(encoding="utf-8")

    for token in ("/*FONTS*/", *SHOTS):
        found = html.count(token)
        if found != 1:
            print(f"error: expected {token} exactly once, found {found}", file=sys.stderr)
            return 1

    html = html.replace("/*FONTS*/", FONT_NOTE + FONTS.read_text(encoding="utf-8"), 1)
    for token, name in SHOTS.items():
        html = html.replace(token, data_uri(ROOT / "assets" / name), 1)

    OUT.write_text(html, encoding="utf-8")
    print(f"built {OUT.name}: {OUT.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
