"""
Build huv.html (standalone) AND patch worker.js with the HUV page content.

Inputs:
  scripts/huv_page_template.html               — template with {{HUV_TRAJ_JSON}} marker
  simulation/data/huv_test/huv_trajectories.json — sim output

Outputs:
  huv.html                                      — committed; opens standalone
  worker.js                                     — patched between
                                                  /* HUV_PAGE_BEGIN */ … /* HUV_PAGE_END */

Run:  PYTHONPATH=. python scripts/build_huv_page.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT      = Path(__file__).resolve().parent.parent
TEMPLATE  = ROOT / "scripts" / "huv_page_template.html"
JSON_PATH = ROOT / "simulation" / "data" / "huv_test" / "huv_trajectories.json"
HUV_HTML  = ROOT / "huv.html"
WORKER_JS = ROOT / "worker.js"

JSON_MARKER       = "{{HUV_TRAJ_JSON}}"
WORKER_BEGIN_TAG  = "/* HUV_PAGE_BEGIN */"
WORKER_END_TAG    = "/* HUV_PAGE_END */"


def build_huv_html() -> str:
    template = TEMPLATE.read_text()
    raw_json = JSON_PATH.read_text().strip()
    json.loads(raw_json)
    if JSON_MARKER not in template:
        raise SystemExit(f"placeholder {JSON_MARKER!r} not found in template")
    html = template.replace(JSON_MARKER, raw_json)
    HUV_HTML.write_text(html)
    print(f"  wrote  {HUV_HTML.relative_to(ROOT)}  ({len(html):,} bytes)")
    return html


def patch_worker(huv_html: str) -> None:
    if not WORKER_JS.exists():
        print("  skip   worker.js (not present)")
        return
    src = WORKER_JS.read_text()
    if WORKER_BEGIN_TAG not in src or WORKER_END_TAG not in src:
        print(f"  skip   worker.js (markers {WORKER_BEGIN_TAG!r} / {WORKER_END_TAG!r} not found)")
        return

    # Embed the HUV page as a JS template literal — escape backticks, ${, and backslashes.
    safe = (
        huv_html
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )
    embedded = (
        f"{WORKER_BEGIN_TAG}\n"
        f"const HUV_PAGE_HTML = `{safe}`;\n"
        f"{WORKER_END_TAG}"
    )

    pattern = re.compile(
        re.escape(WORKER_BEGIN_TAG) + r".*?" + re.escape(WORKER_END_TAG),
        re.DOTALL,
    )
    new_src = pattern.sub(lambda _: embedded, src)
    WORKER_JS.write_text(new_src)
    print(f"  patch  {WORKER_JS.relative_to(ROOT)}  "
          f"({len(huv_html):,} bytes embedded between {WORKER_BEGIN_TAG} … {WORKER_END_TAG})")


def main() -> None:
    huv_html = build_huv_html()
    patch_worker(huv_html)


if __name__ == "__main__":
    main()
