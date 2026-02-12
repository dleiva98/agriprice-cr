from pathlib import Path
import numpy as np
import pandas as pd


def _load_pima_prices() -> pd.DataFrame | None:
    candidates = [
        Path("data/raw/pima/pima_prices.csv"),
        Path("data/raw/prices.csv"),
    ]
    for path in candidates:
        if path.exists():
            df = pd.read_csv(path, parse_dates=["date"])
            expected = {"date", "product", "price"}
            if not expected.issubset(df.columns):
                raise ValueError(f"{path} debe contener columnas: {sorted(expected)}")
            return df[list(expected)].copy()
    return None


def load_or_create_prices() -> pd.DataFrame:
    pima_df = _load_pima_prices()
    if pima_df is not None:
        return pima_df

    dates = pd.date_range("2022-01-01", "2024-12-31", freq="D")
    df = pd.DataFrame(
        {
            "date": dates,
            "product": "tomate",
            "price": 800 + 50 * np.sin(np.arange(len(dates)) / 14),
        }
    )
    out = Path("data/raw/pima/pima_prices.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return df


def main() -> None:
    prices = load_or_create_prices().sort_values(["product", "date"])

    prices["dow"] = prices["date"].dt.dayofweek
    prices["month"] = prices["date"].dt.month

    for lag in [1, 7, 14, 28]:
        prices[f"price_lag_{lag}"] = prices.groupby("product")["price"].shift(lag)

    prices["price_roll7_mean"] = prices.groupby("product")["price"].transform(lambda s: s.shift(1).rolling(7).mean())
    prices["target_t_plus_7"] = prices.groupby("product")["price"].shift(-7)

    out = Path("data/processed/features.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    prices.dropna().to_csv(out, index=False)
    print(f"Saved features to {out}")


if __name__ == "__main__":
    main()
