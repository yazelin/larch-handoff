#!/bin/bash
# 本機執行產圖與配樂：從本機設定讀服務網址與金鑰（不進 repo）
#   tools/run_local.sh <stage…>          產圖
#   tools/run_local.sh music gen [名字…]  配樂
cd "$(dirname "$0")"
export CODEX_IMAGE_BASE=$(grep -m1 '^BASE = ' ~/larch-taoyuan/buchan/cg_jobs.py | cut -d'"' -f2)
source <(grep '^export CODEX_IMAGE_KEY' ~/.bashrc)
export GEMINI_WEB_MUSIC_URL=$(grep -m1 "^URL = " ~/larch-eleven-minutes/art/music.py | cut -d"'" -f2)
if [ "$1" = music ]; then shift; exec python3 music.py "$@"; fi
for stage in "$@"; do
  echo "== stage: $stage"
  python3 cg_jobs.py $stage
done
