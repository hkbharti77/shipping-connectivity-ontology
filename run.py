# from src.data_extraction.fetch_lsci import fetch_lsci_data
# from src.data_extraction.enrich_data import enrich_lsci_data
# from src.data_pipeline.pipeline import generate_instances
# from src.validation.schema_check import check_schema
# from src.validation.completeness_check import check_completeness
# from src.validation.sample_queries import run_sample_queries

# def main():
#     print("\n🚢 Starting Shipping Connectivity Ontology Pipeline\n")

#     # Step 1: Fetch raw LSCI data from SDMX API
#     print("📥 Step 1: Fetching LSCI data from UNCTADstat...")
#     fetch_lsci_data()

#     # Step 2: Enrich data with ISO codes and regions
#     print("\n🧪 Step 2: Enriching data with ISO codes and regions...")
#     enrich_lsci_data()

#     # Step 3: Generate ontology object instances and links
#     print("\n📦 Step 3: Generating ontology instances and relationships...")
#     generate_instances()

#     # Step 4: Run validation scripts
#     print("\n🔍 Step 4a: Validating schema...")
#     check_schema()

#     print("\n🔍 Step 4b: Validating completeness...")
#     check_completeness()

#     # Step 5: Sample query insights
#     print("\n📊 Step 5: Running sample analytics queries...")
#     run_sample_queries()

#     print("\n✅ Pipeline completed successfully!\n")

# if __name__ == "__main__":
#     main()





# lsci_api_server.py
# ✅ A complete FastAPI server to serve enriched LSCI data + growth trends

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import pandas as pd
import tomllib

# ------------------- CONFIG -------------------
def load_config():
    with open("config/config.toml", "rb") as f:
        return tomllib.load(f)

config = load_config()
data_dir = Path(config["data"]["output_dir"])
growth_file = data_dir / "lsci_growth_trends.csv"
enriched_file = data_dir / "lsci_enriched_with_growth.json"

# ------------------- FASTAPI APP -------------------
app = FastAPI(
    title="📊 LSCI Growth API",
    description="""
API for exploring Liner Shipping Connectivity Index (LSCI) data,
including country-level trends and enriched metadata.

**Query Examples**:
- `/api/growth?economy=India`
- `/api/enriched?economy=Vietnam`
""",
    version="1.0.0",
    contact={
        "name": "Himanshu Bharti",
        "email": "you@example.com"
    }
)

@app.get("/")
def index():
    return {"message": "📡 LSCI Growth API is running."}

# ------------------- GET ALL GROWTH -------------------
@app.get("/api/growth", tags=["Growth Data"], summary="Get LSCI growth data")
def get_growth_data(economy: str = Query(None, description="Filter by economy name")):
    if not growth_file.exists():
        raise HTTPException(status_code=404, detail="Growth file not found.")

    df = pd.read_csv(growth_file)
    if economy:
        df = df[df["economy"].str.lower() == economy.lower()]

    return JSONResponse(content=df.to_dict(orient="records"))

# ------------------- GET ENRICHED DATA -------------------
@app.get("/api/enriched", tags=["Enriched Data"], summary="Get enriched LSCI data")
def get_enriched_data(economy: str = Query(None, description="Filter by economy name")):
    if not enriched_file.exists():
        raise HTTPException(status_code=404, detail="Enriched data file not found.")

    df = pd.read_json(enriched_file)
    if economy:
        df = df[df["economy"].str.lower() == economy.lower()]

    return JSONResponse(content=df.to_dict(orient="records"))
