import os
import json
import pandas as pd
from pathlib import Path
import tomllib
import pycountry
import pycountry_convert as pc

def load_config():
    with open("config/config.toml", "rb") as f:
        return tomllib.load(f)

def get_country_codes(name):
    try:
        country = pycountry.countries.lookup(name)
        return country.alpha_2, country.alpha_3
    except LookupError:
        return None, None

def get_region(alpha_2_code):
    try:
        continent_code = pc.country_alpha2_to_continent_code(alpha_2_code)
        return pc.convert_continent_code_to_continent_name(continent_code)
    except:
        return None

def fetch_lsci_data(config):
    input_dir = Path(config["data"]["input_dir"])
    output_dir = Path(config["data"]["output_dir"])
    input_csv = input_dir / "US_LSCI.csv"
    output_json = output_dir / "lsci_data.json"

    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_csv.exists():
        print(f"❌ Input CSV not found at: {input_csv}")
        return False

    df = pd.read_csv(input_csv)
    df.columns = df.columns.str.lower().str.strip()  # normalize column names
    df.to_json(output_json, orient="records", indent=2)
    print(f"✅ CSV → JSON saved to: {output_json}")
    return True

def enrich_lsci_data(config):
    output_dir = Path(config["data"]["output_dir"])
    input_json = output_dir / "lsci_data.json"
    enriched_json = output_dir / "lsci_enriched.json"

    if not input_json.exists():
        print(f"❌ Input JSON not found at: {input_json}")
        return False

    with open(input_json, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    enriched = []
    for record in raw_data:
        if not all(k in record for k in ("economy", "year", "lsci_value")):
            print(f"⚠️ Skipping incomplete record: {record}")
            continue

        economy = record["economy"]
        year = record["year"]
        value = record["lsci_value"]

        iso2, iso3 = get_country_codes(economy)
        region = get_region(iso2) if iso2 else None

        enriched.append({
            "economy": economy,
            "year": year,
            "lsci_value": value,
            "iso2": iso2,
            "iso3": iso3,
            "region": region
        })

    pd.DataFrame(enriched).to_json(enriched_json, orient="records", indent=2)
    print(f"✅ Enriched JSON saved to: {enriched_json}")
    return True

def check_completeness(config):
    output_dir = Path(config["data"]["output_dir"])
    enriched_json = output_dir / "lsci_enriched.json"

    if not enriched_json.exists():
        print(f"❌ Enriched JSON not found at: {enriched_json}")
        return

    with open(enriched_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    print("🧪 Completeness Check:")
    for col in ["iso3", "region", "lsci_value"]:
        if col not in df.columns:
            print(f" - {col}: ❌ column missing")
        else:
            missing = df[col].isnull().sum()
            print(f" - {col}: {missing}")

    if all(col in df.columns and df[col].isnull().sum() == 0 for col in ["iso3", "region", "lsci_value"]):
        print("✅ All essential fields are complete.")
    else:
        print("⚠️ Incomplete fields found. Please review enrichment.")

def run_pipeline():
    config = load_config()
    print("🚀 Starting LSCI Data Pipeline...\n")

    if not fetch_lsci_data(config):
        return
    if not enrich_lsci_data(config):
        return

    check_completeness(config)

if __name__ == "__main__":
    run_pipeline()
