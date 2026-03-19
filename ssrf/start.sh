#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║      SSRF — Demo Environment                ║"
echo "  ╚══════════════════════════════════════════════╝"
echo ""

cd "$SCRIPT_DIR"

echo "  [*] Building and starting containers..."
echo ""

docker compose -p webapp-vulns-ssrf up --build -d

echo ""
echo "  ✓ Containers started!"
echo ""
echo "  ┌──────────────────────────────────────────────────────────┐"
echo "  │  LinkProbe UI  →  http://localhost:38085                 │"
echo "  │  Internal svc  →  NOT exposed (Docker network only)      │"
echo "  └──────────────────────────────────────────────────────────┘"
echo ""
echo "  Demo flow:"
echo "    1. Open http://localhost:38085"
echo "    2. Click an 'internal' chip (red) — e.g. internal /credentials"
echo "    3. The backend fetches it server-side and returns the response"
echo "    4. Your browser cannot reach webapp-vulns-ssrf-internal directly"
echo ""
echo "  Containers:"
echo "    webapp-vulns-ssrf-backend"
echo "    webapp-vulns-ssrf-internal  (no host port — internal only)"
echo "    webapp-vulns-ssrf-frontend"
echo ""
