#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
pip install -r requirements.txt

mkdir -p data/raw/precios/pdfs data/processed models

echo "Proyecto inicializado. Siguiente paso: correr scripts de ingesta y entrenamiento."
