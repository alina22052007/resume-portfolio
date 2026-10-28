"""
Database Module for AI-Powered Portfolio Database & Resume Generator
Provides complete SQLite storage, schema initialization, seed data population,
and full CRUD operations across all portfolio entities.
"""

import os
import sqlite3
import json
from typing import Dict, List, Any, Optional

DB_FILE = os.path.join(os.path.dirname(__file__), "portfolio.db")
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")
SEED_FILE = os.path.join(os.path.dirname(__file__), "seed_data.sql")

VALID_CATEGORIES = [
    "personal_info",
    "education",
    "skills",
    "certifications",
    "projects",
    "experience",
    "achievements",
    "publications",
    "languages"
]

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_reseed: bool = False):
    """Initializes the database schema and seeds sample data if needed."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Read and execute schema
    if os.path.exists(SCHEMA_FILE):
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
    conn.commit()

    # Check if empty or forced reseed
    cursor.execute("SELECT COUNT(*) FROM personal_info")
    count = cursor.fetchone()[0]

    if count == 0 or force_reseed:
        if force_reseed:
            for cat in VALID_CATEGORIES:
                cursor.execute(f"DELETE FROM {cat}")
            cursor.execute("DELETE FROM sync_logs")
            cursor.execute("DELETE FROM customized_resumes")
            conn.commit()

        if os.path.exists(SEED_FILE):
            with open(SEED_FILE, "r", encoding="utf-8") as f:
                cursor.executescript(f.read())
            conn.commit()
            print("Successfully initialized and seeded portfolio database.")

    conn.close()

def get_full_portfolio() -> Dict[str, Any]:
    """Fetches all records across all 9 portfolio categories."""
    conn = get_db_connection()
    cursor = conn.cursor()

    portfolio = {}
    for cat in VALID_CATEGORIES:
        cursor.execute(f"SELECT * FROM {cat} ORDER BY id ASC")
        rows = cursor.fetchall()
        portfolio[cat] = [dict(row) for row in rows]
        
        # Parse JSON fields for projects and experience highlights
        if cat == "projects":
            for item in portfolio[cat]:
                if isinstance(item.get("highlights"), str):
                    try:
                        item["highlights"] = json.loads(item["highlights"])
                    except Exception:
                        item["highlights"] = [h.strip() for h in item["highlights"].split("\n") if h.strip()]
        elif cat == "experience":
            for item in portfolio[cat]:
                if isinstance(item.get("highlights"), str):
                    try:
                        item["highlights"] = json.loads(item["highlights"])
                    except Exception:
                        item["highlights"] = [h.strip() for h in item["highlights"].split("\n") if h.strip()]

    # Make personal_info a single object if available
    personal = portfolio.get("personal_info", [])
    portfolio["profile"] = personal[0] if personal else {}

    conn.close()
    return portfolio

def get_category_items(category: str) -> List[Dict[str, Any]]:
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {category} ORDER BY id ASC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def add_category_item(category: str, data: Dict[str, Any]) -> int:
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")
    
    # Sanitize and serialize json fields if necessary
    item = dict(data)
    item.pop("id", None)
    item.pop("created_at", None)
    item.pop("updated_at", None)

    if category in ("projects", "experience") and isinstance(item.get("highlights"), (list, dict)):
        item["highlights"] = json.dumps(item["highlights"])

    keys = list(item.keys())
    placeholders = ", ".join(["?"] * len(keys))
    columns = ", ".join(keys)
    values = [item[k] for k in keys]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {category} ({columns}) VALUES ({placeholders})", values)
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def update_category_item(category: str, item_id: int, data: Dict[str, Any]) -> bool:
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")

    item = dict(data)
    item.pop("id", None)
    item.pop("created_at", None)
    item.pop("updated_at", None)

    if category in ("projects", "experience") and isinstance(item.get("highlights"), (list, dict)):
        item["highlights"] = json.dumps(item["highlights"])

    keys = list(item.keys())
    set_clause = ", ".join([f"{k} = ?" for k in keys])
    values = [item[k] for k in keys] + [item_id]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {category} SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", values)
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_category_item(category: str, item_id: int) -> bool:
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {category} WHERE id = ?", (item_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def log_sync(sync_type: str, status: str, record_count: int, details: str = ""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sync_logs (sync_type, status, record_count, details) VALUES (?, ?, ?, ?)",
        (sync_type, status, record_count, details)
    )
    conn.commit()
    conn.close()

def get_sync_logs(limit: int = 20) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sync_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def save_customized_resume(
    target_job_title: str,
    target_company: str,
    job_description: str,
    match_score: float,
    selected_skills: List[str],
    selected_projects: List[int],
    selected_experiences: List[int],
    selected_certifications: List[int],
    tailored_summary: str,
    resume_payload: Dict[str, Any]
) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO customized_resumes (
            target_job_title, target_company, job_description, match_score,
            selected_skills, selected_projects, selected_experiences, selected_certifications,
            tailored_summary, resume_payload
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        target_job_title,
        target_company,
        job_description,
        match_score,
        json.dumps(selected_skills),
        json.dumps(selected_projects),
        json.dumps(selected_experiences),
        json.dumps(selected_certifications),
        tailored_summary,
        json.dumps(resume_payload)
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_customized_resumes(limit: int = 10) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customized_resumes ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

if __name__ == "__main__":
    init_db(force_reseed=True)
    p = get_full_portfolio()
    print("Database test passed. Counts:")
    for k, v in p.items():
        if isinstance(v, list):
            print(f" - {k}: {len(v)} records")

