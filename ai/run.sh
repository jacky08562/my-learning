#!/usr/bin/env bash
# 从 .env 读取配置后调用,免得每次手动 export
#   ./ai/run.sh "你的问题"
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "缺少 .env。先把 .env.example 复制成 .env,再填入自己的 Key。" >&2
  exit 1
fi

set -a; . ./.env; set +a
exec ./ai/01-first-call.sh "$@"
