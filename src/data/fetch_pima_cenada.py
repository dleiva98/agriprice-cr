from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.pima.go.cr"
BOLETIN_URL = f"{BASE_URL}/boletin/"


def fetch_boletin_links() -> pd.DataFrame:
    response = requests.get(BOLETIN_URL, timeout=60)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    rows = []
    for anchor in soup.select("a[href]"):
        href = anchor.get("href", "")
        text = " ".join(anchor.get_text(" ", strip=True).split())
        if not href:
            continue

        full_url = urljoin(BOLETIN_URL, href)
        href_l = href.lower()
        full_l = full_url.lower()
        if "boletin" in href_l or "boletin" in text.lower() or full_l.endswith(".pdf"):
            rows.append({"title": text or "boletin", "url": full_url})

    df = pd.DataFrame(rows).drop_duplicates(subset=["url"])
    return df


def main() -> None:
    links = fetch_boletin_links()

    out_dir = Path("data/raw/pima")
    out_dir.mkdir(parents=True, exist_ok=True)
    links_path = out_dir / "boletin_links.csv"
    links.to_csv(links_path, index=False)

    print(f"Saved {len(links)} boletín links to {links_path}")
    print("Next step: extraer precios desde PDFs a data/raw/pima/pima_prices.csv")


if __name__ == "__main__":
    main()
