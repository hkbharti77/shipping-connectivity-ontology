import json
import pandas as pd
from pathlib import Path
import tomllib

def load_config():
    with open("config/config.toml", "rb") as f:
        return tomllib.load(f)

def analyze_growth():
    config = load_config()
    data_path = Path(config["data"]["output_dir"]) / "lsci_enriched.json"

    if not data_path.exists():
        print(f"❌ Enriched file not found: {data_path}")
        return

    df = pd.read_json(data_path, orient="records")
    df.columns = [str(col).lower().strip() for col in df.columns]  # ✅ normalize safely

    print("📊 Available Columns:", df.columns.tolist())  # ✅ debug line

    if "period" not in df.columns or "lsci_value" not in df.columns:
        print("❌ Required fields ('period', 'lsci_value') not found in JSON. Aborting.")
        return

    # Extract year/quarter from period
    df["year"] = df["period"].str[:4]
    df["quarter"] = df["period"].str[-2:]

    df["lsci_value"] = pd.to_numeric(df["lsci_value"], errors="coerce")
    df = df.sort_values(by=["economy", "period"])

    df["lsci_growth_pct"] = df.groupby("economy")["lsci_value"].pct_change() * 100
    df["lsci_growth_pct"] = df["lsci_growth_pct"].round(2)

    print("\n📈 LSCI Growth Sample:")
    print(df[["economy", "period", "lsci_value", "lsci_growth_pct"]].head(10))

    output_path = Path(config["data"]["output_dir"]) / "lsci_growth_trends.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✅ Growth trends saved to: {output_path}")

if __name__ == "__main__":
    analyze_growth()
