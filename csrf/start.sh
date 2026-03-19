#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║      CSRF — Demo Environment                ║"
echo "  ╚══════════════════════════════════════════════╝"
echo ""

cd "$SCRIPT_DIR"

echo "  [*] Building and starting containers..."
echo ""

docker compose -p webapp-vulns-csrf up --build -d

echo ""
echo "  ✓ Containers started!"
echo ""
echo "  ┌─────────────────────────────────────────────┐"
echo "  │  Bank (victim)  →  http://localhost:38083   │"
echo "  │  Attacker page  →  http://localhost:38084   │"
echo "  └─────────────────────────────────────────────┘"
echo ""
echo "  Demo flow:"
echo "    1. Log in as alice at http://localhost:38083"
echo "    2. Visit the attacker page at http://localhost:38084"
echo "    3. Watch the CSRF attack drain alice's balance"
echo ""
echo "  Containers:"
echo "    webapp-vulns-csrf-backend"
echo "    webapp-vulns-csrf-bank"
echo "    webapp-vulns-csrf-attacker"
echo ""
