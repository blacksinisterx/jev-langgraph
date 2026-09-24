#!/usr/bin/env bash
# api/app is a deliberate copy of backend/app, not a symlink -- Vercel's
# Python bundler only reliably includes files inside the function's own
# directory. Run this after changing anything in backend/app/ and before
# deploying, or the live site will serve stale logic.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf api/app
cp -r backend/app api/app
find api/app -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
echo "synced backend/app -> api/app"
