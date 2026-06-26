#!/usr/bin/env python3
"""Generate download_*_video.yaml suite files from config/sites.yaml."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "sites.yaml"

ENV_FIELDS = [
    ("SITE_URL", "url"),
    ("READY_TEXT", "ready_text"),
    ("TAP_STRATEGY", "tap_strategy"),
    ("TAP_X", "tap_x"),
    ("TAP_Y", "tap_y"),
    ("DOWNLOAD_STYLE", "download_style"),
    ("TEARDOWN_MODE", "teardown_mode"),
    ("DISMISS_AGE", "dismiss_age"),
    ("DISMISS_OK", "dismiss_ok"),
    ("DISMISS_COOKIE", "dismiss_cookie"),
    ("DISMISS_ENTER", "dismiss_enter"),
]

GROUP_FILES = {
    "pornhub": "download_pornhub_video.yaml",
    "xvideos": "download_xvideos_video.yaml",
    "xnxx": "download_xnxx_video.yaml",
    "redtube": "download_redtube_video.yaml",
    "spankbang": "download_spankbang_video.yaml",
    "xhamster": "download_xhamster_video.yaml",
}


def load_config(path: Path = CONFIG) -> tuple[dict[str, dict[str, str]], dict[str, list[str]]]:
    sites: dict[str, dict[str, str]] = {}
    groups: dict[str, list[str]] = {}
    current_site: str | None = None
    current_group: str | None = None
    mode = "sites"

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        if re.match(r"^groups:\s*$", line):
            mode = "groups"
            current_site = None
            continue

        if mode == "sites":
            key_match = re.match(r"^([A-Za-z0-9_]+):\s*$", line)
            if key_match:
                current_site = key_match.group(1)
                sites[current_site] = {}
                continue

            if current_site is None:
                continue

            kv = re.match(r"^\s+([a-z_]+):\s*(.+?)\s*$", line)
            if not kv:
                continue

            field, value = kv.group(1), kv.group(2)
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            sites[current_site][field] = value
            continue

        group_match = re.match(r"^  ([a-z_]+):\s*$", line)
        if group_match:
            current_group = group_match.group(1)
            groups[current_group] = []
            continue

        item_match = re.match(r"^    - ([A-Za-z0-9_]+)\s*$", line)
        if item_match and current_group:
            groups[current_group].append(item_match.group(1))

    return sites, groups


def site_env_dict(site: dict[str, str], *, teardown: bool = False) -> dict[str, str]:
    env: dict[str, str] = {}

    for env_key, yaml_key in ENV_FIELDS:
        val = site.get(yaml_key)
        if val is not None:
            env[env_key] = val

    if site.get("scroll_before_tap", "").lower() == "true":
        env["SCROLL_BEFORE_TAP"] = "true"

    if site.get("home_probe", "").lower() == "true":
        env["HOME_PROBE"] = "true"

    if teardown or site.get("teardown", "").lower() == "true":
        env["TEARDOWN"] = "true"

    return env


def site_env_cli(site: dict[str, str], *, teardown: bool = False) -> list[str]:
    args: list[str] = []
    for key, val in site_env_dict(site, teardown=teardown).items():
        args.extend(["-e", f"{key}={val}"])
    return args


def _yaml_scalar(value: str) -> str:
    if not value:
        return '""'
    if any(ch in value for ch in "\"':{}[]&*#?|-<>=!%@`"):
        return '"' + value.replace('"', '\\"') + '"'
    return value


def _render_env_block(env: dict[str, str]) -> str:
    lines = ["    env:"]
    for key, val in env.items():
        lines.append(f"      {key}: {_yaml_scalar(val)}")
    return "\n".join(lines)


def render_group_suite(group: str, site_keys: list[str], sites: dict[str, dict[str, str]]) -> str:
    lines = [
        "# Generated from config/sites.yaml — do not edit by hand.",
        f"# Regenerate: python3 android/downloader/scripts/generate_suites.py",
        "appId: free.video.downloader.converter.music",
        "---",
        "- launchApp",
        "",
    ]

    for site_key in site_keys:
        if site_key not in sites:
            raise KeyError(f"group '{group}' references unknown site '{site_key}'")
        env = site_env_dict(sites[site_key])
        lines.append("- runFlow:")
        lines.append("    file: download_site.yaml")
        lines.append(_render_env_block(env))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def generate_all(root: Path = ROOT) -> list[Path]:
    sites, groups = load_config()
    written: list[Path] = []

    for group, site_keys in groups.items():
        filename = GROUP_FILES.get(group, f"download_{group}_video.yaml")
        out = root / filename
        out.write_text(render_group_suite(group, site_keys, sites), encoding="utf-8")
        written.append(out)

    return written


def group_flow_path(group: str, root: Path = ROOT) -> Path:
    filename = GROUP_FILES.get(group, f"download_{group}_video.yaml")
    return root / filename


def main() -> int:
    written = generate_all()
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
