#!/usr/bin/env python3
"""Update Snapcast version in all Dockerfiles."""
from __future__ import annotations

import argparse
import glob
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

RE_VERSION = re.compile(r"^(ARG\s+snapcast_version=)(?P<version>[0-9]+\.[0-9]+\.[0-9]+)\s*$", re.MULTILINE)
GITHUB_API = "https://api.github.com/repos/badaix/snapcast/releases/latest"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bump the Snapcast version used by all snapcast images.")
    parser.add_argument(
        "--files",
        nargs="*",
        type=pathlib.Path,
        help="Specific Dockerfile(s) to update (defaults to all Dockerfiles with ARG snapcast_version).",
    )
    parser.add_argument(
        "--version",
        help="Snapcast version to set (defaults to the latest GitHub release).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned changes without modifying the Dockerfiles.",
    )
    return parser.parse_args()


def find_dockerfiles() -> list[pathlib.Path]:
    """Find all Dockerfiles that contain ARG snapcast_version."""
    pattern = "**/Dockerfile*"
    dockerfiles = []
    
    for dockerfile_path in glob.glob(pattern, recursive=True):
        path_obj = pathlib.Path(dockerfile_path)
        try:
            contents = path_obj.read_text(encoding="utf-8")
            if RE_VERSION.search(contents):
                dockerfiles.append(path_obj)
        except (FileNotFoundError, UnicodeDecodeError):
            continue
    
    return dockerfiles


def fetch_latest_version() -> str:
    request = urllib.request.Request(GITHUB_API, headers={"User-Agent": "mopidy-icesnap-version-bot"})
    token = os.getenv("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.URLError as exc:  # pragma: no cover - network failure reported upstream
        raise SystemExit(f"Failed to fetch latest Snapcast release: {exc}") from exc

    tag_name = payload.get("tag_name")
    if not tag_name:
        raise SystemExit("Snapcast release payload did not contain tag_name")

    return tag_name.lstrip("v")


def read_current_version(text: str) -> str:
    match = RE_VERSION.search(text)
    if not match:
        raise SystemExit("Could not find ARG snapcast_version line in Dockerfile")
    return match.group("version")


def update_text(text: str, new_version: str) -> str:
    return RE_VERSION.sub(lambda match: f"{match.group(1)}{new_version}", text, count=1)


def main() -> int:
    args = parse_args()
    
    # Determine which Dockerfiles to update
    if args.files:
        dockerfiles = [path for file_path in args.files if (path := pathlib.Path(file_path)).exists()]
        if not dockerfiles:
            raise SystemExit("None of the specified Dockerfiles exist")
    else:
        dockerfiles = find_dockerfiles()
        if not dockerfiles:
            raise SystemExit("No Dockerfiles with ARG snapcast_version found")

    desired_version = (args.version or fetch_latest_version()).lstrip("v")
    
    updated_files = []
    no_change_files = []
    
    for dockerfile in dockerfiles:
        try:
            contents = dockerfile.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"Warning: Dockerfile not found: {dockerfile}")
            continue

        current_version = read_current_version(contents)

        if desired_version == current_version:
            no_change_files.append((dockerfile, current_version))
            continue

        updated_contents = update_text(contents, desired_version)
        updated_files.append((dockerfile, current_version, desired_version))

        if not args.dry_run:
            dockerfile.write_text(updated_contents, encoding="utf-8")

    # Report results
    if args.dry_run:
        print(f"Would bump snapcast_version to {desired_version} in:")
        for dockerfile, old_version, new_version in updated_files:
            print(f"  {dockerfile} ({old_version} -> {new_version})")
    else:
        print(f"Updated snapcast_version to {desired_version} in:")
        for dockerfile, old_version, new_version in updated_files:
            print(f"  {dockerfile} ({old_version} -> {new_version})")
    
    for dockerfile, current_version in no_change_files:
        print(f"  {dockerfile} already at {current_version}")

    return 0


if __name__ == "__main__":
    sys.exit(main())