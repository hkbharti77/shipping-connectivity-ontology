import json
import pandas as pd
import pycountry
import pycountry_convert as pc
from pathlib import Path
import tomllib

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

def enrich_lsci_data():
    config = load_config()
    output_dir = Path(config["data"]["output_dir"])
    json_file = output_dir / "lsci_data.json"
    enriched_file = output_dir / "lsci_enriched.json"

    if not json_file.exists():
        print(f"❌ Input JSON file not found: {json_file}")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    if not isinstance(raw_data, list):
        print("❌ Input JSON is not a list of records. Aborting.")
        return

    print(f"🔍 Loaded {len(raw_data)} raw records")

    enriched_records = []
    skipped_count = 0

    for record in raw_data:
        required_keys = ["economy label", "quarter", "index (average q1 2023 = 100)"]
        if not all(key in record for key in required_keys):
            print(f"⚠️ Skipping incomplete record: {record}")
            skipped_count += 1
            continue

        economy = record["economy label"]
        period = record["quarter"]
        value = record["index (average q1 2023 = 100)"]

        iso2, iso3 = get_country_codes(economy)
        region = get_region(iso2) if iso2 else None

        enriched_record = {
            "economy": economy,
            "period": period,
            "lsci_value": value,
            "iso2": iso2,
            "iso3": iso3,
            "region": region
        }

        enriched_records.append(enriched_record)

    if not enriched_records:
        print("❌ No enriched records created. Output file will not be saved.")
        return

    # Show first few enriched records in terminal
    print("\n🔎 Sample Enriched Records:")
    for i, rec in enumerate(enriched_records[:5]):
        print(f"{i+1}. {rec}")

    # Save to file
    pd.DataFrame(enriched_records).to_json(enriched_file, orient="records", indent=2)
    print(f"\n✅ Enriched data saved to {enriched_file}")
    print(f"📊 Total records written: {len(enriched_records)} | Skipped: {skipped_count}")

if __name__ == "__main__":
    enrich_lsci_data()
