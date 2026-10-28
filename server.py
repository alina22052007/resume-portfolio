"""
High-Performance Standard Library HTTP & REST Server
Runs with ZERO external dependencies using Python 3.10+ standard library.
Also compatible with modern web browsers, CORS enabled, and multithreaded.
"""

import sys
import os
import json
import mimetypes
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from typing import Dict, Any, Optional

import database
import gemini_service
import sheets_service
import docx_generator
from samples.sample_data import SAMPLE_JDS

PORT = 5050
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class PortfolioRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for cross-origin integration (e.g. Google Apps Script / frontend tools)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Gemini-Key")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def parse_json_body(self) -> Dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            raw = self.rfile.read(content_length).decode("utf-8")
            try:
                return json.loads(raw)
            except Exception:
                return {}
        return {}

    def send_json(self, data: Any, status: int = 200):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. API Endpoints
        if path == "/api/status":
            p = database.get_full_portfolio()
            counts = {k: len(v) for k, v in p.items() if isinstance(v, list)}
            has_key = bool(gemini_service.get_api_key())
            return self.send_json({
                "status": "online",
                "system": "AI-Powered Portfolio & Resume Generator",
                "database_connected": True,
                "counts": counts,
                "gemini_api_configured": has_key,
                "version": "2.0.0"
            })

        if path == "/api/portfolio":
            data = database.get_full_portfolio()
            return self.send_json(data)

        if path.startswith("/api/portfolio/") and len(path.split("/")) == 4:
            # /api/portfolio/<category>
            cat = path.split("/")[3]
            try:
                items = database.get_category_items(cat)
                return self.send_json(items)
            except ValueError as e:
                return self.send_json({"error": str(e)}, 400)

        if path == "/api/export/sheets-json":
            sheets_data = sheets_service.format_portfolio_for_sheets()
            return self.send_json(sheets_data)

        if path.startswith("/api/export/sheets-csv/"):
            cat = path.split("/")[4]
            try:
                csv_text = sheets_service.generate_category_csv(cat)
                csv_bytes = csv_text.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", f"attachment; filename={cat}.csv")
                self.send_header("Content-Length", str(len(csv_bytes)))
                self.end_headers()
                self.wfile.write(csv_bytes)
                return
            except Exception as e:
                return self.send_json({"error": str(e)}, 400)

        if path == "/api/sample-jds":
            return self.send_json(SAMPLE_JDS)

        if path == "/api/apps-script-code":
            script_path = os.path.join(os.path.dirname(__file__), "google_apps_script", "Code.gs")
            if os.path.exists(script_path):
                with open(script_path, "r", encoding="utf-8") as f:
                    return self.send_json({"code": f.read()})
            return self.send_json({"code": "// Code.gs not found"})

        if path == "/api/sync/logs":
            logs = database.get_sync_logs()
            return self.send_json(logs)

        if path == "/api/resume/saved":
            resumes = database.get_customized_resumes()
            return self.send_json(resumes)

        # 2. Static File Serving
        if path == "/" or path == "/index.html":
            file_path = os.path.join(STATIC_DIR, "index.html")
            return self.serve_file(file_path, "text/html; charset=utf-8")
        
        # Check static dir
        clean_rel = path.lstrip("/")
        if clean_rel.startswith("static/"):
            clean_rel = clean_rel[7:]
        
        static_file = os.path.join(STATIC_DIR, clean_rel)
        if os.path.isfile(static_file):
            ctype, _ = mimetypes.guess_type(static_file)
            return self.serve_file(static_file, ctype or "application/octet-stream")

        # Fallback to index.html for SPA
        index_file = os.path.join(STATIC_DIR, "index.html")
        if os.path.exists(index_file):
            return self.serve_file(index_file, "text/html; charset=utf-8")

        self.send_error(404, "File not found")

    def serve_file(self, file_path: str, content_type: str):
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self.parse_json_body()
        req_key = self.headers.get("X-Gemini-Key") or body.get("gemini_api_key")

        # Reset database to initial seed data
        if path == "/api/portfolio/reset-seed":
            database.init_db(force_reseed=True)
            return self.send_json({"success": True, "message": "Database reset to verified seed data."})

        # Add portfolio item: /api/portfolio/<category>
        if path.startswith("/api/portfolio/") and len(path.split("/")) == 4:
            cat = path.split("/")[3]
            try:
                new_id = database.add_category_item(cat, body)
                return self.send_json({"success": True, "id": new_id, "category": cat})
            except Exception as e:
                return self.send_json({"error": str(e)}, 400)

        # AI: Parse unstructured text
        if path == "/api/ai/parse-unstructured":
            text = body.get("text", "")
            if not text.strip():
                return self.send_json({"error": "Empty text provided"}, 400)
            structured = gemini_service.parse_unstructured_portfolio(text, req_key)
            return self.send_json({"success": True, "parsed": structured})

        # AI: Analyze Job Description
        if path == "/api/ai/analyze-jd":
            jd_text = body.get("jd_text", "")
            if not jd_text.strip():
                return self.send_json({"error": "Job description cannot be empty"}, 400)
            analysis = gemini_service.analyze_job_description(jd_text, req_key)
            return self.send_json({"success": True, "analysis": analysis})

        # AI: Match Portfolio with JD
        if path == "/api/ai/match-portfolio":
            jd_data = body.get("jd_analysis")
            if not jd_data:
                jd_text = body.get("jd_text", "")
                jd_data = gemini_service.analyze_job_description(jd_text, req_key)
            portfolio = database.get_full_portfolio()
            match_result = gemini_service.match_portfolio_with_jd(portfolio, jd_data, req_key)
            return self.send_json({"success": True, "match": match_result, "jd_analysis": jd_data})

        # AI: Generate Assembled Tailored Resume
        if path == "/api/ai/generate-resume":
            portfolio = database.get_full_portfolio()
            jd_analysis = body.get("jd_analysis", {})
            selected_skills = body.get("selected_skills", [])
            selected_projects = body.get("selected_projects", [])
            selected_exp = body.get("selected_experiences", [])
            selected_certs = body.get("selected_certifications", [])
            custom_summary = body.get("custom_summary", "")

            resume_payload = gemini_service.assemble_customized_resume(
                portfolio=portfolio,
                jd_analysis=jd_analysis,
                selected_skill_names=selected_skills,
                selected_project_ids=selected_projects,
                selected_experience_ids=selected_exp,
                selected_cert_ids=selected_certs,
                custom_summary=custom_summary
            )
            return self.send_json({"success": True, "resume": resume_payload})

        # Sync to Google Sheets via Apps Script Web App
        if path == "/api/sync/google-sheets":
            script_url = body.get("apps_script_url", "")
            result = sheets_service.sync_to_google_apps_script(script_url)
            return self.send_json(result)

        # Webhook from Google Sheets
        if path == "/api/sheets/webhook":
            res = sheets_service.handle_incoming_sheets_sync(body)
            return self.send_json(res)

        # Export to DOCX
        if path == "/api/export/docx":
            resume_data = body.get("resume")
            if not resume_data:
                return self.send_json({"error": "Missing resume payload"}, 400)
            
            docx_bytes = docx_generator.generate_docx_bytes(resume_data)
            candidate_name = resume_data.get("header", {}).get("name", "Resume").replace(" ", "_")
            role_name = resume_data.get("target_role", "Customized").replace(" ", "_")
            filename = f"{candidate_name}_{role_name}_Resume.docx"

            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            self.send_header("Content-Disposition", f"attachment; filename=\"{filename}\"")
            self.send_header("Content-Length", str(len(docx_bytes)))
            self.end_headers()
            self.wfile.write(docx_bytes)
            return

        # Save customized resume to database
        if path == "/api/resume/save":
            try:
                res_id = database.save_customized_resume(
                    target_job_title=body.get("target_job_title", "Software Engineer"),
                    target_company=body.get("target_company", "Enterprise"),
                    job_description=body.get("job_description", ""),
                    match_score=float(body.get("match_score", 0.0)),
                    selected_skills=body.get("selected_skills", []),
                    selected_projects=body.get("selected_projects", []),
                    selected_experiences=body.get("selected_experiences", []),
                    selected_certifications=body.get("selected_certifications", []),
                    tailored_summary=body.get("tailored_summary", ""),
                    resume_payload=body.get("resume_payload", {})
                )
                return self.send_json({"success": True, "id": res_id})
            except Exception as e:
                return self.send_json({"error": str(e)}, 400)

        self.send_error(404, "Endpoint not found")

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self.parse_json_body()

        # Update portfolio item: /api/portfolio/<category>/<id>
        parts = path.split("/")
        if len(parts) == 5 and parts[1] == "api" and parts[2] == "portfolio":
            cat = parts[3]
            try:
                item_id = int(parts[4])
                success = database.update_category_item(cat, item_id, body)
                return self.send_json({"success": success})
            except Exception as e:
                return self.send_json({"error": str(e)}, 400)

        self.send_error(404, "Endpoint not found")

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Delete portfolio item: /api/portfolio/<category>/<id>
        parts = path.split("/")
        if len(parts) == 5 and parts[1] == "api" and parts[2] == "portfolio":
            cat = parts[3]
            try:
                item_id = int(parts[4])
                success = database.delete_category_item(cat, item_id)
                return self.send_json({"success": success})
            except Exception as e:
                return self.send_json({"error": str(e)}, 400)

        self.send_error(404, "Endpoint not found")

def run(port: int = PORT):
    # Ensure database is initialized
    database.init_db()
    server_address = ("", port)
    httpd = ThreadedHTTPServer(server_address, PortfolioRequestHandler)
    print(f"==================================================================")
    print(f"🚀 AI-Powered Portfolio & Dynamic Resume Generator running at:")
    print(f"👉 http://localhost:{port}")
    print(f"==================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == "__main__":
    p = PORT
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        p = int(sys.argv[1])
    run(p)
