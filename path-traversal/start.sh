#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║   Path Traversal — Demo Environment     ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""

cd "$SCRIPT_DIR"

echo "  [*] Building and starting containers..."
echo ""

docker compose -p webapp-vulns-pathtrav up --build -d

echo ""
echo "  ✓ Containers started!"
echo ""
echo "  ┌─────────────────────────────────────────┐"
echo "  │  Frontend   →  http://localhost:38081   │"
echo "  └─────────────────────────────────────────┘"
echo ""
echo "  Containers:"
echo "    webapp-vulns-pathtrav-backend"
echo "    webapp-vulns-pathtrav-frontend"
echo ""
echo "  Quick payloads to try:"
echo "    App files     →  ../secret/credentials.txt"
echo "    Config leak   →  ../config/database.conf"
echo "    /etc/passwd   →  ../../../../etc/passwd"
echo "    /etc/hosts    →  ../../../../etc/hosts"
echo ""
