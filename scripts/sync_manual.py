#!/usr/bin/env python3
"""Render the manual's GCU firmware "## Releases" section from CHANGELOG.md.

GitHub (this repo) is the source of truth for GCU release notes. The owner's
manual (Rush-Auto-Works/manual.rush.sr) renders a mirror on the Legacy GCU page
`maintenance/electronics-and-wiring/gcu/legacy.md`. This script regenerates
ONLY that file's `## Releases` section from CHANGELOG.md so the two never drift;
the page's flashing instructions above `## Releases` are left untouched.

Usage:
  sync_manual.py render                       # print the Releases section
  sync_manual.py apply   <manual_repo_root>   # rewrite the manual page in place
  sync_manual.py --check <manual_repo_root>   # exit 1 if the page would change

Asset references point at `../../.gitbook/assets/rush_GCU_<version>.zip`; the
workflow copies each release zip there under that canonical name (dropping any
" (1)" GitBook upload suffix).
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CHANGELOG = HERE / "CHANGELOG.md"
MANUAL_PAGE = Path("maintenance/electronics-and-wiring/gcu/legacy.md")
ASSET_TMPL = "../../.gitbook/assets/rush_GCU_{version}.zip"
# Matches a real version heading ("3.1.0 — March 2026") but NOT prose headings
# like "3.0.3 and earlier", so the latter gets no download asset.
VERSION_RE = re.compile(r"^(\d+\.\d+\.\d+)(?:\s+—\s+.+)?$")


def parse_sections(changelog_text):
    """Yield (heading, body) for each `## ` section in CHANGELOG.md."""
    sections = []
    cur_head, cur_body = None, []
    for line in changelog_text.splitlines():
        if line.startswith("## "):
            if cur_head is not None:
                sections.append((cur_head, "\n".join(cur_body).strip()))
            cur_head, cur_body = line[3:].strip(), []
        elif cur_head is not None:
            cur_body.append(line)
    if cur_head is not None:
        sections.append((cur_head, "\n".join(cur_body).strip()))
    return sections


def render():
    out = ["## Releases", ""]
    for heading, body in parse_sections(CHANGELOG.read_text()):
        out.append(f"### {heading}")
        out.append("")
        if body:
            out.append(body)
            out.append("")
        m = VERSION_RE.match(heading)
        if m:
            out.append("{% file src=\"" + ASSET_TMPL.format(version=m.group(1)) + "\" %}")
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def splice(page_text, releases_section):
    """Replace everything from `## Releases` onward; keep the header intact."""
    idx = page_text.find("## Releases")
    if idx == -1:
        raise SystemExit("ERROR: '## Releases' marker not found in manual page")
    return page_text[:idx] + releases_section


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    if args[0] == "render":
        sys.stdout.write(render())
        return 0

    check = args[0] == "--check"
    if args[0] not in ("apply", "--check") or len(args) < 2:
        print(__doc__)
        return 2

    page = Path(args[1]) / MANUAL_PAGE
    if not page.exists():
        raise SystemExit(f"ERROR: manual page not found: {page}")

    current = page.read_text()
    updated = splice(current, render())

    if check:
        if current == updated:
            print("in sync: manual page matches CHANGELOG.md")
            return 0
        print("OUT OF SYNC: manual page would change. Run `apply` to update.")
        return 1

    if current == updated:
        print("no change")
        return 0
    page.write_text(updated)
    print(f"updated {page}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
