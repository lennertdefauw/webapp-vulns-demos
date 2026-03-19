#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

echo ""
echo "  [*] Stopping SQL Injection demo containers..."
docker compose -p webapp-vulns-sqli down
echo "  ✓ Done."
echo ""
