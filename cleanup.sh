#!/bin/bash
# cleanup.sh — stop & remove all containers and networks for a given vuln slug
#
# Every demo container follows the pattern:  webapp-vulns-<slug>-<role>
#
# Usage:
#   ./cleanup.sh sqli        → cleans up webapp-vulns-sqli-*
#   ./cleanup.sh xss         → cleans up webapp-vulns-xss-*
#   ./cleanup.sh all         → cleans up ALL webapp-vulns-* resources
#   ./cleanup.sh             → lists all running webapp-vulns-* containers

set -e

GLOBAL_PREFIX="webapp-vulns"
SLUG="$1"

if [[ -z "$SLUG" ]]; then
  echo ""
  echo "  Usage: ./cleanup.sh <slug|all>"
  echo ""
  echo "  Running demo containers (all webapp-vulns-*):"
  docker ps --filter "name=${GLOBAL_PREFIX}-" \
            --format "  {{.Names}}\t{{.Status}}" 2>/dev/null || true
  echo ""
  exit 0
fi

if [[ "$SLUG" == "all" ]]; then
  FILTER="${GLOBAL_PREFIX}-"
else
  FILTER="${GLOBAL_PREFIX}-${SLUG}-"
fi

echo ""
echo "  [*] Cleaning up containers matching: ${FILTER}*"

# ── Stop & remove matching containers ─────────────────────────
CONTAINERS=$(docker ps -aq --filter "name=${FILTER}" 2>/dev/null)

if [[ -n "$CONTAINERS" ]]; then
  echo "  [*] Stopping containers..."
  docker stop $CONTAINERS > /dev/null

  echo "  [*] Removing containers..."
  docker rm   $CONTAINERS > /dev/null
else
  echo "  [i] No containers found matching '${FILTER}*'"
fi

# ── Remove matching networks ───────────────────────────────────
NETWORKS=$(docker network ls --filter "name=${FILTER}" -q 2>/dev/null)

if [[ -n "$NETWORKS" ]]; then
  echo "  [*] Removing networks..."
  docker network rm $NETWORKS > /dev/null
fi

echo "  ✓ Done. All '${FILTER}*' resources removed."
echo ""
