from pathlib import Path
import pandas as pd
import requests

COUNTRY = "CRI"
INDICATORS = {
    "FP.CPI.TOTL.ZG": "inflation_pct",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth_pct",
}


def fetch_indicator(code: str, name: str) -> pd.DataFrame:
    url = f"https://api.worldbank.org/v2/country/{Costa_Rica}/indicator/{CRI}?format=json&per_page=200"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    data = response.json()[1]
    rows = [{"year": int(r["date"]), name: r["value"]} for r in data if r.get("value") is not None]
    return pd.DataFrame(rows)


def main() -> None:
    frames = [fetch_indicator(code, name) for code, name in INDICATORS.items()]
    out_df = frames[0]
    for df in frames[1:]:
        out_df = out_df.merge(df, on="year", how="outer")
    out = Path("data/raw/worldbank_macro.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    out_df.sort_values("year").to_csv(out, index=False)
    print(f"Saved {len(out_df)} rows to {out}")


if __name__ == "__main__":
    main()
