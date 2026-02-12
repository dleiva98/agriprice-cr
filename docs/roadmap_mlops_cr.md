# Roadmap ML/AI para predecir precios agrícolas en Costa Rica (cloud-first)

Este documento está diseñado para ejecutar el proyecto **sin depender de infraestructura local**. Se prioriza GitHub + Colab + servicios gratuitos.

---

## 1) Arquitectura objetivo

1. **Fuentes de datos**
   - Núcleo: PIMA/CENADA (boletines oficiales de precios; scraping + carga manual de respaldo).
   - Opcional fase 2: clima (Open-Meteo) y macro (BCCR/World Bank).
   - Política/mercado (plus): indicadores de riesgo país y eventos regulatorios.

2. **Data Lake ligero**
   - `data/raw/` para descargas crudas.
   - `data/processed/` para tablas limpias y feature store simple.
   - Escalable a S3/GCS + DVC cuando crezca.

3. **Entrenamiento**
   - Colab como entorno principal para entrenar el modelo inicial.
   - Modelo baseline: XGBoost/LightGBM con features de rezagos, clima, calendario.

4. **Seguimiento de experimentos**
   - MLflow (preferencia: Dagshub gratis).

5. **Automatización (MLOps)**
   - GitHub Actions semanal:
     - extraer nuevas observaciones,
     - reconstruir features,
     - correr validaciones de calidad,
     - opcionalmente reentrenar.

6. **Serving**
   - API FastAPI o dashboard Streamlit en cloud.

---

## 2) Plan operativo por fases

### Día 1 (30-45 min)

- [ ] Crear repo GitHub.
- [ ] Subir esta base del proyecto.
- [ ] Crear entorno en Colab (no local).
- [ ] Instalar dependencias.

**Comandos (en Colab o Codespaces):**

```bash
git clone <TU_REPO>
cd agriprice-cr
pip install -r requirements.txt
```

### Día 1-2 (60-90 min)

- [ ] Ejecutar scraping de boletines PIMA/CENADA.
- [ ] Extraer tabla de precios a `data/raw/pima/pima_prices.csv`.
- [ ] Si scraping PDF falla: carga manual desde boletines oficiales y continuar.

### Día 2-3 (2-3 horas)

- [ ] Construir features (`build_features.py`).
- [ ] Entrenar baseline (`train.py`).
- [ ] Revisar métricas (MAE, RMSE, MAPE).
- [ ] Guardar artefactos del modelo.

### Día 4+

- [ ] Registrar token/API de BCCR y enriquecer datos diarios.
- [ ] Activar workflow semanal en GitHub Actions.
- [ ] Integrar MLflow en Dagshub.
- [ ] Publicar endpoint de inferencia.
- [ ] Implementar monitoreo de drift.

---

## 3) Qué publicar en GitHub (mínimo viable)

1. Código de ingesta y entrenamiento (`src/`).
2. `requirements.txt` y/o `pyproject.toml`.
3. Workflows en `.github/workflows/`.
4. Configuración en `configs/base.yaml`.
5. Plantilla de uso en README.

No subir datos sensibles. Para PIMA/CENADA no se requieren secrets; usa GitHub Secrets solo para APIs privadas.

---

## 4) Uso recomendado de Colab

1. Runtime con GPU (si disponible).
2. Clonar repo.
3. Instalar dependencias.
4. Ejecutar pipeline por módulos.

```bash
python -m src.data.fetch_pima_cenada
python -m src.features.build_features
python -m src.models.train
```

5. Guardar modelos en `models/` y hacer commit/push.

> Si el dataset es pequeño/mediano, CPU también funciona bien para baseline de árboles.

---

## 5) Fuentes de datos sugeridas

### Precios agrícolas (núcleo)
- PIMA/CENADA boletines.
- MAG/SEPSA (si aplica para series históricas).

### Clima
- Open-Meteo Archive API (temperatura, precipitación, humedad, etc.).
- Opcional: CHIRPS/ERA5 para mayor granularidad.

### Económico
- World Bank: inflación, GDP, indicadores macro.
- BCCR: tipo de cambio, tasas, IMAE, series diarias/mensuales.

### Político / contexto (plus)
- Índices de riesgo y confianza (si consigues fuentes estables).
- Eventos/cambios regulatorios (features de calendario/eventos).

---

## 6) Diseño de features (muy importante)

- **Lags de precio**: 1, 7, 14, 28 días.
- **Rolling stats**: media/std móvil.
- **Calendario**: día de semana, quincena, mes, feriados.
- **Clima agregado**: lluvia acumulada 7/14 días por región.
- **Macro**: inflación y FX rezagados.
- **Interacciones**: lluvia × producto sensible; estacionalidad por cultivo.

---

## 7) Métricas y validación

- MAE y RMSE por producto.
- MAPE cuando los precios no estén cerca de 0.
- Backtesting temporal (TimeSeriesSplit).
- Métrica de negocio: error promedio en colones por kg/caja.

---

## 8) MLOps mínimo viable

1. **Data quality checks**
   - porcentaje de nulos,
   - duplicados,
   - outliers extremos.

2. **Reentrenamiento programado**
   - semanal (viernes) o mensual según estabilidad.

3. **Model registry simple**
   - versionar `model.pkl` + `metrics.json`.

4. **Monitoreo en producción**
   - latencia,
   - tasa de error,
   - drift de features.

---

## 9) FAQ operativo

- **¿Se puede hacer 100% gratis?** Sí, con límites razonables de uso.
- **¿Si falla PIMA?** Continuar con dataset de práctica + carga manual temporal.
- **¿Necesito GPU?** No para baseline; sí ayuda en tuning masivo.
- **¿Cada cuánto actualizar?** Semanal al inicio, luego ajustar por volatilidad.



## Nota de secretos

Para PIMA/CENADA no necesitas ningún secret (fuente pública).
Solo requerirás GitHub Secrets cuando conectemos APIs con autenticación (por ejemplo BCCR).
