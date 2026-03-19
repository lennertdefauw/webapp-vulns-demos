#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║     SQL Injection — Demo Environment     ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""

cd "$SCRIPT_DIR"

echo "  [*] Building and starting containers..."
echo ""

docker compose -p webapp-vulns-sqli up --build -d

echo ""
echo "  ✓ Containers started!"
echo ""
echo "  ┌─────────────────────────────────────────┐"
echo "  │  Frontend   →  http://localhost:38080   │"
echo "  └─────────────────────────────────────────┘"
echo ""
echo "  Containers:"
echo "    webapp-vulns-sqli-db"
echo "    webapp-vulns-sqli-backend"
echo "    webapp-vulns-sqli-frontend"
echo ""
echo "  Quick payloads to try:"
echo "    Auth bypass   →  ' OR '1'='1' -- -"
echo "    Login as user →  admin' -- -"
echo "    UNION dump    →  ' UNION SELECT 1,username,password,role,email FROM users -- -"
echo ""
