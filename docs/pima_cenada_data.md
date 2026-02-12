# PIMA/CENADA: datos base para entrenar

Este proyecto usa **PIMA/CENADA** como fuente principal de precios en Costa Rica.

## 1) Descargar enlaces de boletines

```bash
python -m src.data.fetch_pima_cenada
```

Salida:
- `data/raw/pima/boletin_links.csv`

## 2) Crear tabla de precios para entrenamiento

Debes construir `data/raw/pima/pima_prices.csv` con este formato mínimo:

```csv
date,product,price
2024-01-05,tomate,850
2024-01-05,papa,620
2024-01-12,tomate,870
```

- `date`: fecha ISO (`YYYY-MM-DD`)
- `product`: nombre del producto
- `price`: precio numérico

## 3) Entrenar y evaluar

```bash
python -m src.features.build_features
python -m src.models.train
```

Artefactos:
- `models/metrics.json`
- `models/predictions.csv`
- `models/predictions_plot.png`

## ¿Necesito GitHub Secrets?

Para **PIMA/CENADA no** (fuente pública).

Solo necesitarás secrets si integras fuentes con autenticación (por ejemplo BCCR token).
