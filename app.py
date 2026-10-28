"""
Flask Application for AI-Powered Portfolio Database & Dynamic Resume Generator
Alternative framework option supporting Flask if installed in the environment.
To run with Flask:
    pip install -r requirements.txt
    python3 app.py
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory, send_file, Response
import io

import database
import gemini_service
import sheets_service
import docx_generator
from samples.sample_data import SAMPLE_JDS

app = Flask(__name__, static_folder="static")

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Gemini-Key"
    return response

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

@app.route("/api/status", methods=["GET"])
def get_status():
    p = database.get_full_portfolio()
    counts = {k: len(v) for k, v in p.items() if isinstance(v, list)}
    has_key = bool(gemini_service.get_api_key())
    return jsonify({
        "status": "online",
        "system": "AI-Powered Portfolio & Resume Generator (Flask)",
        "database_connected": True,
        "counts": counts,
        "gemini_api_configured": has_key,
        "version": "2.0.0"
    })

@app.route("/api/portfolio", methods=["GET"])
def get_portfolio():
    return jsonify(database.get_full_portfolio())

@app.route("/api/portfolio/<category>", methods=["GET"])
def get_category(category):
    try:
        return jsonify(database.get_category_items(category))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/portfolio/<category>", methods=["POST"])
def add_category(category):
    try:
        new_id = database.add_category_item(category, request.get_json(force=True) or {})
        return jsonify({"success": True, "id": new_id, "category": category})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/portfolio/<category>/<int:item_id>", methods=["PUT"])
def update_category(category, item_id):
    try:
        success = database.update_category_item(category, item_id, request.get_json(force=True) or {})
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/portfolio/<category>/<int:item_id>", methods=["DELETE"])
def delete_category(category, item_id):
    try:
        success = database.delete_category_item(category, item_id)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/portfolio/reset-seed", methods=["POST"])
def reset_seed():
    database.init_db(force_reseed=True)
    return jsonify({"success": True, "message": "Database reset to verified seed data."})

@app.route("/api/ai/parse-unstructured", methods=["POST"])
def parse_unstructured():
    data = request.get_json(force=True) or {}
    text = data.get("text", "")
    key = request.headers.get("X-Gemini-Key") or data.get("gemini_api_key")
    if not text.strip():
        return jsonify({"error": "Empty text provided"}), 400
    structured = gemini_service.parse_unstructured_portfolio(text, key)
    return jsonify({"success": True, "parsed": structured})

@app.route("/api/ai/analyze-jd", methods=["POST"])
def analyze_jd():
    data = request.get_json(force=True) or {}
    jd_text = data.get("jd_text", "")
    key = request.headers.get("X-Gemini-Key") or data.get("gemini_api_key")
    if not jd_text.strip():
        return jsonify({"error": "Job description cannot be empty"}), 400
    analysis = gemini_service.analyze_job_description(jd_text, key)
    return jsonify({"success": True, "analysis": analysis})

@app.route("/api/ai/match-portfolio", methods=["POST"])
def match_portfolio():
    data = request.get_json(force=True) or {}
    key = request.headers.get("X-Gemini-Key") or data.get("gemini_api_key")
    jd_data = data.get("jd_analysis")
    if not jd_data:
        jd_text = data.get("jd_text", "")
        jd_data = gemini_service.analyze_job_description(jd_text, key)
    portfolio = database.get_full_portfolio()
    match_result = gemini_service.match_portfolio_with_jd(portfolio, jd_data, key)
    return jsonify({"success": True, "match": match_result, "jd_analysis": jd_data})

@app.route("/api/ai/generate-resume", methods=["POST"])
def generate_resume():
    data = request.get_json(force=True) or {}
    portfolio = database.get_full_portfolio()
    resume_payload = gemini_service.assemble_customized_resume(
        portfolio=portfolio,
        jd_analysis=data.get("jd_analysis", {}),
        selected_skill_names=data.get("selected_skills", []),
        selected_project_ids=data.get("selected_projects", []),
        selected_experience_ids=data.get("selected_experiences", []),
        selected_cert_ids=data.get("selected_certifications", []),
        custom_summary=data.get("custom_summary", "")
    )
    return jsonify({"success": True, "resume": resume_payload})

@app.route("/api/export/sheets-json", methods=["GET"])
def export_sheets_json():
    return jsonify(sheets_service.format_portfolio_for_sheets())

@app.route("/api/export/sheets-csv/<category>", methods=["GET"])
def export_sheets_csv(category):
    try:
        csv_text = sheets_service.generate_category_csv(category)
        return Response(
            csv_text,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename={category}.csv"}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/sync/google-sheets", methods=["POST"])
def sync_google_sheets():
    data = request.get_json(force=True) or {}
    script_url = data.get("apps_script_url", "")
    return jsonify(sheets_service.sync_to_google_apps_script(script_url))

@app.route("/api/export/docx", methods=["POST"])
def export_docx():
    data = request.get_json(force=True) or {}
    resume_data = data.get("resume")
    if not resume_data:
        return jsonify({"error": "Missing resume payload"}), 400
    
    docx_bytes = docx_generator.generate_docx_bytes(resume_data)
    candidate_name = resume_data.get("header", {}).get("name", "Resume").replace(" ", "_")
    role_name = resume_data.get("target_role", "Customized").replace(" ", "_")
    filename = f"{candidate_name}_{role_name}_Resume.docx"

    return send_file(
        io.BytesIO(docx_bytes),
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        as_attachment=True,
        download_name=filename
    )

@app.route("/api/sample-jds", methods=["GET"])
def get_sample_jds():
    return jsonify(SAMPLE_JDS)

@app.route("/api/apps-script-code", methods=["GET"])
def get_apps_script_code():
    script_path = os.path.join(os.path.dirname(__file__), "google_apps_script", "Code.gs")
    if os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            return jsonify({"code": f.read()})
    return jsonify({"code": "// Code.gs not found"})

if __name__ == "__main__":
    database.init_db()
    app.run(host="0.0.0.0", port=5050, debug=True)
