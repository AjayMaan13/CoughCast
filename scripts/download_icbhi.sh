#!/usr/bin/env bash
# Download the ICBHI 2017 database into data/icbhi. Needs .wav, .txt annotations, and the official split file.
# Source: https://bhichallenge.med.auth.gr/ICBHI_2017_Challenge
# TLS is verified on purpose. If the host's certificate is expired, this fails; do not add -k.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/icbhi
BASE="https://bhichallenge.med.auth.gr/sites/default/files/ICBHI_final_database"
[ -f data/icbhi/ICBHI_final_database.zip ] || curl -fL -C - -o data/icbhi/ICBHI_final_database.zip "$BASE/ICBHI_final_database.zip"
[ -d data/icbhi/ICBHI_final_database ] || unzip -q data/icbhi/ICBHI_final_database.zip -d data/icbhi
# Official train/test split: check the challenge page for the exact file URL
[ -f data/icbhi/ICBHI_challenge_train_test.txt ] || curl -fL -o data/icbhi/ICBHI_challenge_train_test.txt "$BASE/ICBHI_challenge_train_test.txt"
echo "wav files: $(find data/icbhi -name '*.wav' | wc -l)"
echo "annotation files: $(find data/icbhi/ICBHI_final_database -name '*.txt' | wc -l)"
echo "split lines: $(wc -l < data/icbhi/ICBHI_challenge_train_test.txt)"
