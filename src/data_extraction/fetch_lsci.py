import os
import pandas as pd
from pathlib import Path
import tomllib

def load_config():
    config_path = "config/config.toml"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"❌ Config file not found at {config_path}")
    with open(config_path, "rb") as f:
        return tomllib.load(f)

def fetch_lsci_data():
    config = load_config()

    # Get input/output paths from config
    input_dir = Path(config["data"]["input_dir"])
    output_dir = Path(config["data"]["output_dir"])
    input_csv_path = input_dir / "US_LSCI.csv"
    output_json_path = output_dir / "lsci_data.json"

    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_csv_path.exists():
        print(f"❌ Input CSV file not found: {input_csv_path}")
        return

    print(f"📥 Reading CSV from: {input_csv_path}")
    
    # ✅ Step 1: Read CSV
    df = pd.read_csv(input_csv_path)

    # ✅ Step 2: Normalize column names (critical)
    df.columns = df.columns.str.lower().str.strip()

    # ✅ Step 3: Save as JSON
    df.to_json(output_json_path, orient="records", indent=2)
    print(f"✅ CSV converted to JSON and saved at: {output_json_path}")

if __name__ == "__main__":
    fetch_lsci_data()
