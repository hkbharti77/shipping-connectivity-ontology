import json
import pandas as pd
from pathlib import Path
import tomllib

def load_config():
    with open("config/config.toml", "rb") as f:
        return tomllib.load(f)

def check_completeness():
    config = load_config()
    data_path = Path(config["data"]["output_dir"]) / "lsci_enriched.json"
    report_path = Path(config["data"]["output_dir"]) / "lsci_incomplete_records.csv"

    if not data_path.exists():
        print(f"❌ Enriched JSON file not found at {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    print("🧪 Completeness Check:")

    expected_columns = ["iso3", "region", "lsci_value"]
    missing_counts = {}

    # Check column existence and missing values
    for col in expected_columns:
        if col in df.columns:
            missing_counts[col] = df[col].isnull().sum()
        else:
            missing_counts[col] = "❌ column missing"

    # Print summary
    for col, count in missing_counts.items():
        print(f" - {col}: {count}")

    # Save incomplete records (optional)
    incomplete_df = df[df[expected_columns].isnull().any(axis=1)] if all(col in df.columns for col in expected_columns) else pd.DataFrame()

    if not incomplete_df.empty:
        incomplete_df.to_csv(report_path, index=False)
        print(f"📁 Incomplete records saved to: {report_path}")

    # Final completeness status
    if all(isinstance(count, int) and count == 0 for count in missing_counts.values()):
        print("✅ All essential fields are complete.")
    else:
        print("⚠️ Incomplete fields found. Please review enrichment.")

if __name__ == "__main__":
    check_completeness()
