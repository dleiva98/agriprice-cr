from pathlib import Path
import numpy as np
import pandas as pd


def load_or_create_prices() -> pd.DataFrame:
    path = Path("data/raw/prices.csv")
    if path.exists():
        return pd.read_csv(path, parse_dates=["date"])

    dates = pd.date_range("2022-01-01", "2024-12-31", freq="D")
    df = pd.DataFrame(
        {
            "date": dates,
            "product": "tomate",
            "price": 800 + 50 * np.sin(np.arange(len(dates)) / 14),
        }
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def main() -> None:
    prices = load_or_create_prices().sort_values(["product", "date"])

    weather_path = Path("data/raw/weather_openmeteo.csv")
    if weather_path.exists():
        weather = pd.read_csv(weather_path, parse_dates=["date"])
        prices = prices.merge(weather, on="date", how="left")

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
