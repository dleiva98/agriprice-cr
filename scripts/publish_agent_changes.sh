#!/usr/bin/env bash
set -euo pipefail

# Publica en main los commits hechos por el agente en esta sesión.
# Uso:
#   bash scripts/publish_agent_changes.sh <GITHUB_REPO_URL>
# Ejemplo:
#   bash scripts/publish_agent_changes.sh https://github.com/dleiva98/agriprice-cr.git

REPO_URL="${1:-}"
if [[ -z "$REPO_URL" ]]; then
  echo "Uso: bash scripts/publish_agent_changes.sh <GITHUB_REPO_URL>"
  exit 1
fi

if git remote | grep -q '^origin$'; then
  git remote set-url origin "$REPO_URL"
else
  git remote add origin "$REPO_URL"
fi

# Commits locales del agente pendientes de publicar.
COMMITS=(
  5f58375
  67aad83
  131bcad
  f926736
)

git fetch origin || true
git checkout -B main

for c in "${COMMITS[@]}"; do
  git cherry-pick "$c" || {
    echo "Cherry-pick falló en $c. Resuelve conflictos y luego ejecuta: git cherry-pick --continue"
    exit 1
  }
done

git push -u origin main

echo "✅ Cambios publicados en main"
