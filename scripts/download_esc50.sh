#!/usr/bin/env bash
# Download ESC-50 (CC BY-NC 3.0) into data/esc50. Needs audio/ and meta/esc50.csv.
set -euo pipefail                      # stop on any error, unset variable, or failed pipe
cd "$(dirname "$0")/.."                # run from the repo root, wherever the script is called from
mkdir -p data
if [ -d data/esc50/audio ]; then echo "data/esc50 already exists, skipping"; else
  # --depth 1: latest snapshot only, not the full history (saves several hundred MB)
  git clone --depth 1 https://github.com/karolpiczak/ESC-50.git data/esc50
fi
echo "wav files: $(ls data/esc50/audio/*.wav | wc -l)"
echo "metadata rows: $(($(wc -l < data/esc50/meta/esc50.csv) - 1))"
