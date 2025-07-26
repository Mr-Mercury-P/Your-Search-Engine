from flask import Blueprint, request, jsonify, render_template, send_file, Response
import pandas as pd
import os
import io
from .serpapi_client import fetch_search_results
from .groq_client import get_llm_results

main = Blueprint("main", __name__)

# Global variable to store results
search_results_data = None

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    try:
        # Detect file type and use appropriate reader
        if file.filename.lower().endswith(".csv"):
            df = pd.read_csv(file_path, encoding='latin1')
        elif file.filename.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)
        else:
            return jsonify({"error": "Unsupported file type. Please upload a CSV or Excel file."}), 400

        return jsonify({"columns": df.columns.tolist(), "file_path": file_path})
    except Exception as e:
        print("Upload Error:", str(e))
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
        # Read based on file type
        if file_path.lower().endswith(".csv"):
            df = pd.read_csv(file_path, encoding='latin1')
        elif file_path.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)
        else:
            return jsonify({"error": "Unsupported file type in search"}), 400

        if column not in df.columns:
            return jsonify({"error": f"Column '{column}' not found in file"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to read the file: {str(e)}"}), 400

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

    global search_results_data
    search_results_data = pd.DataFrame(list(results.items()), columns=["Entity", "Response"])
    return jsonify(results)

@main.route("/download_results", methods=["GET"])
def download_results():
    global search_results_data
    if search_results_data is None or search_results_data.empty:
        return jsonify({"error": "No results available for download"}), 400

    # Convert DataFrame to CSV in memory
    output = io.StringIO()
    search_results_data.to_csv(output, index=False)
    output.seek(0)

    return Response(
        output,
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=search_results.csv"}
    )
