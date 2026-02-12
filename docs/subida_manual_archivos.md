# Subida manual a GitHub cuando solo aparece `.gitkeep`

Este documento te dice exactamente **qué archivos subir** y **en qué orden** si vas a usar el botón de **Upload files** en GitHub.

## 0) Estructura mínima que debes subir

1. `.github/workflows/scrape_weekly.yml`
2. `.github/workflows/train_weekly.yml`
3. `README.md`
4. `requirements.txt`
5. `setup_proyecto.sh`
6. `configs/base.yaml`
7. `docs/roadmap_mlops_cr.md`
8. `docs/publicar_en_github.md`
9. `scripts/verify_repo_structure.sh`
10. `src/data/fetch_openmeteo.py`
11. `src/data/fetch_worldbank.py`
12. `src/features/build_features.py`
13. `src/models/train.py`

---

## 1) Orden recomendado de subida en GitHub Web

### Commit 1 — Base del proyecto
Sube primero:
- `README.md`
- `requirements.txt`
- `setup_proyecto.sh`
- `configs/base.yaml`

Mensaje de commit sugerido:
`chore: add base project files`

### Commit 2 — Código fuente
Sube:
- `src/data/fetch_openmeteo.py`
- `src/data/fetch_worldbank.py`
- `src/features/build_features.py`
- `src/models/train.py`

Mensaje sugerido:
`feat: add data ingestion, feature engineering and training scripts`

### Commit 3 — Workflows de automatización
Sube:
- `.github/workflows/scrape_weekly.yml`
- `.github/workflows/train_weekly.yml`

Mensaje sugerido:
`ci: add weekly data and training workflows`

### Commit 4 — Documentación/ayuda
Sube:
- `docs/roadmap_mlops_cr.md`
- `docs/publicar_en_github.md`
- `scripts/verify_repo_structure.sh`

Mensaje sugerido:
`docs: add roadmap and publishing/verification guides`

---

## 2) Alternativa rápida (1 solo commit)

Si quieres hacerlo en un solo paso, sube todos los archivos de la lista del punto 0 en un único commit.

Mensaje sugerido:
`chore: bootstrap agriprice-cr scaffold`

---

## 3) Verificación final (obligatoria)

Cuando termines, en la raíz del repo de GitHub debes ver estas carpetas/archivos:
- `.github/`
- `configs/`
- `docs/`
- `scripts/`
- `src/`
- `README.md`
- `requirements.txt`
- `setup_proyecto.sh`

Si eso aparece, ya quedó bien subido.
