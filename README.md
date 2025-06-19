# 📦 Shipping Connectivity Ontology (LSCI) Project

## 📘 Project Overview

This project models global shipping connectivity using the Liner Shipping Connectivity Index (LSCI) as provided by UNCTAD. The goal is to:

* Extract and enrich LSCI data over multiple years
* Build an ontology to represent economies, measurements, and time periods
* Expose the data via a RESTful API with Swagger documentation

---

## 💂️ Directory Structure

```
shipping-connectivity-ontology/
├── config/                      # Configuration folder
│   └── config.toml
├── data/                        # Output enriched and growth data
│   ├── lsci_enriched_with_growth.json
│   └── lsci_growth_trends.csv
├── doc/                         # Source CSV input (e.g., US_LSCI.csv)
│   └── US_LSCI.csv
├── ontology_objects/           # Object tables like Economy, Period
├── ontology_links/             # Linkage tables (e.g. Economy->LSCI)
├── ontology_output/            # Final assembled ontology (optional)
├── src/                        # Pipeline & analysis scripts
│   ├── analytics/              # Trend analysis & scoring
│   ├── data_extraction/        # Load & enrich LSCI data
│   ├── data_pipeline/          # ETL coordination (if used)
│   ├── ontology_definition/    # Define objects and links
│   ├── ontology_sim/           # Optional simulation/test ontology logic
│   └── validation/             # Schema + completeness checks
├── run_local_ontology.py       # Optional runner script
├── LsciApiServer.py            # Flask API (entry point)
├── README.md                   # Project overview
└── requirements.txt            # Python dependencies

```

---

## 🔄 Workflow Summary

### 1. ✅ Data Extraction & Enrichment

* Fetched LSCI data (fallback to `lsci_data.csv` if API fails)
* Extracted fields: `economy`, `period`, `lsci_value`
* Enriched with:

  * ISO2 / ISO3 country codes
  * UN region (Asia, Europe, etc.)
  * Calculated `growth_rate` using `pct_change()`

### 2. ✅ Ontology Modeling

* **Objects**:

  * `Economy` with ISO codes and region
  * `LSCI_Measurement` with values and growth
  * `Time_Period` (e.g. "2023Q1")
* **Links**:

  * `Economy → MEASURED_BY → LSCI_Measurement`
  * `LSCI_Measurement → RECORDED_IN → Time_Period`

### 3. ✅ API Layer (Flask + Swagger)

* `/` — Health check
* `/api/growth` — LSCI trends (with optional `economy` filter)
* `/api/enriched` — Full enriched dataset (with optional filter)
* `/apidocs` — Swagger UI via Flasgger

---

## 🚀 How to Run the API

### Prerequisites

* Python 3.11+

### ⚙️ Create and Activate a Virtual Environment (Recommended)

Using a virtual environment ensures that dependencies are isolated:

<details>
<summary><strong>🔹 For Windows</strong></summary>

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

</details>

<details>
<summary><strong>🔹 For macOS/Linux</strong></summary>

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

</details>

Then install dependencies inside the environment:

```bash
pip install -r requirements.txt
```

### Run the API

```bash
python api/lsci_api_server.py
```

Visit:

* `http://localhost:5000/` (health check)
* `http://localhost:5000/apidocs` (Swagger UI)

---

## 📊 Evaluation Criteria Coverage

| Criterion                       | Coverage                                         |
| ------------------------------- | ------------------------------------------------ |
| Relevance of Objects & Linkages | ✅ Defined + linked                               |
| Data Modeling Quality           | ✅ Normalized & enriched                          |
| Completeness                    | ✅ All required fields included                   |
| Flexibility/Extensibility       | ✅ Region & growth support + extendable structure |
| Reasoning Capabilities          | ✅ Trend queries + filters via API                |

---

## ✨ Optional Extensions (Future Work)

* Add `CONNECTED_TO` relationships based on LSCI similarity
* Add a frontend dashboard (React + Chart.js)
* Export ontology as YAML or OWL for semantic reasoning
* Deploy with Docker + NGINX for production

---

## 🙌 Author & Acknowledgements

This project was implemented as part of Stage 1: Ontology & Data Modeling for LSCI. Data provided by [UNCTADstat](https://unctadstat.unctad.org/datacentre/dataviewer/US.LSCI).

---

Feel free to clone, adapt, and extend! 💡
