#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

echo ""
echo "  [*] Stopping Path Traversal demo containers..."
docker compose -p webapp-vulns-pathtrav down
echo "  ✓ Done."
echo ""
