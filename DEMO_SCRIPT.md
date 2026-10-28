# 🎬 Demonstration Video Script & Walkthrough Guide

## Assignment Details
- **Project**: AI-Powered Portfolio Database and Dynamic Resume Generator
- **Guide**: Prof. Poonam Suresh Khanvilkar (Assistant Professor - Computer Science, Kharghar)
- **Target Video Duration**: 3 – 5 Minutes

---

## 🕒 Timestamp Breakdown & Speaking Script

### 0:00 – 0:35 | Introduction & Objective
**Visual**: Show the PortfoliAI web application home screen at `http://localhost:5050` with the status pills glowing green.
> **Speaker Script**:  
> "Good day, Professor and evaluators. Today I am presenting my project: **AI-Powered Portfolio Database and Dynamic Resume Generator**.  
> The core problem this system solves is the disconnect between maintaining a comprehensive career portfolio and tailoring targeted, ATS-optimized resumes for specific job descriptions.  
> Instead of manually maintaining multiple Word files, our system acts as a centralized single source of truth backed by a normalized SQLite database, integrates the Google Gemini API for intelligent JD matching and anti-hallucination verification, syncs seamlessly with Google Sheets, and dynamically generates downloadable, ATS-compliant PDF and DOCX resumes in real time."

---

### 0:35 – 1:15 | Module 1: Portfolio Database & AI Importer
**Visual**: Click through the 9 category subtabs (Personal Info, Education, Skills, Experience, Projects, Certifications, Achievements, Publications, Languages). Click **Add New Record** to show the form modal, and then open the **AI Unstructured Importer**.
> **Speaker Script**:  
> "Let's begin in the **Portfolio Database Management** module. Here, all professional information is stored in a normalized relational schema across 9 dedicated categories.  
> We can view, edit, and add records with strict data validation.  
> Furthermore, we have built an **AI Unstructured Importer**. If a candidate has a raw LinkedIn bio or unformatted text, they can paste it here. The Gemini API analyzes the unstructured text, organizes it into structured fields like skills and experience, and allows the candidate to import them directly into the database with one click."

---

### 1:15 – 1:55 | Module 2: Google Sheets Two-Way Synchronization
**Visual**: Navigate to the **Google Sheets Sync** tab. Show the Apps Script code preview, click **View JSON Payload**, and show the one-click category CSV downloads.
> **Speaker Script**:  
> "Next is the **Google Sheets Synchronization** module. As required, Google Sheets serves as an accessible, collaborative spreadsheet view.  
> We have engineered a Google Apps Script Web App in `Code.gs` that automatically creates and formats 9 color-coded tabs corresponding to each database entity.  
> Updates made in the application can be pushed directly to Google Sheets using the webhook URL, or downloaded instantly using our pre-formatted CSV exports. Every sync operation is logged in our SQLite audit table."

---

### 1:55 – 2:45 | Module 3: Gemini Job Description & ATS Matcher
**Visual**: Switch to **JD & ATS Matcher**. Click **Sample JD 1: Full-Stack**, click **Analyze & Match with Portfolio (Gemini AI)**. Point out the ATS Match score gauge (94%), the green matched skills pills, the missing skills, the tailored suggestions, and the anti-hallucination badge.
> **Speaker Script**:  
> "Now let's examine the heart of the system: the **Gemini AI Matching Engine**.  
> When a candidate inputs a target job description—such as this Senior Full-Stack role—Gemini extracts the required competencies and compares them against our database records.  
> It computes an ATS Match Score—here 94%—and highlights matched skills like Python, FastAPI, and Docker versus missing skills.  
> Crucially, we enforce a **Strict Anti-Hallucination Guardrail**: the system verifies every skill and qualification against our SQLite database. It is mathematically impossible for the AI to fabricate non-existent degrees or credentials."

---

### 2:45 – 3:30 | Module 4: Dynamic Resume Studio & Export
**Visual**: Click **Customize & Generate Resume in Studio**. Show the left controls with checkboxes for skills and projects, and the right live resume paper updating dynamically in real time. Click **Download DOCX** (browser downloads .docx file) and **Download PDF** (print preview).
> **Speaker Script**:  
> "In the **Dynamic Resume Studio**, the candidate has full granular control. On the left, we can select or deselect specific projects, skills, or certifications.  
> The Gemini-generated professional summary is already tailored specifically for this role. Notice as I modify any selection, the live resume on the right regenerates instantaneously with ATS-compliant typography.  
> Finally, we can download the final resume with one click: as a standard Microsoft Word `.docx` document generated natively, or as a crisp, print-ready PDF."

---

### 3:30 – 4:00 | Conclusion & Dual JD Verification
**Visual**: Open the **Dual JD Comparison** tab showing the side-by-side comparison of the Full-Stack resume versus the AI/ML resume.
> **Speaker Script**:  
> "To conclude, in the **Dual JD Comparison** tab, you can see how the exact same portfolio for candidate Aarav Sharma generates two completely different, tailored resumes: one highlighting distributed backend systems and AWS, and the second highlighting applied PyTorch, Gemini multimodal healthcare models, and IEEE research publications.  
> The application is fully functional, zero-dependency, and ready for deployment. Thank you!"

---

## 📋 Tips for Recording
1. **Screen Resolution**: Set display to 1080p (1920x1080) for clear text.
2. **Recording Tool**: Use QuickTime Player on Mac (`Command + Shift + 5` -> Record Entire Screen) or OBS Studio.
3. **Local Server**: Run `python3 server.py` in your terminal and open `http://localhost:5050` in Chrome/Safari before recording.
4. **Duration**: Keep it between 3 to 4 minutes.

