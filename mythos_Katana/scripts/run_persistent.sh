#!/bin/bash
# Run the council forever on YOUR machine. No key is stored in this file.
#
#   1) put your key in the environment (or a file you own):
#        export OPENAI_API_KEY=...
#   2) ./scripts/run_persistent.sh
set -euo pipefail

: "${OPENAI_API_KEY:?set OPENAI_API_KEY first}"
export KATANA_LLM_PROVIDER="${KATANA_LLM_PROVIDER:-openai}"
export OPENAI_BASE_URL="${OPENAI_BASE_URL:-https://api.openai.com/v1}"
export KATANA_LLM_MODEL="${KATANA_LLM_MODEL:-gpt-4o-mini}"
export KATANA_LLM_TIMEOUT="${KATANA_LLM_TIMEOUT:-30}"
export KATANA_LLM_RETRIES="${KATANA_LLM_RETRIES:-1}"
export KATANA_LLM_BACKOFF="${KATANA_LLM_BACKOFF:-20}"

# persistent state next to the repo, survives reboots
export KATANA_LOG="${KATANA_LOG:-$PWD/.katana/scan.log}"
export KATANA_MEM="${KATANA_MEM:-$PWD/.katana/mem.json}"
mkdir -p "$(dirname "$KATANA_LOG")"

exec python3 -m agent.persistent
