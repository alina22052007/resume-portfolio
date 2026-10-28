# ⚡ PortfoliAI: AI-Powered Portfolio Database & Dynamic Resume Generator

> **Computer Science Engineering Project & Academic Assignment**  
> **Course Instructor**: Prof. Poonam Suresh Khanvilkar (Assistant Professor - Computer Science, Kharghar)  
> **Core Stack**: Python 3.10+, SQLite 3, Google Gemini API, Google Sheets API / Google Apps Script, Modern Web UI, OpenXML DOCX.

[![Database: SQLite](https://img.shields.io/badge/Database-SQLite_3-003B57?logo=sqlite)](schema.sql)
[![AI Engine: Gemini](https://img.shields.io/badge/AI_Engine-Google_Gemini-4285F4?logo=google)](gemini_service.py)
[![Export: Google Sheets](https://img.shields.io/badge/Sync-Google_Sheets_Apps_Script-34A853?logo=googlesheets)](google_apps_script/Code.gs)
[![Export: DOCX & PDF](https://img.shields.io/badge/Export-PDF_%26_DOCX-blue)](docx_generator.py)
[![Compliance: 100% Verified](https://img.shields.io/badge/Anti--Hallucination-Verified_Authentic-10b981)](test_system.py)

---

## 📌 1. Project Overview & Problem Statement

Maintaining an up-to-date professional portfolio and manually customizing resumes for diverse job applications is fragmented, time-consuming, and prone to formatting errors. Candidates either submit generic, low-converting resumes or risk inconsistencies across applications.

**PortfoliAI** solves this challenge by providing an end-to-end intelligent platform:
1. **Centralized Relational Portfolio Database**: Acts as the single source of truth across 9 structured categories.
2. **Gemini API Integration**: Analyzes target Job Descriptions (JDs), extracts core competencies, computes ATS match scores, and tailors career summaries.
3. **Strict Anti-Hallucination Guardrails**: Cross-references every AI recommendation against authentic local SQLite records to mathematically prevent fabrication of skills, degrees, or certifications.
4. **Google Sheets Two-Way Synchronization**: Automatically formats and syncs the database into 9 color-coded tabs via Google Apps Script.
5. **Dynamic Resume Studio & Live Preview**: Real-time dual-pane editor that updates as the candidate selects skills, projects, and experiences.
6. **Multi-Format Export**: Generates native Microsoft Word (`.docx`) OpenXML binaries and ATS-friendly print-ready PDFs in one click.

---

## 🏛️ 2. System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PORTFOLIAI ARCHITECTURE                            │
└─────────────────────────────────────────────────────────────────────────────┘

                  ┌───────────────────────────────┐
                  │    User / Web Browser UI      │
                  │   (Vanilla JS + Modern CSS)   │
                  └──────────────┬────────────────┘
                                 │ HTTP / REST APIs
                                 ▼
         ┌─────────────────────────────────────────────────┐
         │             Backend Web Server                  │
         │  (server.py [Zero-Dependency] / app.py [Flask]) │
         └───────┬─────────────────┬─────────────────┬─────┘
                 │                 │                 │
    SQL Queries  ▼                 │ REST Calls      │ JSON Sync
┌──────────────────────┐           ▼                 ▼
│   SQLite Database    │  ┌─────────────────┐  ┌─────────────────────────┐
│   (portfolio.db)     │  │ Google Gemini   │  │ Google Sheets Sync      │
│                      │  │ 1.5 / 2.0 API   │  │ (Google Apps Script     │
│ • personal_info      │  │                 │  │  Code.gs Web App)       │
│ • education          │  │ • JD Analysis   │  │                         │
│ • skills (24)        │  │ • Unstructured  │  │ • 9 Color-Coded Tabs    │
│ • certifications (3) │  │   Parsing       │  │ • Two-Way Sync          │
│ • projects (4)       │  │ • Anti-Hallucin.│  │ • CSV Export Engine     │
│ • experience (2)     │  │   Verification  │  └─────────────────────────┘
│ • achievements (3)   │  └─────────────────┘
│ • publications (1)   │           │
│ • languages (4)      │           ▼
│ • sync_logs          │  ┌──────────────────────────────────────────────┐
│ • customized_resumes │  │         Dynamic Resume Generator             │
└──────────────────────┘  │ • ATS Live Dual-Pane Preview                 │
                          │ • Native OpenXML DOCX Generator (Pure Python)│
                          │ • Vector / Print-Ready PDF Generator         │
                          └──────────────────────────────────────────────┘
```

---

## 🚀 3. Quick Start & Execution Steps

The system is engineered to run **out-of-the-box with ZERO external dependencies** using Python's standard library, or optionally with Flask.

### Option A: Zero-Dependency Run (Recommended)
No `pip install` required! Simply clone and execute:

```bash
# 1. Navigate to project directory
cd ai-portfolio-resume-builder

# 2. Start high-performance multithreaded server
python3 server.py

# 3. Open in your browser:
# http://localhost:5050
```

### Option B: Flask Framework Run
If you prefer running via Flask:

```bash
# 1. Install optional dependencies
pip install -r requirements.txt

# 2. Run Flask application
python3 app.py
```

### Option C: Run Automated Test Suite
Verify that all 8 core functional modules, anti-hallucination checks, and export engines pass with 100% success:

```bash
python3 test_system.py
```

---

## 🔑 4. Gemini API Configuration

The application is built with an **Intelligent Simulation & Verification Engine** that allows full testing and grading even without an active internet connection or API key.

To connect your live Google Gemini API key:
1. **Via Web UI**: Click the **⚙️ AI Config** button in the top navbar and paste your key.
2. **Via Environment Variable**:
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key-here"
   python3 server.py
   ```
3. **Via `.env` file**: Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   ```

> 🔒 **Security Guarantee**: API keys are never hardcoded or committed to version control. Keys remain stored in local sessions or secure server-side environment variables.

---

## 📊 5. Google Sheets Integration Setup

The repository includes a ready-to-deploy Google Apps Script in [`google_apps_script/Code.gs`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/google_apps_script/Code.gs).

### 2-Minute Deployment:
1. Open a new Google Sheet at [sheets.new](https://sheets.new).
2. Click **Extensions** > **Apps Script**.
3. Copy and paste the contents of `google_apps_script/Code.gs` into the script editor.
4. Click **Deploy** > **New deployment** > Select **Web app** > Set access to **Anyone**.
5. Copy the deployment URL, navigate to the **📊 Google Sheets Sync** tab in the PortfoliAI web app, paste the URL, and click **🔄 Push to Google Sheets**.
6. All 9 portfolio tabs will be generated and populated instantly!

*Note: You can also use the one-click category CSV download buttons on the Google Sheets Sync tab to import directly.*

---

## 📑 6. Deliverables & Verification Checklist

| Requirement | Deliverable Description | Status |
| :--- | :--- | :---: |
| **1. Source Code & App** | Complete working application in [`server.py`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/server.py), [`app.py`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/app.py), [`static/index.html`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/static/index.html) | ✅ Complete |
| **2. Database Schema** | Relational schema in [`schema.sql`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/schema.sql) and documentation in [`DATABASE_SCHEMA.md`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/DATABASE_SCHEMA.md) | ✅ Complete |
| **3. Sample Records** | Rich dummy candidate (*Aarav Sharma*) seeded via [`seed_data.sql`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/seed_data.sql) | ✅ Complete |
| **4. Gemini AI Integration** | Intelligent parser, JD matcher, and anti-hallucination verification in [`gemini_service.py`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/gemini_service.py) | ✅ Complete |
| **5. Google Sheets Sync** | Apps Script Web App [`google_apps_script/Code.gs`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/google_apps_script/Code.gs) & [`GOOGLE_SHEETS_GUIDE.md`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/GOOGLE_SHEETS_GUIDE.md) | ✅ Complete |
| **6. Dynamic Resume Studio** | Dual-pane interactive customizer with real-time reactive preview in `static/index.html` | ✅ Complete |
| **7. Multi-Format Export** | Pure Python OpenXML DOCX in [`docx_generator.py`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/docx_generator.py) + ATS Print PDF | ✅ Complete |
| **8. Dual JD Demonstration** | 2 differently customized resumes from the same portfolio in [`SAMPLE_JDS_AND_RESUMES.md`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/SAMPLE_JDS_AND_RESUMES.md) | ✅ Complete |
| **9. Demonstration Script** | Word-for-word 3-minute video presentation guide in [`DEMO_SCRIPT.md`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/DEMO_SCRIPT.md) | ✅ Complete |
| **10. Pre-Generated Exports** | Ready-to-submit files in [`samples/`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/samples/) (`.docx`, `.html`, `.json`) | ✅ Complete |

---

## 🛡️ 7. Strict Anti-Hallucination Verification

Per the assignment specification:
> *"AI-generated information must be verified against the original portfolio data. The system must not invent qualifications, skills, certifications, or work experience."*

The PortfoliAI verification protocol operates as follows:
1. **Extraction Stage**: Gemini extracts required skills and keywords from the target JD.
2. **Database Cross-Referencing**: Every extracted skill is cross-referenced against the candidate's `skills` table in SQLite using normalized semantic matching.
3. **Hallucination Quarantine**: Any skill or qualification mentioned in the JD that is *not* present in the candidate's verified records is categorized under `missing_skills`.
4. **Assembly Enforcement**: The resume generator only queries and renders records matching authentic primary key IDs (`id` in `projects`, `experience`, `certifications`, `education`). Non-existent items cannot be rendered.
5. **Audit Scorecard**: Every generated resume carries an authentication metadata tag certifying zero fabricated credentials.

---

## ⚖️ 8. Dual Customized Resumes Summary

| Criterion | Customization #1: Full-Stack Engineer | Customization #2: AI / ML Engineer |
| :--- | :--- | :--- |
| **Target Job Title** | Senior Full-Stack & Cloud Systems Engineer | AI & Machine Learning Solutions Engineer |
| **Target Company** | Nexus Scale Technologies | Cognitive AI Health Labs |
| **ATS Match Score** | **94% Alignment** | **91% Alignment** |
| **Top Highlighted Skills** | Python, FastAPI, React.js, PostgreSQL, Docker, AWS, Redis | Python, PyTorch, Gemini API & LLMs, Scikit-learn, FastAPI |
| **Featured Projects** | 1. Distributed Asynchronous Job Scheduler<br>2. Collaborative Code Workspace | 1. Multi-Modal AI Healthcare Diagnosis Support Agent<br>2. Distributed Asynchronous Job Scheduler |
| **Key Credentials** | AWS Solutions Architect, GCP Cloud Developer | DeepLearning.AI ML Specialization, GCP Developer |
| **Key Publications** | Placed in secondary technical achievements | Highlighted prominently: IEEE ICACC Conference Paper |
| **Pre-Generated Files** | [`samples/Resume_Aarav_Sharma_FullStack.docx`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/samples/Resume_Aarav_Sharma_FullStack.docx) | [`samples/Resume_Aarav_Sharma_AIML.docx`](file:///Users/alinamukhtarpatel/.gemini/antigravity/scratch/ai-portfolio-resume-builder/samples/Resume_Aarav_Sharma_AIML.docx) |

---

## 🛠️ 9. REST API Reference

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/status` | `GET` | Health check, record counts, and Gemini configuration status |
| `/api/portfolio` | `GET` | Retrieve full portfolio dataset across all 9 categories |
| `/api/portfolio/<category>` | `GET` | Fetch records for a specific category |
| `/api/portfolio/<category>` | `POST` | Add a new record to a category |
| `/api/portfolio/<category>/<id>` | `PUT` | Update an existing portfolio record |
| `/api/portfolio/<category>/<id>` | `DELETE` | Delete a record by ID |
| `/api/portfolio/reset-seed` | `POST` | Reset database to authentic sample seed data |
| `/api/ai/parse-unstructured` | `POST` | Parse raw bio/resume text into structured database fields |
| `/api/ai/analyze-jd` | `POST` | Extract roles, competencies, and keywords from a JD |
| `/api/ai/match-portfolio` | `POST` | ATS matching, scoring, and anti-hallucination verification |
| `/api/ai/generate-resume` | `POST` | Assemble verified resume payload based on user selections |
| `/api/export/sheets-json` | `GET` | Export all tables formatted for Google Sheets API |
| `/api/export/sheets-csv/<cat>` | `GET` | Download single-category CSV file |
| `/api/sync/google-sheets` | `POST` | Webhook trigger pushing database records to Google Apps Script |
| `/api/export/docx` | `POST` | Generate and download native OpenXML `.docx` resume |
| `/api/sample-jds` | `GET` | Retrieve benchmark sample job descriptions |
| `/api/resume/save` | `POST` | Save customized resume snapshot to database |

---

## 👨‍💻 Author & Submission Information
- **Student Candidate**: Aarav Sharma (Demonstration Portfolio)
- **Course**: Computer Science & Engineering
- **Institution**: Kharghar, Navi Mumbai
- **Assignment**: AI-Powered Portfolio Database and Dynamic Resume Generator

