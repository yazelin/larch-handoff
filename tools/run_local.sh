#!/bin/bash
# 本機執行產圖：從本機設定讀服務網址與金鑰（不進 repo）
cd "$(dirname "$0")"
export CODEX_IMAGE_BASE=$(grep -m1 '^BASE = ' ~/larch-taoyuan/buchan/cg_jobs.py | cut -d'"' -f2)
source <(grep '^export CODEX_IMAGE_KEY' ~/.bashrc)
for stage in "$@"; do
  echo "== stage: $stage"
  python3 cg_jobs.py $stage
done
