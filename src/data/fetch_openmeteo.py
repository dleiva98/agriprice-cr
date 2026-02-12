from pathlib import Path
import pandas as pd
import requests

URL = "https://archive-api.open-meteo.com/v1/archive"


def fetch_weather(lat: float = 9.9281, lon: float = -84.0907) -> pd.DataFrame:
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2018-01-01",
        "end_date": "2024-12-31",
        "daily": "temperature_2m_mean,precipitation_sum",
        "timezone": "America/Costa_Rica",
    }
    response = requests.get(URL, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json().get("daily", {})
    return pd.DataFrame(payload).rename(columns={"time": "date"})


def main() -> None:
    df = fetch_weather()
    out = Path("data/raw/weather_openmeteo.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} rows to {out}")


if __name__ == "__main__":
    main()
