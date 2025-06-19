import json
import pandas as pd
from pathlib import Path
import tomllib

def load_config():
    with open("config/config.toml", "rb") as f:
        return tomllib.load(f)

def check_schema():
    config = load_config()
    file_path = Path(config["data"]["output_dir"]) / "lsci_enriched.json"

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    print("🧪 Schema Check:")
    expected_schema = {
        "economy": str,
        "period": str,
        "lsci_value": (int, float),
        "iso2": str,
        "iso3": str,
        "region": str
    }

    for col, expected_type in expected_schema.items():
        if col not in df.columns:
            print(f"❌ Column missing: {col}")
            continue

        mismatches = df[~df[col].apply(lambda x: isinstance(x, expected_type) or pd.isnull(x))]

        if not mismatches.empty:
            print(f"⚠️ Type mismatch in column '{col}': Found {len(mismatches)} mismatches.")
            print(f"   🔍 Example: {mismatches.iloc[0].to_dict()}")
        else:
            print(f"✅ Column '{col}' type check passed.")

if __name__ == "__main__":
    check_schema()
