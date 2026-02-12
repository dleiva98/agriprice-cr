# Evidencia de cambios (PIMA/CENADA)

Este archivo existe para que puedas verificar rápidamente que los cambios sí quedaron en el repo.

## Commits clave

```bash
git log --oneline -n 10
```

Debes ver commits recientes con estos temas:
- `shift pipeline to PIMA/CENADA-first data flow`
- `clean duplicated source bullet in roadmap`

## Archivos críticos que deben existir

```bash
git ls-tree --name-only -r HEAD | rg "fetch_pima_cenada|pima_cenada_data|scrape_weekly|build_features|train.py"
```

Esperado:
- `src/data/fetch_pima_cenada.py`
- `src/features/build_features.py`
- `.github/workflows/scrape_weekly.yml`
- `docs/pima_cenada_data.md`

## Qué hace cada parte

1. `python -m src.data.fetch_pima_cenada`
   - Genera: `data/raw/pima/boletin_links.csv`
2. `python -m src.features.build_features`
   - Usa: `data/raw/pima/pima_prices.csv`
   - Genera: `data/processed/features.csv`
3. `python -m src.models.train`
   - Genera: `models/metrics.json`, `models/predictions.csv`, `models/predictions_plot.png`

## ¿Necesitas secrets?

No para PIMA/CENADA.

Solo para APIs privadas (por ejemplo BCCR) cuando las integremos.
