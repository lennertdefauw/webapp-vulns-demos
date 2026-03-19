#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║      XSS — Demo Environment                 ║"
echo "  ╚══════════════════════════════════════════════╝"
echo ""

cd "$SCRIPT_DIR"

echo "  [*] Building and starting containers..."
echo ""

docker compose -p webapp-vulns-xss up --build -d

echo ""
echo "  ✓ Containers started!"
echo ""
echo "  ┌──────────────────────────────────────────────────────────────┐"
echo "  │  XSS Demo  →  http://localhost:38086                        │"
echo "  │                                                              │"
echo "  │  Tab 1: Stored XSS    — post a payload, hits all visitors   │"
echo "  │  Tab 2: Reflected XSS — payload in URL, craft a link        │"
echo "  └──────────────────────────────────────────────────────────────┘"
echo ""
echo "  Containers:"
echo "    webapp-vulns-xss-backend"
echo "    webapp-vulns-xss-frontend"
echo ""
