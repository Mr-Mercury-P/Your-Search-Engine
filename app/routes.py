from flask import Blueprint, request, jsonify, render_template
import pandas as pd
import os
from .serpapi_client import fetch_search_results
from .groq_client import get_llm_results

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    upload_folder = "uploads"
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    try:
        df = pd.read_csv(file_path)
        return jsonify({"columns": df.columns.tolist(), "file_path": file_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@main.route("/search", methods=["POST"])
def search():
    data = request.json
    file_path = data.get("file_path")
    column = data.get("column")
    prompt_template = data.get("prompt")

    if not file_path or not column or not prompt_template:
        return jsonify({"error": "Missing required data"}), 400

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        df = pd.read_csv(file_path)
        if column not in df.columns:
            return jsonify({"error": f"Column '{column}' not found in CSV"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to read the CSV: {str(e)}"}), 400

    results = {}
    for entity in df[column]:
        if pd.isna(entity) or not isinstance(entity, str) or not entity.strip():
            continue

        query = prompt_template.format(entity=entity)
        search_results = fetch_search_results(query)

        if search_results:
            cleaned_text = search_results[0].get("cleaned_snippet", "")
            groq_response = get_llm_results(query, cleaned_text)
            results[entity] = groq_response
        else:
            results[entity] = "No search results found"

    return jsonify(results)
