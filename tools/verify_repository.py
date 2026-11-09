#!/usr/bin/env python3
"""Host-only repository integrity checks. No network or phone operations."""

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SHA256SUMS.txt"


def repository_files():
    return sorted(
        p for p in ROOT.rglob("*")
        if p.is_file()
        and p != MANIFEST
        and not {".git", "__pycache__"}.intersection(p.relative_to(ROOT).parts)
        and p.suffix != ".pyc"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()
    files = repository_files()
    actual = {
        p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in files
    }
    if args.write_manifest:
        with MANIFEST.open("w", encoding="utf-8", newline="\n") as out:
            out.write("".join(f"{digest}  {name}\n" for name, digest in actual.items()))

    errors = []
    expected = {}
    if not MANIFEST.exists():
        errors.append("missing SHA256SUMS.txt")
    else:
        for line in MANIFEST.read_text(encoding="utf-8").splitlines():
            match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
            if not match:
                errors.append("malformed checksum entry")
                continue
            digest, name = match.groups()
            if name in expected:
                errors.append(f"duplicate checksum entry: {name}")
            expected[name] = digest
    for name in sorted(expected.keys() | actual.keys()):
        if expected.get(name) != actual.get(name):
            errors.append(f"missing, unexpected, or modified file: {name}")

    json_count = link_count = 0
    for path in files:
        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
                json_count += 1
            except (ValueError, UnicodeError) as exc:
                errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        if path.suffix != ".md":
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", path.read_text(encoding="utf-8")):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(ROOT) or not destination.exists():
                errors.append(f"invalid local link in {path.relative_to(ROOT)}: {target}")
            link_count += 1

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {len(actual)} file checksums, {json_count} JSON files, {link_count} local link targets")
    print("Experimental validity, external URLs, and heading anchors are not checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
