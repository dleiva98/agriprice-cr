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

## 6) Si estás en Codespaces y te sale `pathspec 'work' did not match`

Eso significa que en ese clone **no existe** la rama `work` (estás en `main` o en otra rama).

Usa este flujo exacto:

```bash
# 0) ruta correcta en Codespaces
git rev-parse --show-toplevel

# 1) remoto
git remote set-url origin https://github.com/dleiva98/agriprice-cr.git || \
  git remote add origin https://github.com/dleiva98/agriprice-cr.git

# 2) sincronizar
git fetch origin

# 3) crear work desde main actual (si no existe)
git checkout -b work || git checkout work

# 4) rebase contra main remoto (puede generar conflictos)
git rebase origin/main || true

# 5) resolver conflictos forzando versión local en archivos clave
bash scripts/resolve_conflicts_force_agent.sh

# 6) continuar rebase
git rebase --continue || true

# 7) subir work y actualizar PR
git push -u origin work --force-with-lease
```

## 7) Si GitHub no te deja aprobar tu propio PR

Mensaje típico: `Pull request authors can't approve their own pull requests`.

Esto es normal en GitHub cuando eres el autor del PR.

Opciones para continuar:

1. **Merge directo sin aprobación** (si el repo lo permite).
2. **Pedir review a otra cuenta/colaborador** con permisos de write/admin.
3. **Si hay branch protection obligatoria** y estás solo:
   - Ir a `Settings` → `Branches` → regla de `main`.
   - Quitar temporalmente `Require pull request reviews before merging`.
   - Hacer merge y luego reactivar la protección.
4. **Si no quieres PR**: push directo a `main` desde terminal (si la política del repo lo permite).
