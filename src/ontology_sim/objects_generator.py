import pandas as pd
from pathlib import Path

def generate_objects(df, output_dir="ontology_output/objects"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    df[['economy', 'iso2', 'iso3', 'region']].drop_duplicates() \
        .to_csv(output_path / "economy.csv", index=False)

    df[['economy', 'period', 'lsci_value']].drop_duplicates() \
        .to_csv(output_path / "lsci_measurement.csv", index=False)

    df[['period']].drop_duplicates() \
        .to_csv(output_path / "time_period.csv", index=False)

    print("✅ Object CSVs created in:", output_path)
