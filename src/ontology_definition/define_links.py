import pandas as pd
from pathlib import Path

def define_links():
    input_path = Path("data/lsci_enriched.json")
    output_dir = Path("ontology_links")
    output_dir.mkdir(exist_ok=True)

    df = pd.read_json(input_path)

    # Economy → LSCI_Measurement
    df[['economy', 'period']]\
        .drop_duplicates()\
        .to_csv(output_dir / "Economy_MeasuredBy_LSCI.csv", index=False)

    # LSCI_Measurement → Time_Period
    df[['period']].drop_duplicates()\
        .rename(columns={"period": "time_period"})\
        .to_csv(output_dir / "LSCI_RecordedIn_TimePeriod.csv", index=False)

    print("✅ Ontology link files created in 'ontology_links/'")

if __name__ == "__main__":
    define_links()
