#!/usr/bin/env bash
# Download COUGHVID v1.0 (CC BY 4.0) from Zenodo record 4048312 into data/coughvid.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/coughvid
URL="https://zenodo.org/api/records/4048312/files/public_dataset.zip/content"
# -C - resumes a partial download; -L follows redirects; -f fails on HTTP errors
[ -f data/coughvid/public_dataset.zip ] || curl -fL -C - -o data/coughvid/public_dataset.zip "$URL"
[ -d data/coughvid/public_dataset ] || unzip -q data/coughvid/public_dataset.zip -d data/coughvid
echo "recordings: $(find data/coughvid -name '*.webm' -o -name '*.ogg' | wc -l)"
echo "metadata: $(ls data/coughvid/public_dataset/*.csv 2>/dev/null)"
