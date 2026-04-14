#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"
ENV_FILE="${ENV_FILE:-.env}"

usage() {
  echo "Usage: $0 {up|down|pull|logs|ps|backup-db}"
  echo ""
  echo "Environment:"
  echo "  COMPOSE_FILE  default: docker-compose.prod.yml"
  echo "  ENV_FILE      default: .env"
}

require_env_file() {
  if [[ ! -f "$ENV_FILE" ]]; then
    echo "Missing $ENV_FILE — copy .env.example and configure it."
    exit 1
  fi
}

cmd_up() {
  require_env_file
  docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d "$@"
}

cmd_down() {
  require_env_file
  docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" down "$@"
}

cmd_pull() {
  docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" pull
}

cmd_logs() {
  require_env_file
  docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" logs -f --tail=200
}

cmd_ps() {
  require_env_file
  docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" ps
}

cmd_backup_db() {
  require_env_file
  TS="$(date +%Y%m%d_%H%M%S)"
  OUT="backup_postgres_${TS}.sql.gz"
  echo "Writing $OUT ..."
  docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" exec -T postgres \
    sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' | gzip > "$OUT"
  echo "Done: $OUT"
}

case "${1:-}" in
  up) shift; cmd_up "$@" ;;
  down) shift; cmd_down "$@" ;;
  pull) shift; cmd_pull "$@" ;;
  logs) shift; cmd_logs "$@" ;;
  ps) cmd_ps ;;
  backup-db) cmd_backup_db ;;
  ""|-h|--help) usage ;;
  *) echo "Unknown command: $1"; usage; exit 1 ;;
esac
