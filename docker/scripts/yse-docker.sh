#!/usr/bin/env bash
# Wrapper for local YSE Docker workflows with automatic post-success pruning.
#
# Usage (from repo root or docker/):
#   ./docker/scripts/yse-docker.sh up          # compose up -d, light prune
#   ./docker/scripts/yse-docker.sh pull        # pull web image, prune old layers
#   ./docker/scripts/yse-docker.sh rebuild     # local dev image build + up, aggressive prune
#   ./docker/scripts/yse-docker.sh prune       # prune only
#   ./docker/scripts/yse-docker.sh down        # compose down (keeps DB volume)
#
# Set YSE_DOCKER_PRUNE=0 to skip pruning for a single invocation.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$DOCKER_DIR"

COMPOSE=(docker compose -f docker-compose.yml)
if [[ "${YSE_DOCKER_BUILD_LOCAL:-0}" == "1" ]]; then
  COMPOSE+=( -f docker-compose.dev.yml )
fi

run_prune() {
  local mode="${1:-light}"
  if [[ "${YSE_DOCKER_PRUNE:-1}" == "0" ]]; then
    echo "==> Skipping prune (YSE_DOCKER_PRUNE=0)"
    return 0
  fi
  bash "$SCRIPT_DIR/prune-yse-docker.sh" "$mode"
}

usage() {
  cat <<'EOF'
YSE Docker helper (auto-prunes superseded images after success)

  yse-docker.sh up       Start stack (docker compose up -d)
  yse-docker.sh pull     Pull ghcr.io/davecoulter/yse_pz:latest and prune old copies
  yse-docker.sh rebuild  Build local dev web image, start stack, aggressive prune
  yse-docker.sh prune    Prune only (--aggressive optional second arg)
  yse-docker.sh down     Stop stack (does not delete MySQL volume)

Environment:
  YSE_DOCKER_PRUNE=0     Disable automatic prune for one command
  YSE_DOCKER_BUILD_LOCAL=1  Use docker-compose.dev.yml (set automatically by rebuild)

MySQL data lives in VOL_DB from .env and is never removed by these commands.
Use: docker compose down -v   only if you intentionally want a fresh database.
EOF
}

cmd="${1:-up}"
shift || true

case "$cmd" in
  up)
    "${COMPOSE[@]}" up -d "$@"
    run_prune light
    ;;
  pull)
    docker pull ghcr.io/davecoulter/yse_pz:latest
    run_prune aggressive
    ;;
  rebuild)
    export YSE_DOCKER_BUILD_LOCAL=1
    COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.dev.yml)
    "${COMPOSE[@]}" build "$@"
    "${COMPOSE[@]}" up -d
    run_prune aggressive
    ;;
  prune)
    aggressive="${1:-light}"
    run_prune "$aggressive"
    ;;
  down)
    "${COMPOSE[@]}" down "$@"
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    usage >&2
    exit 1
    ;;
esac
