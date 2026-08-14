"""filecheck.py — file integrity checker.

--init  : creates a baseline hash manifest for a directory
--scan  : compares current state against the baseline, reports changes
"""

import hashlib
import json
import os
from pathlib import Path

MANIFEST_NAME = ".techastuceskit_manifest.json"


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest(directory: Path) -> dict:
    manifest = {}
    for root, _, files in os.walk(directory):
        if MANIFEST_NAME in files:
            files = [f for f in files if f != MANIFEST_NAME]
        for name in files:
            full_path = Path(root) / name
            rel_path = str(full_path.relative_to(directory))
            try:
                manifest[rel_path] = hash_file(full_path)
            except (PermissionError, OSError):
                continue
    return manifest


def init_baseline(directory: Path):
    manifest = build_manifest(directory)
    manifest_path = directory / MANIFEST_NAME
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"✅ Baseline created: {len(manifest)} files indexed in {manifest_path}")


def scan(directory: Path):
    manifest_path = directory / MANIFEST_NAME
    if not manifest_path.exists():
        print(f"❌ No baseline found. Run this first: techastuceskit filecheck {directory} --init")
        return

    with open(manifest_path) as f:
        old_manifest = json.load(f)

    new_manifest = build_manifest(directory)

    added = [f for f in new_manifest if f not in old_manifest]
    removed = [f for f in old_manifest if f not in new_manifest]
    modified = [
        f for f in new_manifest
        if f in old_manifest and new_manifest[f] != old_manifest[f]
    ]

    if not added and not removed and not modified:
        print("✅ No changes detected — everything's intact.")
        return

    if added:
        print(f"\n🟢 Added ({len(added)}):")
        for f in added:
            print(f"  + {f}")
    if modified:
        print(f"\n🟠 Modified ({len(modified)}):")
        for f in modified:
            print(f"  ~ {f}")
    if removed:
        print(f"\n🔴 Removed ({len(removed)}):")
        for f in removed:
            print(f"  - {f}")


def run(args):
    directory = Path(args.path).resolve()
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        return

    if args.init:
        init_baseline(directory)
    else:
        scan(directory)
