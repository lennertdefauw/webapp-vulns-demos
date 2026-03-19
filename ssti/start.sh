#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║      SSTI — Demo Environment                ║"
echo "  ╚══════════════════════════════════════════════╝"
echo ""

cd "$SCRIPT_DIR"

echo "  [*] Building and starting containers..."
echo ""

docker compose -p webapp-vulns-ssti up --build -d

echo ""
echo "  ✓ Containers started!"
echo ""
echo "  ┌─────────────────────────────────────────────┐"
echo "  │  CorpMailer UI  →  http://localhost:38087   │"
echo "  └─────────────────────────────────────────────┘"
echo ""
echo "  Demo flow:"
echo "    1. Open http://localhost:38087"
echo "    2. Use detection chips: {{7*7}} → 49 confirms Jinja2 execution"
echo "    3. Escalate: {{config}} leaks Flask internals"
echo "    4. RCE: {{lipsum.__globals__["os"].popen("id").read()}}"
echo ""
echo "  Containers:"
echo "    webapp-vulns-ssti-backend"
echo "    webapp-vulns-ssti-frontend"
echo ""
