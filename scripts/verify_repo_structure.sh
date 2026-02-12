#!/usr/bin/env bash
set -euo pipefail

required_files=(
  ".github/workflows/scrape_weekly.yml"
  ".github/workflows/train_weekly.yml"
  "README.md"
  "docs/roadmap_mlops_cr.md"
  "configs/base.yaml"
  "requirements.txt"
  "setup_proyecto.sh"
  "src/data/fetch_pima_cenada.py"
  "src/features/build_features.py"
  "src/models/train.py"
)

missing=0
for f in "${required_files[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "MISSING: $f"
    missing=1
  fi
done

if [[ "$missing" -eq 1 ]]; then
  echo "\n❌ Faltan archivos del scaffold."
  exit 1
fi

echo "✅ Estructura del scaffold completa."
