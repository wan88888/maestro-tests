#!/usr/bin/env python3
"""Run downloader site tests from config/sites.yaml."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from generate_suites import (
    CONFIG,
    group_flow_path,
    generate_all,
    load_config,
    site_env_cli,
)

ROOT = Path(__file__).resolve().parents[1]
FLOW = ROOT / "download_site.yaml"


def build_single_site_command(
    site_key: str,
    sites: dict[str, dict[str, str]],
    *,
    teardown: bool,
) -> list[str]:
    if site_key not in sites:
        raise SystemExit(f"Unknown site: {site_key}")

    return ["maestro", "test", *site_env_cli(sites[site_key], teardown=teardown), str(FLOW)]


def build_group_command(group: str, groups: dict[str, list[str]]) -> list[str]:
    if group not in groups:
        raise SystemExit(f"Unknown group: {group}")

    generate_all(ROOT)
    return ["maestro", "test", str(group_flow_path(group, ROOT))]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", help="Site key or group name")
    parser.add_argument("--list", action="store_true", help="List configured site keys")
    parser.add_argument("--list-groups", action="store_true", help="List configured groups")
    parser.add_argument("--group", action="store_true", help="Treat target as a group name")
    parser.add_argument("--generate", action="store_true", help="Regenerate download_*_video.yaml files")
    parser.add_argument("--teardown", action="store_true", help="Force teardown on single-site run")
    parser.add_argument("--dry-run", action="store_true", help="Print maestro command only")
    args = parser.parse_args(argv)

    sites, groups = load_config(CONFIG)

    if args.generate:
        for path in generate_all(ROOT):
            print(path)
        return 0

    if args.list_groups:
        for name in sorted(groups):
            members = ", ".join(groups[name])
            print(f"{name}\t{members}")
        return 0

    if args.list:
        for key in sorted(sites):
            url = sites[key].get("url", "")
            strategy = sites[key].get("tap_strategy", "")
            print(f"{key}\t{url}\t{strategy}")
        return 0

    if not args.target:
        parser.error("site/group key required (or use --list / --list-groups / --generate)")

    if args.group:
        cmd = build_group_command(args.target, groups)
    else:
        cmd = build_single_site_command(args.target, sites, teardown=args.teardown)

    print(" ".join(cmd))
    if args.dry_run:
        return 0

    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
