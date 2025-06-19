import sys
import os
from pathlib import Path

# Ensure src is in path
CURRENT_DIR = Path(__file__).resolve().parent
sys.path.append(str(CURRENT_DIR))

import pandas as pd
import tomllib

from ontology_sim.objects_generator import generate_objects
from ontology_sim.links_generator import generate_links

def load_config():
    config_path = Path("config/config.toml")
    if not config_path.exists():
        raise FileNotFoundError(f"❌ Config file not found: {config_path}")
    with open(config_path, "rb") as f:
        return tomllib.load(f)

def main():
    print("🚀 Running Local Ontology Simulator")

    config = load_config()
    output_dir = config["data"]["output_dir"]
    enriched_file = Path(output_dir) / "lsci_enriched.json"

    if not enriched_file.exists():
        print(f"❌ Enriched file not found: {enriched_file}")
        return

    try:
        df = pd.read_json(enriched_file)
    except Exception as e:
        print(f"❌ Failed to load JSON file: {e}")
        return

    print(f"📂 Loaded {len(df)} records from: {enriched_file}")

    generate_objects(df, output_dir="ontology_output/objects")
    generate_links(df, output_dir="ontology_output/links")

    print("✅ Ontology objects and links created successfully.")

if __name__ == "__main__":
    main()
