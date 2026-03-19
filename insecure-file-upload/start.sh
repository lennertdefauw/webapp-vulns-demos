#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║  Insecure File Upload — Demo Environment  ║"
echo "  ╚══════════════════════════════════════════════╝"
echo ""

cd "$SCRIPT_DIR"

echo "  [*] Building and starting containers..."
echo ""

docker compose -p webapp-vulns-insecure-file-upload up --build -d

echo ""
echo "  ✓ Containers started!"
echo ""
echo "  ┌─────────────────────────────────────────┐"
echo "  │  Frontend   →  http://localhost:38082   │"
echo "  └─────────────────────────────────────────┘"
echo ""
echo "  Containers:"
echo "    webapp-vulns-insecure-file-upload-backend"
echo "    webapp-vulns-insecure-file-upload-frontend"
echo ""
