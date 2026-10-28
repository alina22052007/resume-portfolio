"""
Google Sheets Integration Service for Portfolio Management
Supports:
1. Multi-category formatted export (JSON & CSV)
2. Google Apps Script Web App two-way synchronization
3. Webhook listener for incoming updates from Google Sheets
4. Comprehensive logging in SQLite sync_logs
"""

import json
import io
import csv
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional
import database

SHEET_TAB_ORDER = [
    "Personal_Info",
    "Education",
    "Skills",
    "Certifications",
    "Projects",
    "Experience",
    "Achievements",
    "Publications",
    "Languages"
]

def format_portfolio_for_sheets() -> Dict[str, Any]:
    """Formats all portfolio tables into sheet headers and rows for Google Sheets API or Apps Script."""
    portfolio = database.get_full_portfolio()
    sheets_payload = {}

    # 1. Personal Info
    p = portfolio.get("profile") or {}
    sheets_payload["Personal_Info"] = {
        "headers": ["ID", "Full Name", "Title", "Email", "Phone", "Location", "LinkedIn", "GitHub", "Portfolio URL", "Summary"],
        "rows": [[
            p.get("id", 1),
            p.get("full_name", ""),
            p.get("professional_title", ""),
            p.get("email", ""),
            p.get("phone", ""),
            p.get("location", ""),
            p.get("linkedin_url", ""),
            p.get("github_url", ""),
            p.get("portfolio_url", ""),
            p.get("summary", "")
        ]]
    }

    # 2. Education
    edu_rows = []
    for e in portfolio.get("education", []):
        edu_rows.append([
            e.get("id"),
            e.get("institution"),
            e.get("degree"),
            e.get("field_of_study"),
            e.get("start_year"),
            e.get("end_year"),
            e.get("grade_or_gpa"),
            e.get("location", ""),
            e.get("description", "")
        ])
    sheets_payload["Education"] = {
        "headers": ["ID", "Institution", "Degree", "Field of Study", "Start Year", "End Year", "Grade/GPA", "Location", "Description"],
        "rows": edu_rows
    }

    # 3. Skills
    skill_rows = []
    for s in portfolio.get("skills", []):
        skill_rows.append([
            s.get("id"),
            s.get("name"),
            s.get("category"),
            s.get("proficiency_level"),
            s.get("years_experience")
        ])
    sheets_payload["Skills"] = {
        "headers": ["ID", "Skill Name", "Category", "Proficiency Level", "Years Experience"],
        "rows": skill_rows
    }

    # 4. Certifications
    cert_rows = []
    for c in portfolio.get("certifications", []):
        cert_rows.append([
            c.get("id"),
            c.get("title"),
            c.get("issuing_organization"),
            c.get("issue_date"),
            c.get("expiration_date", "None"),
            c.get("credential_id", ""),
            c.get("skills_covered", "")
        ])
    sheets_payload["Certifications"] = {
        "headers": ["ID", "Certification Title", "Issuer", "Issue Date", "Expiration Date", "Credential ID", "Skills Covered"],
        "rows": cert_rows
    }

    # 5. Projects
    proj_rows = []
    for pr in portfolio.get("projects", []):
        hl = pr.get("highlights", [])
        hl_str = " | ".join(hl) if isinstance(hl, list) else str(hl)
        proj_rows.append([
            pr.get("id"),
            pr.get("title"),
            pr.get("role"),
            pr.get("tech_stack"),
            pr.get("description"),
            hl_str,
            pr.get("repo_url", ""),
            pr.get("live_url", "")
        ])
    sheets_payload["Projects"] = {
        "headers": ["ID", "Project Title", "Role", "Tech Stack", "Description", "Key Highlights", "Repository URL", "Live Demo URL"],
        "rows": proj_rows
    }

    # 6. Experience
    exp_rows = []
    for ex in portfolio.get("experience", []):
        hl = ex.get("highlights", [])
        hl_str = " | ".join(hl) if isinstance(hl, list) else str(hl)
        exp_rows.append([
            ex.get("id"),
            ex.get("job_title"),
            ex.get("company"),
            ex.get("employment_type"),
            ex.get("location"),
            ex.get("start_date"),
            ex.get("end_date") or "Present",
            ex.get("tech_stack", ""),
            ex.get("description"),
            hl_str
        ])
    sheets_payload["Experience"] = {
        "headers": ["ID", "Job Title", "Company", "Type", "Location", "Start Date", "End Date", "Tech Stack", "Description", "Achievements / Highlights"],
        "rows": exp_rows
    }

    # 7. Achievements
    ach_rows = []
    for a in portfolio.get("achievements", []):
        ach_rows.append([
            a.get("id"),
            a.get("title"),
            a.get("issuer"),
            a.get("issue_date"),
            a.get("category"),
            a.get("description")
        ])
    sheets_payload["Achievements"] = {
        "headers": ["ID", "Award Title", "Issuing Body", "Date", "Category", "Description"],
        "rows": ach_rows
    }

    # 8. Publications
    pub_rows = []
    for pu in portfolio.get("publications", []):
        pub_rows.append([
            pu.get("id"),
            pu.get("title"),
            pu.get("publisher_or_journal"),
            pu.get("publication_date"),
            pu.get("authors"),
            pu.get("url", ""),
            pu.get("doi", ""),
            pu.get("abstract", "")
        ])
    sheets_payload["Publications"] = {
        "headers": ["ID", "Paper Title", "Publisher/Journal", "Date", "Authors", "URL", "DOI", "Abstract"],
        "rows": pub_rows
    }

    # 9. Languages
    lang_rows = []
    for l in portfolio.get("languages", []):
        lang_rows.append([
            l.get("id"),
            l.get("language"),
            l.get("proficiency")
        ])
    sheets_payload["Languages"] = {
        "headers": ["ID", "Language", "Proficiency Level"],
        "rows": lang_rows
    }

    return {
        "status": "ready",
        "sheet_tabs": SHEET_TAB_ORDER,
        "sheets": sheets_payload,
        "total_records": sum(len(sheets_payload[t]["rows"]) for t in SHEET_TAB_ORDER)
    }

def generate_category_csv(category_name: str) -> str:
    """Generates standard CSV content for a single portfolio category."""
    data = format_portfolio_for_sheets()
    
    # Case-insensitive and underscore-insensitive lookup
    target_key = None
    clean_cat = category_name.strip().lower().replace(" ", "_")
    for key in data["sheets"].keys():
        if key.lower().replace(" ", "_") == clean_cat:
            target_key = key
            break
            
    if not target_key or target_key not in data["sheets"]:
        raise ValueError(f"Unknown sheet category: {category_name}. Available: {list(data['sheets'].keys())}")
    
    sheet_data = data["sheets"][target_key]
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(sheet_data["headers"])
    for row in sheet_data["rows"]:
        writer.writerow(row)
    return output.getvalue()

def sync_to_google_apps_script(web_app_url: str) -> Dict[str, Any]:
    """Pushes the entire local SQLite portfolio data directly to a Google Apps Script Web App."""
    if not web_app_url or not web_app_url.startswith("https://script.google.com"):
        return {
            "success": False,
            "error": "Invalid Apps Script Web App URL. Must start with https://script.google.com"
        }

    payload = format_portfolio_for_sheets()
    json_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        web_app_url,
        data=json_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            resp_body = resp.read().decode("utf-8")
            result = json.loads(resp_body)
            database.log_sync("export", "success", payload["total_records"], f"Synced to Apps Script: {resp.status}")
            return {"success": True, "details": result}
    except Exception as e:
        database.log_sync("export", "failed", 0, str(e))
        return {"success": False, "error": str(e)}

def handle_incoming_sheets_sync(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Processes incoming updates pushed from Google Sheets or Apps Script Webhook."""
    try:
        updated_count = 0
        # If payload contains 'skills'
        if "skills" in payload and isinstance(payload["skills"], list):
            for s in payload["skills"]:
                if "name" in s and "category" in s:
                    try:
                        database.add_category_item("skills", s)
                        updated_count += 1
                    except Exception:
                        pass
        
        database.log_sync("import", "success", updated_count, "Imported updates from Google Sheet")
        return {"success": True, "updated_count": updated_count}
    except Exception as e:
        database.log_sync("import", "failed", 0, str(e))
        return {"success": False, "error": str(e)}
