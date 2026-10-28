-- ==============================================================================
-- AI-Powered Portfolio Database & Dynamic Resume Generator Schema
-- Database: SQLite 3
-- Designed for modularity, strict relational integrity, and rapid querying
-- ==============================================================================

-- 1. Personal & Contact Information
CREATE TABLE IF NOT EXISTS personal_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    professional_title TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    location TEXT NOT NULL,
    linkedin_url TEXT,
    github_url TEXT,
    portfolio_url TEXT,
    summary TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Educational Qualifications
CREATE TABLE IF NOT EXISTS education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    institution TEXT NOT NULL,
    degree TEXT NOT NULL,
    field_of_study TEXT NOT NULL,
    start_year TEXT NOT NULL,
    end_year TEXT NOT NULL,
    grade_or_gpa TEXT,
    location TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Skills (Technical, Soft, Tools, Frameworks, Cloud/DevOps)
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL CHECK(category IN ('technical', 'soft', 'framework', 'database', 'cloud_devops', 'tool')),
    proficiency_level TEXT NOT NULL CHECK(proficiency_level IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')),
    years_experience REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Certifications & Online Courses
CREATE TABLE IF NOT EXISTS certifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    issuing_organization TEXT NOT NULL,
    issue_date TEXT NOT NULL,
    expiration_date TEXT,
    credential_id TEXT,
    credential_url TEXT,
    skills_covered TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Projects & Descriptions
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    role TEXT NOT NULL,
    category TEXT DEFAULT 'Software Development',
    description TEXT NOT NULL,
    tech_stack TEXT NOT NULL, -- comma separated or JSON string
    repo_url TEXT,
    live_url TEXT,
    highlights TEXT NOT NULL, -- JSON array or bullet points
    start_date TEXT,
    end_date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Internships & Work Experience
CREATE TABLE IF NOT EXISTS experience (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT NOT NULL,
    company TEXT NOT NULL,
    employment_type TEXT DEFAULT 'Full-time' CHECK(employment_type IN ('Full-time', 'Part-time', 'Internship', 'Contract', 'Freelance')),
    location TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT, -- NULL or 'Present' if current
    is_current INTEGER DEFAULT 0 CHECK(is_current IN (0, 1)),
    description TEXT NOT NULL,
    highlights TEXT NOT NULL, -- Bullet points of accomplishments
    tech_stack TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Achievements & Awards
CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    issuer TEXT NOT NULL,
    issue_date TEXT NOT NULL,
    category TEXT DEFAULT 'Academic' CHECK(category IN ('Academic', 'Hackathon', 'Professional', 'Leadership', 'Other')),
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Research Papers, Publications & Relevant Activities
CREATE TABLE IF NOT EXISTS publications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    publisher_or_journal TEXT NOT NULL,
    publication_date TEXT NOT NULL,
    authors TEXT NOT NULL,
    url TEXT,
    doi TEXT,
    abstract TEXT NOT NULL,
    keywords TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Languages & Competencies
CREATE TABLE IF NOT EXISTS languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    language TEXT NOT NULL UNIQUE,
    proficiency TEXT NOT NULL CHECK(proficiency IN ('Elementary', 'Conversational', 'Professional working', 'Full professional', 'Native or bilingual')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Google Sheets Synchronization Log
CREATE TABLE IF NOT EXISTS sync_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sync_type TEXT NOT NULL CHECK(sync_type IN ('export', 'import', 'webhook')),
    status TEXT NOT NULL CHECK(status IN ('success', 'failed', 'pending')),
    record_count INTEGER DEFAULT 0,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Saved Customized Resumes
CREATE TABLE IF NOT EXISTS customized_resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_job_title TEXT NOT NULL,
    target_company TEXT,
    job_description TEXT NOT NULL,
    match_score REAL DEFAULT 0.0,
    selected_skills TEXT,        -- JSON array of skill IDs or names
    selected_projects TEXT,      -- JSON array of project IDs
    selected_experiences TEXT,   -- JSON array of experience IDs
    selected_certifications TEXT,-- JSON array of certification IDs
    tailored_summary TEXT NOT NULL,
    resume_payload TEXT NOT NULL,-- Full JSON representation of the generated resume
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_skills_category ON skills(category);
CREATE INDEX IF NOT EXISTS idx_projects_tech ON projects(tech_stack);
CREATE INDEX IF NOT EXISTS idx_exp_company ON experience(company);
CREATE INDEX IF NOT EXISTS idx_edu_degree ON education(degree);

