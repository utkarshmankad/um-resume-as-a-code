#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
"${PYTHON:-python3}" -m unittest discover -s tests -v
"${PYTHON:-python3}" -c "from scripts.validate_resume import validate_protected_sources; validate_protected_sources()"
compiler="${TECTONIC:-tectonic}"
if [[ "$($compiler --version)" != 'Tectonic 0.17.0' ]]; then
  echo 'Build requires Tectonic 0.17.0.' >&2
  exit 1
fi
mkdir -p build
"$compiler" --bundle https://relay.fullyjustified.net/default_bundle_v33.tar --keep-logs --outdir build main.tex
mv build/main.pdf build/Utkarsh-Mankad-Resume.pdf
"${PYTHON:-python3}" scripts/validate_resume.py
