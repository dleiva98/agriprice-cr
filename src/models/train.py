from pathlib import Path
import argparse
import importlib
import json

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def _safe_mape(y_true: pd.Series, y_pred) -> float:
    y_true_s = pd.Series(y_true)
    y_pred_s = pd.Series(y_pred)
    denom = y_true_s.abs().replace(0, pd.NA)
    mape = ((y_true_s - y_pred_s).abs() / denom).dropna().mean() * 100
    return float(mape) if pd.notna(mape) else float("nan")


def _build_model():
    """Use XGBoost if available; otherwise fallback to RandomForest."""
    spec = importlib.util.find_spec("xgboost")
    if spec is not None:
        xgb = importlib.import_module("xgboost")
        return (
            xgb.XGBRegressor(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=6,
                subsample=0.9,
                colsample_bytree=0.8,
                random_state=42,
            ),
            "xgboost",
        )

    print("[train] xgboost no está disponible, usando RandomForestRegressor como fallback.")
    return RandomForestRegressor(n_estimators=400, random_state=42, n_jobs=-1), "random_forest_fallback"


def train(features_path: str = "data/processed/features.csv", out_dir: str = "models") -> dict:
    path = Path(features_path)
    if not path.exists():
        raise FileNotFoundError("Ejecuta primero: python -m src.features.build_features")

    df = pd.read_csv(path, parse_dates=["date"]).sort_values("date")
    if df.empty:
        raise ValueError(f"El archivo de features está vacío: {path}")

    target = "target_t_plus_7"
    exclude = {"date", "product", target}
    feature_cols = [c for c in df.columns if c not in exclude]
    if not feature_cols:
        raise ValueError("No hay columnas de features disponibles para entrenar.")

    split_date = df["date"].max() - pd.Timedelta(days=60)
    train_df = df[df["date"] <= split_date]
    test_df = df[df["date"] > split_date]
    if train_df.empty or test_df.empty:
        raise ValueError("Split de entrenamiento/prueba vacío. Verifica que features.csv tenga suficientes fechas.")

    print(f"[train] features_path={path}")
    print(
        f"[train] rows={len(df)}, train={len(train_df)}, test={len(test_df)}, n_features={len(feature_cols)}"
    )

    model, model_name = _build_model()
    model.fit(train_df[feature_cols], train_df[target])

    preds = model.predict(test_df[feature_cols])
    mae = mean_absolute_error(test_df[target], preds)
    rmse = mean_squared_error(test_df[target], preds) ** 0.5
    r2 = r2_score(test_df[target], preds)
    mape = _safe_mape(test_df[target], preds)

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    model_file = out_path / "model_xgb.joblib"
    joblib.dump(model, model_file)

    pred_df = test_df[["date", "product", target]].copy()
    pred_df["prediction"] = preds
    pred_df.rename(columns={target: "actual"}, inplace=True)
    pred_df.to_csv(out_path / "predictions.csv", index=False)

    plt.figure(figsize=(12, 5))
    for product, gdf in pred_df.groupby("product"):
        gdf = gdf.sort_values("date")
        plt.plot(gdf["date"], gdf["actual"], label=f"{product} actual", linewidth=1.2)
        plt.plot(gdf["date"], gdf["prediction"], linestyle="--", label=f"{product} pred", linewidth=1.2)
    plt.title("Actual vs Predicción (set de prueba)")
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    plt.savefig(out_path / "predictions_plot.png", dpi=160)
    plt.close()

    metrics = {
        "model": model_name,
        "model_path": str(model_file),
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "mape_pct": float(mape),
        "n_train": len(train_df),
        "n_test": len(test_df),
    }
    (out_path / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Entrena baseline para AgriPrice CR")
    parser.add_argument("--features", default="data/processed/features.csv", help="Ruta a features.csv")
    parser.add_argument("--out-dir", default="models", help="Directorio de salida para artefactos")
    args = parser.parse_args()

    metrics = train(features_path=args.features, out_dir=args.out_dir)

    print("Training complete:")
    print(metrics)


if __name__ == "__main__":
    main()
