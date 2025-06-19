import pandas as pd
from pathlib import Path
import json

def define_objects():
    input_path = Path("data/lsci_enriched.json")
    output_dir = Path("ontology_objects")
    output_dir.mkdir(exist_ok=True)

    df = pd.read_json(input_path)

    # Economy object
    df[['economy', 'iso2', 'iso3', 'region']].drop_duplicates()\
        .to_csv(output_dir / "Economy.csv", index=False)

    # Time_Period object
    df[['period']].drop_duplicates()\
        .rename(columns={"period": "time_period"})\
        .to_csv(output_dir / "Time_Period.csv", index=False)

    # LSCI_Measurement object
    df[['economy', 'period', 'lsci_value']]\
        .to_csv(output_dir / "LSCI_Measurement.csv", index=False)

    print("✅ Ontology object files created in 'ontology_objects/'")

if __name__ == "__main__":
    define_objects()
