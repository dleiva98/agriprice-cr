# Publicar el repositorio en GitHub (si solo ves `.gitkeep`)

Si en GitHub solo aparece `.gitkeep`, normalmente la rama local con los cambios **no está publicada**.

## 1) Verifica que los archivos existen localmente

```bash
git ls-tree --name-only -r HEAD
```

## 2) Conecta el remoto (una sola vez)

```bash
git remote add origin https://github.com/<TU_USUARIO>/<TU_REPO>.git
```

Si ya existe remoto:

```bash
git remote set-url origin https://github.com/<TU_USUARIO>/<TU_REPO>.git
```

## 3) Publica la rama actual

```bash
git push -u origin work
```

## 4) (Opcional pero recomendado) Publicar en `main`

```bash
git checkout -B main
git merge --ff-only work
git push -u origin main
```

## 5) Confirmación final en GitHub

Debes ver al menos:

- `.github/workflows/scrape_weekly.yml`
- `.github/workflows/train_weekly.yml`
- `README.md`
- `docs/roadmap_mlops_cr.md`
- `src/data/fetch_openmeteo.py`
- `src/data/fetch_worldbank.py`
- `src/features/build_features.py`
- `src/models/train.py`

