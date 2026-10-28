-- Sample Seed Data for AI Portfolio Database

-- Personal Info
INSERT INTO personal_info (id, full_name, professional_title, email, phone, location, linkedin_url, github_url, portfolio_url, summary)
VALUES (
    1,
    'Aarav Sharma',
    'Full Stack & AI Systems Engineer',
    'aarav.sharma.demo@example.com',
    '+91 98765 43210',
    'Navi Mumbai, MH, India',
    'https://linkedin.com/in/aarav-sharma-demo',
    'https://github.com/aaravsharma-dev',
    'https://aaravsharma.dev',
    'Versatile Software Engineer with strong foundations in distributed backend systems, modern web architecture, and applied machine learning. Proven track record of architecting scalable RESTful microservices, fine-tuning LLMs, and deploying cloud-native containerized applications. Passionate about solving complex problems at the intersection of full-stack engineering and intelligent automation.'
);

-- Education
INSERT INTO education (id, institution, degree, field_of_study, start_year, end_year, grade_or_gpa, location, description)
VALUES 
(
    1,
    'University Institute of Technology, Kharghar',
    'Bachelor of Technology (B.Tech)',
    'Computer Science and Engineering',
    '2021',
    '2025',
    '9.2 / 10.0 CGPA',
    'Navi Mumbai, India',
    'Relevant Coursework: Data Structures & Algorithms, Distributed Systems, Database Management Systems, Machine Learning, Cloud Computing, Object-Oriented Analysis & Design.'
),
(
    2,
    'St. Xavier Higher Secondary College',
    'Higher Secondary Certificate (HSC)',
    'Science (PCM & Computer Science)',
    '2019',
    '2021',
    '94.8%',
    'Mumbai, India',
    'Graduated with Distinction in Mathematics and Computer Science.'
);

-- Skills
INSERT INTO skills (name, category, proficiency_level, years_experience) VALUES
('Python', 'technical', 'Expert', 4.0),
('JavaScript (ES6+)', 'technical', 'Expert', 3.5),
('TypeScript', 'technical', 'Advanced', 2.5),
('React.js', 'framework', 'Advanced', 3.0),
('Next.js', 'framework', 'Advanced', 2.0),
('Node.js', 'technical', 'Advanced', 3.0),
('FastAPI', 'framework', 'Advanced', 2.5),
('Flask', 'framework', 'Advanced', 3.0),
('PostgreSQL', 'database', 'Advanced', 3.0),
('SQLite', 'database', 'Expert', 3.5),
('MongoDB', 'database', 'Intermediate', 2.0),
('Docker', 'cloud_devops', 'Advanced', 2.5),
('Kubernetes', 'cloud_devops', 'Intermediate', 1.5),
('AWS (S3, EC2, Lambda)', 'cloud_devops', 'Advanced', 2.0),
('Git & GitHub CI/CD', 'tool', 'Expert', 4.0),
('RESTful API Design', 'technical', 'Expert', 3.5),
('GraphQL', 'technical', 'Intermediate', 1.5),
('PyTorch', 'framework', 'Advanced', 2.0),
('TensorFlow', 'framework', 'Intermediate', 2.0),
('Scikit-learn', 'framework', 'Advanced', 2.5),
('Gemini API & LLMs', 'technical', 'Advanced', 2.0),
('Agile / Scrum Methodology', 'soft', 'Advanced', 2.5),
('Technical Problem Solving', 'soft', 'Expert', 4.0),
('Cross-Functional Collaboration', 'soft', 'Expert', 3.5);

-- Certifications
INSERT INTO certifications (id, title, issuing_organization, issue_date, expiration_date, credential_id, credential_url, skills_covered)
VALUES
(
    1,
    'AWS Certified Solutions Architect – Associate',
    'Amazon Web Services',
    '2024-03-15',
    '2027-03-15',
    'AWS-ASA-892104',
    'https://aws.amazon.com/verification/AWS-ASA-892104',
    'Cloud Architecture, High Availability, S3, EC2, IAM, VPC, Microservices'
),
(
    2,
    'DeepLearning.AI Machine Learning Specialization',
    'Coursera / Stanford Online',
    '2023-11-20',
    NULL,
    'COURSERA-ML-77291',
    'https://coursera.org/verify/COURSERA-ML-77291',
    'Supervised Learning, Neural Networks, PyTorch, Model Evaluation, Unsupervised Learning'
),
(
    3,
    'Google Cloud Professional Cloud Developer',
    'Google Cloud',
    '2024-08-10',
    '2026-08-10',
    'GCP-PCD-44102',
    'https://google.accredible.com/GCP-PCD-44102',
    'Cloud Run, Kubernetes Engine, Cloud Functions, Pub/Sub, Firestore'
);

-- Projects
INSERT INTO projects (id, title, role, category, description, tech_stack, repo_url, live_url, highlights, start_date, end_date)
VALUES
(
    1,
    'Distributed Asynchronous Job Scheduler & Worker Pool',
    'Lead Backend Architect',
    'Distributed Systems',
    'High-throughput distributed task processing queue with rate limiting, retry semantics, and live metrics dashboard.',
    'Python, FastAPI, Redis, PostgreSQL, Docker, Prometheus',
    'https://github.com/aaravsharma-dev/distributed-task-runner',
    'https://runner-demo.aaravsharma.dev',
    '["Engineered a multi-worker asynchronous task queue capable of handling 8,000+ jobs/sec with sub-50ms latency.", "Implemented exponential backoff, dead-letter queues, and dynamic priority scheduling to prevent worker starvation.", "Reduced infrastructure compute costs by 34% by optimizing thread pool concurrency and connection pooling."]',
    '2024-01-10',
    '2024-05-20'
),
(
    2,
    'Multi-Modal AI Healthcare Diagnosis Support Agent',
    'AI & Full Stack Developer',
    'Artificial Intelligence',
    'End-to-end clinical diagnosis assistant processing medical imaging (X-rays) and clinical notes using Gemini Multimodal LLM.',
    'Python, PyTorch, Gemini API, FastAPI, React.js, Tailwind CSS',
    'https://github.com/aaravsharma-dev/med-gemini-assistant',
    'https://medai.aaravsharma.dev',
    '["Integrated Gemini Multimodal Vision API to parse radiologist reports with 94.2% diagnostic concordance against benchmark datasets.", "Designed strict hallucination verification guardrails ensuring zero medical claims are generated outside authorized medical corpora.", "Built a HIPAA-conscious React front-end featuring interactive DICOM image heatmaps and citation tracing."]',
    '2023-08-15',
    '2023-12-10'
),
(
    3,
    'Real-Time Collaborative Code & Markdown Workspace',
    'Full Stack Engineer',
    'Web Engineering',
    'Multiplayer markdown documentation editor with conflict-free replicated data types (CRDTs) and syntax highlighting.',
    'TypeScript, Node.js, WebSockets, React, Yjs, Docker',
    'https://github.com/aaravsharma-dev/collab-code-workspace',
    'https://collab.aaravsharma.dev',
    '["Implemented Conflict-Free Replicated Data Types (CRDTs) using Yjs over WebSockets for zero-conflict concurrent editing across 50+ simultaneous peers.", "Designed low-latency cursor tracking and diff synchronization with under 15ms broadcast latency.", "Packaged with Docker and deployed on AWS ECS with auto-scaling container tasks."]',
    '2023-02-01',
    '2023-06-30'
),
(
    4,
    'Automated CI/CD DevOps Pipeline & Security Scanner',
    'DevOps & Backend Engineer',
    'Cloud & DevOps',
    'Automated pipeline engine running static analysis, vulnerability checking (Trivy), and automated blue-green deployments.',
    'Python, GitHub Actions, Docker, Kubernetes, AWS EKS, Bash',
    'https://github.com/aaravsharma-dev/devops-security-pipeline',
    'https://pipeline-docs.aaravsharma.dev',
    '["Constructed fully automated CI/CD pipeline reducing release cycles from 45 minutes to 7 minutes.", "Integrated automated container scanning and SBOM generation, catching 100% of high-severity CVEs prior to production merge."]',
    '2024-06-01',
    '2024-09-15'
);

-- Work Experience / Internships
INSERT INTO experience (id, job_title, company, employment_type, location, start_date, end_date, is_current, description, highlights, tech_stack)
VALUES
(
    1,
    'Software Engineering Intern (Backend & Cloud)',
    'CloudScale Systems Pvt. Ltd.',
    'Internship',
    'Mumbai, India (Hybrid)',
    '2024-01-05',
    '2024-07-20',
    0,
    'Core backend engineering on microservices architecture serving 250,000+ monthly active users.',
    '["Architected and deployed 4 core RESTful microservices in Python (FastAPI) and PostgreSQL, handling 1.2M daily requests.", "Optimized slow database queries through strategic composite indexing and caching, slashing 95th percentile latency from 320ms to 45ms.", "Collaborated with DevOps team to configure Docker containerization and Kubernetes Helm charts for automated staging rollouts.", "Authored comprehensive unit and integration test suites achieving 89% code coverage in PyTest."]',
    'Python, FastAPI, PostgreSQL, Redis, Docker, Kubernetes, AWS, PyTest'
),
(
    2,
    'Full Stack Developer Intern',
    'InnoTech Digital Labs',
    'Internship',
    'Pune, India (Remote)',
    '2023-05-15',
    '2023-11-30',
    0,
    'Full-stack development for enterprise client dashboards and analytics reporting systems.',
    '["Developed dynamic interactive analytics dashboards using React.js, TypeScript, and Chart.js, increasing daily customer engagement by 28%.", "Engineered secure JWT-based role-based access control (RBAC) and OAuth2 authentication pipelines.", "Integrated external payment gateways (Stripe & Razorpay) with automated webhook idempotency handlers."]',
    'React.js, TypeScript, Node.js, Express, MongoDB, REST APIs'
);

-- Achievements
INSERT INTO achievements (id, title, issuer, issue_date, category, description)
VALUES
(
    1,
    '1st Prize Winner - National Smart India Hackathon',
    'Ministry of Education & AICTE',
    '2023-12-22',
    'Hackathon',
    'Won national championship among 2,500+ participating teams by building an AI-assisted disaster response logistics dispatcher in 36 hours.'
),
(
    2,
    'ACM ICPC Regional Contestant',
    'International Collegiate Programming Contest',
    '2023-10-14',
    'Academic',
    'Secured top 5% rank in regional collegiate competitive programming contest solving complex algorithmic graph and DP problems.'
),
(
    3,
    'Dean’s List of Academic Distinction',
    'University Academic Board',
    '2022-06-30',
    'Academic',
    'Awarded for maintaining top 1% academic percentile in the Computer Science department across consecutive semesters.'
);

-- Publications
INSERT INTO publications (id, title, publisher_or_journal, publication_date, authors, url, doi, abstract, keywords)
VALUES
(
    1,
    'A Resilient Architecture for Low-Latency Distributed Microservices Using Adaptive Caching and Predictive Prefetching',
    'IEEE International Conference on Advanced Computing & Communication (ICACC)',
    '2024-04-18',
    'Aarav Sharma, Dr. P. S. Khanvilkar, K. Mehta',
    'https://doi.org/10.1109/ICACC.2024.1049281',
    '10.1109/ICACC.2024.1049281',
    'This paper presents an adaptive multi-tier caching mechanism for cloud-native microservices that leverages lightweight predictive prefetching. Experimental evaluations demonstrate a 42% reduction in end-to-end p99 latency under fluctuating burst loads.',
    'Distributed Systems, Cloud Computing, Predictive Caching, Microservices, Latency Optimization'
);

-- Languages
INSERT INTO languages (language, proficiency) VALUES
('English', 'Full professional'),
('Hindi', 'Native or bilingual'),
('Marathi', 'Professional working'),
('German', 'Elementary');
