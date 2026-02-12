#!/usr/bin/env bash
set -euo pipefail

# Resuelve conflictos tomando la versión local (--ours)
# para los archivos críticos del scaffold.

files=(
  ".github/workflows/scrape_weekly.yml"
  "README.md"
  "docs/roadmap_mlops_cr.md"
  "requirements.txt"
  "scripts/verify_repo_structure.sh"
  "setup_proyecto.sh"
  "src/features/build_features.py"
)

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "❌ Ejecuta este script dentro del repositorio git."
  exit 1
fi

unmerged="$(git diff --name-only --diff-filter=U || true)"
if [[ -z "$unmerged" ]]; then
  echo "ℹ️ No hay conflictos activos."
  exit 0
fi

for f in "${files[@]}"; do
  if echo "$unmerged" | grep -Fxq "$f"; then
    git checkout --ours -- "$f"
    git add "$f"
    echo "✅ Resuelto con versión local: $f"
  fi
done

remaining="$(git diff --name-only --diff-filter=U || true)"
if [[ -n "$remaining" ]]; then
  echo "⚠️ Quedan conflictos pendientes:"
  echo "$remaining"
  exit 1
fi

echo "✅ Conflictos resueltos en archivos objetivo."
