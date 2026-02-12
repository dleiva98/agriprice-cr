from pathlib import Path
import pandas as pd
import requests

COUNTRY = "CRI"
INDICATORS = {
    # Precios generales y de alimentos
    "FP.CPI.TOTL.ZG": "inflation_pct",
    "FP.CPI.TOTL": "cpi_index",
    "FP.CPI.FOOD": "food_cpi_index",
    # Tipo de cambio
    "PA.NUS.FCRF": "fx_official_lcu_per_usd",
    # Apertura comercial (proxy de presión externa en precios)
    "NE.IMP.GNFS.ZS": "imports_goods_services_pct_gdp",
    "NE.EXP.GNFS.ZS": "exports_goods_services_pct_gdp",
    # Actividad macro
    "NY.GDP.MKTP.KD.ZG": "gdp_growth_pct",
}

MIN_EXPECTED_YEAR_SPAN = 20


def fetch_indicator(code: str, name: str) -> pd.DataFrame:
    url = f"https://api.worldbank.org/v2/country/{COUNTRY}/indicator/{code}?format=json&per_page=200"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    payload = response.json()
    data = payload[1] if len(payload) > 1 and payload[1] else []
    rows = [{"year": int(r["date"]), name: r["value"]} for r in data if r.get("value") is not None]
    return pd.DataFrame(rows)


def validate_output(df: pd.DataFrame) -> None:
    if df["year"].duplicated().any():
        duplicate_years = df.loc[df["year"].duplicated(), "year"].tolist()
        raise ValueError(f"Duplicados detectados en year: {duplicate_years}")

    null_pct = (df.isna().mean() * 100).round(2)
    print("Porcentaje de nulos por columna (%):")
    print(null_pct.to_string())

    year_span = int(df["year"].max() - df["year"].min() + 1)
    if year_span < MIN_EXPECTED_YEAR_SPAN:
        raise ValueError(
            f"Rango de años insuficiente: {df['year'].min()}-{df['year'].max()} "
            f"({year_span} años), mínimo esperado {MIN_EXPECTED_YEAR_SPAN}."
        )


def main() -> None:
    frames = [fetch_indicator(code, name) for code, name in INDICATORS.items()]
    out_df = (
        pd.concat(frames, axis=0, ignore_index=True)
        .groupby("year", as_index=False)
        .first()
        .sort_values("year")
        .reset_index(drop=True)
    )

    validate_output(out_df)

    out = Path("data/raw/worldbank_macro.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(out, index=False)
    print(f"Saved {len(out_df)} rows to {out}")


if __name__ == "__main__":
    main()
