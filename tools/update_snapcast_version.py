#!/usr/bin/env python3
"""Update Snapcast version in snapserver Dockerfile."""
from __future__ import annotations

import argparse
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
    parser = argparse.ArgumentParser(description="Bump the Snapcast version used by the snapserver image.")
    parser.add_argument(
        "--file",
        type=pathlib.Path,
        default=pathlib.Path("snapserver") / "Dockerfile",
        help="Path to the Dockerfile that declares ARG snapcast_version.",
    )
    parser.add_argument(
        "--version",
        help="Snapcast version to set (defaults to the latest GitHub release).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned change without modifying the Dockerfile.",
    )
    return parser.parse_args()


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
    dockerfile = args.file

    try:
        contents = dockerfile.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"Dockerfile not found: {dockerfile}")

    current_version = read_current_version(contents)

    desired_version = (args.version or fetch_latest_version()).lstrip("v")

    if desired_version == current_version:
        print(f"snapcast_version already at {current_version}")
        return 0

    updated_contents = update_text(contents, desired_version)

    if args.dry_run:
        print(f"Would bump snapcast_version from {current_version} to {desired_version}")
        return 0

    dockerfile.write_text(updated_contents, encoding="utf-8")
    print(f"Updated snapcast_version from {current_version} to {desired_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())