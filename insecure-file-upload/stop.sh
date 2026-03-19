#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

echo ""
echo "  [*] Stopping Insecure File Upload demo containers..."
docker compose -p webapp-vulns-insecure-file-upload down
echo "  ✓ Done."
echo ""
