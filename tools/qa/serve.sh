#!/bin/sh
# Serve a test copy of the built site (docs/) with window.__dw exposed for the QA scripts.
# Usage: sh tools/qa/serve.sh [dir] [port]   (defaults: /tmp/wardrobe-qa, 8770). Rebuild docs first:
#   python3 tools/build_site.py --out docs
D=${1:-/tmp/wardrobe-qa}; P=${2:-8770}; R=$(cd "$(dirname "$0")/../.." && pwd)
rm -rf "$D" && mkdir -p "$D" && cp -r "$R/docs/." "$D/" && python3 "$R/tools/qa/inject.py" "$D/index.html"
echo "serving $D on http://localhost:$P (QA_PORT=$P for the scripts)"
exec python3 -m http.server "$P" --directory "$D"
