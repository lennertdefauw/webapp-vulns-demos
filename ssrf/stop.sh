#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

echo ""
echo "  [*] Stopping SSRF demo containers..."
docker compose -p webapp-vulns-ssrf down
echo "  ✓ Done."
