#!/usr/bin/env bash
# Cloudflare Pages build entry point.  Keeps the build command short
# enough to type by hand on mobile without triggering chat-client
# autolinking of *.py filenames.
set -euo pipefail
python scripts/build_huv_page.py
