from flask import Flask, jsonify, request
from flasgger import Swagger
import pandas as pd
from pathlib import Path
import tomllib

# Load config
def load_config():
    with open("config/config.toml", "rb") as f:
        return tomllib.load(f)

config = load_config()
data_dir = Path(config["data"]["output_dir"])
growth_file = data_dir / "lsci_growth_trends.csv"
enriched_file = data_dir / "lsci_enriched_with_growth.json"

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def index():
    return jsonify({"message": "📡 LSCI Growth API is running."})

@app.route('/api/growth', methods=['GET'])
def get_growth_data():
    """
    Get LSCI Growth Data
    ---
    parameters:
      - name: economy
        in: query
        type: string
        required: false
        description: Filter by economy
    responses:
      200:
        description: List of LSCI growth records
    """
    if not growth_file.exists():
        return jsonify({"error": "File not found"}), 404

    df = pd.read_csv(growth_file)
    economy = request.args.get("economy")

    if economy:
        df = df[df["economy"].str.lower() == economy.lower()]

    return jsonify(df.to_dict(orient="records"))

@app.route('/api/enriched', methods=['GET'])
def get_enriched_data():
    """
    Get Enriched LSCI Data
    ---
    parameters:
      - name: economy
        in: query
        type: string
        required: false
        description: Filter by economy
    responses:
      200:
        description: Enriched LSCI data with ISO and region info
    """
    if not enriched_file.exists():
        return jsonify({"error": "File not found"}), 404

    df = pd.read_json(enriched_file)
    economy = request.args.get("economy")

    if economy:
        df = df[df["economy"].str.lower() == economy.lower()]

    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
