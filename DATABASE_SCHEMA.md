# 🗄️ Database Architecture & Relational Schema Documentation

## 1. Overview
The **PortfoliAI System** utilizes a normalized, relational SQLite 3 database (`portfolio.db`) designed to act as the single source of truth for all professional and technical information of a candidate.

To ensure consistency, eliminate redundancy, and facilitate ATS keyword matching and dynamic resume generation, the database is partitioned into **9 dedicated category tables**, plus system tables for audit tracking and saved resumes.

---

## 2. Entity-Relationship (ER) Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CENTRAL PORTFOLIO SCHEMA                           │
└─────────────────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────┐             ┌──────────────────────────┐
 │      personal_info       │             │        education         │
 ├──────────────────────────┤             ├──────────────────────────┤
 │ id: INTEGER (PK)         │             │ id: INTEGER (PK)         │
 │ full_name: TEXT          │             │ institution: TEXT        │
 │ professional_title: TEXT │             │ degree: TEXT             │
 │ email: TEXT              │             │ field_of_study: TEXT     │
 │ phone: TEXT              │             │ start_year: TEXT         │
 │ location: TEXT           │             │ end_year: TEXT           │
 │ linkedin_url: TEXT       │             │ grade_or_gpa: TEXT       │
 │ github_url: TEXT         │             │ description: TEXT        │
 │ portfolio_url: TEXT      │             └──────────────────────────┘
 │ summary: TEXT            │
 └──────────────────────────┘

 ┌──────────────────────────┐             ┌──────────────────────────┐
 │          skills          │             │        experience        │
 ├──────────────────────────┤             ├──────────────────────────┤
 │ id: INTEGER (PK)         │             │ id: INTEGER (PK)         │
 │ name: TEXT (UNIQUE)      │             │ job_title: TEXT          │
 │ category: TEXT (CHECK)   │             │ company: TEXT            │
 │ proficiency_level: TEXT  │             │ employment_type: TEXT    │
 │ years_experience: REAL   │             │ start_date: TEXT         │
 └──────────────────────────┘             │ end_date: TEXT           │
                                          │ description: TEXT        │
 ┌──────────────────────────┐             │ highlights: TEXT (JSON)  │
 │         projects         │             │ tech_stack: TEXT         │
 ├──────────────────────────┤             └──────────────────────────┘
 │ id: INTEGER (PK)         │
 │ title: TEXT              │             ┌──────────────────────────┐
 │ role: TEXT               │             │      certifications      │
 │ tech_stack: TEXT         │             ├──────────────────────────┤
 │ description: TEXT        │             │ id: INTEGER (PK)         │
 │ highlights: TEXT (JSON)  │             │ title: TEXT              │
 │ repo_url: TEXT           │             │ issuing_org: TEXT        │
 │ live_url: TEXT           │             │ issue_date: TEXT         │
 └──────────────────────────┘             │ credential_id: TEXT      │
                                          └──────────────────────────┘

 ┌──────────────────────────┐             ┌──────────────────────────┐
 │       achievements       │             │       publications       │
 ├──────────────────────────┤             ├──────────────────────────┤
 │ id: INTEGER (PK)         │             │ id: INTEGER (PK)         │
 │ title: TEXT              │             │ title: TEXT              │
 │ issuer: TEXT             │             │ publisher: TEXT          │
 │ issue_date: TEXT         │             │ publication_date: TEXT   │
 │ category: TEXT           │             │ authors: TEXT            │
 │ description: TEXT        │             │ doi: TEXT                │
 └──────────────────────────┘             │ abstract: TEXT           │
                                          └──────────────────────────┘

 ┌──────────────────────────┐             ┌──────────────────────────┐
 │        languages         │             │    customized_resumes    │
 ├──────────────────────────┤             ├──────────────────────────┤
 │ id: INTEGER (PK)         │             │ id: INTEGER (PK)         │
 │ language: TEXT (UNIQUE)  │             │ target_job_title: TEXT   │
 │ proficiency: TEXT        │             │ match_score: REAL        │
 └──────────────────────────┘             │ resume_payload: TEXT     │
                                          └──────────────────────────┘
```

---

## 3. Detailed Table Specifications

### 3.1 `personal_info`
Maintains core identity and contact details.
- `id` (INTEGER, Primary Key, Auto Increment)
- `full_name` (TEXT, NOT NULL): Candidate's full name.
- `professional_title` (TEXT, NOT NULL): Target headline (e.g. *Full Stack & AI Systems Engineer*).
- `email` (TEXT, NOT NULL): Valid email address.
- `phone` (TEXT, NOT NULL): Contact phone number.
- `location` (TEXT, NOT NULL): Geographic location (City, State, Country).
- `linkedin_url` (TEXT): LinkedIn profile link.
- `github_url` (TEXT): GitHub code repository portfolio.
- `portfolio_url` (TEXT): Personal website link.
- `summary` (TEXT, NOT NULL): Comprehensive baseline career summary.
- `created_at`, `updated_at` (TIMESTAMP): Automatic timestamp auditing.

### 3.2 `education`
Stores degrees, collegiate institutions, and academic distinction.
- `id` (INTEGER, Primary Key)
- `institution` (TEXT, NOT NULL): College / University name.
- `degree` (TEXT, NOT NULL): e.g. *Bachelor of Technology (B.Tech)*.
- `field_of_study` (TEXT, NOT NULL): e.g. *Computer Science and Engineering*.
- `start_year` (TEXT, NOT NULL): e.g. `2021`
- `end_year` (TEXT, NOT NULL): e.g. `2025`
- `grade_or_gpa` (TEXT): e.g. `9.2 / 10.0 CGPA`
- `description` (TEXT): Relevant coursework and academic honors.

### 3.3 `skills`
Maintains verified competencies categorized for ATS matching.
- `id` (INTEGER, Primary Key)
- `name` (TEXT, NOT NULL, UNIQUE): Skill name (e.g. *Python, Docker, FastAPI*).
- `category` (TEXT, NOT NULL): CHECK constraint `('technical', 'soft', 'framework', 'database', 'cloud_devops', 'tool')`.
- `proficiency_level` (TEXT, NOT NULL): CHECK constraint `('Beginner', 'Intermediate', 'Advanced', 'Expert')`.
- `years_experience` (REAL, DEFAULT 1.0): Years of practical hands-on experience.

### 3.4 `certifications`
Official industry and academic credentials.
- `id` (INTEGER, Primary Key)
- `title` (TEXT, NOT NULL): Certification name.
- `issuing_organization` (TEXT, NOT NULL): e.g. *Amazon Web Services, Google Cloud*.
- `issue_date` (TEXT, NOT NULL): ISO date (`YYYY-MM-DD`).
- `expiration_date` (TEXT): Expiry or NULL for lifetime credentials.
- `credential_id` (TEXT): Verification ID or license number.
- `skills_covered` (TEXT): Skills validated by the credential.

### 3.5 `projects`
Production, open-source, and research project portfolio.
- `id` (INTEGER, Primary Key)
- `title` (TEXT, NOT NULL): Project name.
- `role` (TEXT, NOT NULL): Candidate's role (e.g. *Lead Backend Architect*).
- `tech_stack` (TEXT, NOT NULL): Comma-delimited list of technologies.
- `description` (TEXT, NOT NULL): High-level system overview.
- `highlights` (TEXT, NOT NULL): JSON array of quantifiable achievement bullets.
- `repo_url` (TEXT): GitHub repository URL.
- `live_url` (TEXT): Live deployment or demonstration link.

### 3.6 `experience`
Internships, contract, and full-time professional roles.
- `id` (INTEGER, Primary Key)
- `job_title` (TEXT, NOT NULL): Role designation.
- `company` (TEXT, NOT NULL): Employer name.
- `employment_type` (TEXT): CHECK constraint `('Full-time', 'Part-time', 'Internship', 'Contract', 'Freelance')`.
- `location` (TEXT, NOT NULL): On-site/Hybrid/Remote city.
- `start_date` (TEXT, NOT NULL): Start period.
- `end_date` (TEXT): End period or 'Present'.
- `description` (TEXT, NOT NULL): Scope of responsibilities.
- `highlights` (TEXT, NOT NULL): JSON array of quantifiable results achieved.
- `tech_stack` (TEXT): Technologies utilized in the role.

### 3.7 `achievements`
Awards, competitive programming ranks, and hackathon wins.
- `id` (INTEGER, Primary Key)
- `title` (TEXT, NOT NULL): Honor / award name.
- `issuer` (TEXT, NOT NULL): Awarding authority.
- `category` (TEXT): Academic, Hackathon, Professional, Leadership.

### 3.8 `publications`
Peer-reviewed conference papers, journal articles, and preprints.
- `id` (INTEGER, Primary Key)
- `title` (TEXT, NOT NULL): Paper title.
- `publisher_or_journal` (TEXT, NOT NULL): e.g. *IEEE ICACC*.
- `publication_date` (TEXT, NOT NULL): Date of publication.
- `authors` (TEXT, NOT NULL): Author citation list.
- `doi` (TEXT): Digital Object Identifier.
- `abstract` (TEXT, NOT NULL): Executive summary of research.

### 3.9 `languages`
Spoken and written language proficiencies.
- `id` (INTEGER, Primary Key)
- `language` (TEXT, NOT NULL, UNIQUE)
- `proficiency` (TEXT, NOT NULL): CHECK constraint.

### 3.10 `sync_logs`
Audit trails for Google Sheets export and import events.
- `id` (INTEGER, Primary Key)
- `sync_type` (TEXT): 'export', 'import', 'webhook'.
- `status` (TEXT): 'success', 'failed'.
- `record_count` (INTEGER): Number of synced entities.
- `details` (TEXT): System diagnostics or error messages.
- `timestamp` (TIMESTAMP): UTC event time.

---

## 4. Key Relational Indexes
To optimize ATS query performance during job description matching:
```sql
CREATE INDEX idx_skills_category ON skills(category);
CREATE INDEX idx_projects_tech ON projects(tech_stack);
CREATE INDEX idx_exp_company ON experience(company);
CREATE INDEX idx_edu_degree ON education(degree);
```

