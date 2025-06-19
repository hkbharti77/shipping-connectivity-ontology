import pandas as pd
from pathlib import Path

def generate_links(df, output_dir="ontology_output/links"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    df[['economy', 'period']].drop_duplicates() \
        .to_csv(output_path / "economy_measured_by_lsci.csv", index=False)

    df[['period']].drop_duplicates() \
        .assign(lsci_id=lambda x: "lsci_" + x['period']) \
        .to_csv(output_path / "lsci_recorded_in_time.csv", index=False)

    df[['economy', 'region']].drop_duplicates() \
        .to_csv(output_path / "economy_belongs_to_region.csv", index=False)

    print("✅ Link CSVs created in:", output_path)
