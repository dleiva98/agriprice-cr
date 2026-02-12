# Agriprice-CR: Predicción de precios agrícolas en Costa Rica

Proyecto base para construir un sistema **MLops cloud-first** que prediga precios de productos agrícolas usando:

- Históricos de precios (PIMA/CENADA u otras fuentes).
- Variables climatológicas (Open-Meteo / ERA5).
- Variables económicas (World Bank / BCCR).

## Arranque rápido (orden sugerido)

1. Crear repo en GitHub y subir este esqueleto.
2. Configurar secrets de GitHub (`BCCR_TOKEN`, opcionales).
3. Ejecutar pipeline inicial en Colab (entrenamiento).
4. Activar GitHub Actions para ingestión semanal.
5. Publicar API o dashboard (Hugging Face Spaces / Render / Cloud Run).

Guía paso a paso completa: `docs/roadmap_mlops_cr.md`.

## Estructura

```text
.github/workflows/      # Automatizaciones
configs/                # Configuración YAML
src/data/               # Ingesta de datos
src/features/           # Ingeniería de características
src/models/             # Entrenamiento y evaluación
data/                   # Artefactos de datos (opcional en repo)
models/                 # Modelos serializados
```

## Comandos base

```bash
pip install -r requirements.txt
python -m src.data.fetch_pima_cenada
# (opcional) coloca data/raw/pima/pima_prices.csv con columnas date,product,price
python -m src.features.build_features
python -m src.models.train
```

## Datos Costa Rica (PIMA/CENADA)

El flujo principal ahora está centrado en PIMA/CENADA:

1. `python -m src.data.fetch_pima_cenada` guarda enlaces de boletines en `data/raw/pima/boletin_links.csv`.
2. Debes extraer (manual o script) precios a `data/raw/pima/pima_prices.csv` con columnas: `date,product,price`.
3. `python -m src.features.build_features` usa ese CSV como fuente primaria de entrenamiento.

No necesitas secrets para PIMA (sitio público). Secrets solo son necesarios para futuras integraciones privadas (ej. BCCR token).

## Colab: entrenamiento sin errores (recomendado)

Si `python -m src.models.train` no muestra salida, usa esta secuencia exacta en Colab:

```bash
%cd /content/agriprice-cr
!pip install -r requirements.txt
!python -u -m src.data.fetch_pima_cenada
# sube o genera data/raw/pima/pima_prices.csv
!python -u -m src.features.build_features
!python -u src/models/train.py
!ls -lah models
!cat models/metrics.json
```

> Nota: si `xgboost` no está disponible, el script usa automáticamente `RandomForestRegressor` como fallback y aún genera `models/metrics.json`.

Resultados que debes revisar después de entrenar:

```bash
!cat models/metrics.json
!head -n 10 models/predictions.csv
```

Además se genera una gráfica: `models/predictions_plot.png` (actual vs predicción en test).


Opcional (con rutas explícitas):

```bash
!python -u src/models/train.py --features data/processed/features.csv --out-dir models
```

## Despliegue sugerido (sin depender de local)

- **Entrenamiento inicial**: Google Colab (GPU).
- **Ingesta recurrente**: GitHub Actions + almacenamiento en S3/GCS/DVC.
- **Registro de experimentos**: MLflow (Dagshub).
- **Serving**: FastAPI + contenedor en Cloud Run/Render.



## Verificación rápida de que los archivos existen en el repo

Si en GitHub no ves los archivos, normalmente es por una de estas razones:

1. Estás viendo otra rama distinta a la rama donde se hizo el commit.
2. Falta hacer `git push` de la rama actual al remoto.
3. La carpeta `.github/` es oculta en algunos exploradores locales (en GitHub sí se ve).

Comprobación local:

```bash
git ls-tree --name-only -r HEAD
```

Deberías ver, entre otros:

- `.github/workflows/scrape_weekly.yml`
- `.github/workflows/train_weekly.yml`
- `docs/roadmap_mlops_cr.md`
- `src/data/fetch_pima_cenada.py`
- `src/features/build_features.py`
- `src/models/train.py`



## Publicación en GitHub (importante)

Si en GitHub solo te aparece `.gitkeep`, revisa esta guía:

- `docs/publicar_en_github.md` (incluye caso Codespaces cuando no existe la rama `work`)

También puedes validar localmente la estructura con:

```bash
bash scripts/verify_repo_structure.sh
```


## Subida manual (si GitHub solo muestra `.gitkeep`)

Usa esta guía con el orden exacto de archivos a subir:

- `docs/subida_manual_archivos.md`


Guía detallada PIMA/CENADA: `docs/pima_cenada_data.md`.
Evidencia de cambios para verificar en GitHub: `docs/pr_evidence.md`.
