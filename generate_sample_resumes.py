"""
Script to generate and export two customized resumes for the sample JDs
Produces:
1. samples/Resume_Aarav_Sharma_FullStack.docx
2. samples/Resume_Aarav_Sharma_FullStack.html
3. samples/Resume_Aarav_Sharma_AIML.docx
4. samples/Resume_Aarav_Sharma_AIML.html
5. samples/exported_portfolio_sheets.json
"""

import os
import json
import database
import gemini_service
import docx_generator
import sheets_service
from samples.sample_data import SAMPLE_JD_1, SAMPLE_JD_2

def build_html_resume(resume_data):
    h = resume_data.get("header", {})
    skills = resume_data.get("skills", [])
    grouped_skills = {}
    for s in skills:
        cat = s.get("category", "technical").capitalize()
        grouped_skills.setdefault(cat, []).append(s.get("name"))

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{h.get('name')} - {resume_data.get('target_role')}</title>
<style>
  body {{ font-family: "Georgia", serif; max-width: 820px; margin: 40px auto; padding: 20px; color: #111827; line-height: 1.5; }}
  .header {{ text-align: center; border-bottom: 2px solid #2563eb; padding-bottom: 12px; margin-bottom: 20px; }}
  .name {{ font-size: 28px; font-weight: bold; color: #1e3a8a; font-family: sans-serif; }}
  .title {{ font-size: 16px; font-weight: 600; color: #4b5563; margin-top: 4px; font-family: sans-serif; }}
  .contact {{ font-size: 13px; color: #6b7280; margin-top: 6px; font-family: sans-serif; }}
  .sec-title {{ font-size: 15px; font-weight: bold; color: #1e3a8a; text-transform: uppercase; border-bottom: 1px solid #93c5fd; padding-bottom: 4px; margin: 18px 0 8px 0; font-family: sans-serif; }}
  .item {{ margin-bottom: 12px; }}
  .item-head {{ display: flex; justify-content: space-between; font-weight: bold; font-family: sans-serif; font-size: 14px; }}
  .item-sub {{ color: #2563eb; font-size: 13px; font-family: sans-serif; font-weight: 600; }}
  ul {{ margin: 4px 0 0 20px; font-size: 13.5px; color: #374151; }}
  li {{ margin-bottom: 4px; }}
  .summary {{ font-size: 14px; text-align: justify; color: #374151; }}
  @media print {{ body {{ margin: 0; padding: 0; }} }}
</style>
</head>
<body>
  <div class="header">
    <div class="name">{h.get('name')}</div>
    <div class="title">{resume_data.get('target_role')}</div>
    <div class="contact">{h.get('email')} | {h.get('phone')} | {h.get('location')} | {h.get('linkedin')} | {h.get('github')}</div>
  </div>

  <div class="sec-title">Professional Summary</div>
  <div class="summary">{resume_data.get('summary')}</div>

  <div class="sec-title">Technical Competencies</div>
  <div style="font-size: 13.5px;">
"""
    for cat, items in grouped_skills.items():
        html += f"<div><strong>{cat}:</strong> {', '.join(items)}</div>"

    html += """</div><div class="sec-title">Work Experience</div>"""
    for exp in resume_data.get("experience", []):
        hl = exp.get("highlights", [])
        if isinstance(hl, str): hl = [hl]
        html += f"""
        <div class="item">
          <div class="item-head">
            <span>{exp.get('job_title')}</span>
            <span>{exp.get('start_date')} – {exp.get('end_date') or 'Present'}</span>
          </div>
          <div class="item-sub">{exp.get('company')} | {exp.get('location')}</div>
          <ul>{''.join([f"<li>{b}</li>" for b in hl])}</ul>
        </div>
        """

    html += """<div class="sec-title">Key Projects</div>"""
    for proj in resume_data.get("projects", []):
        hl = proj.get("highlights", [])
        if isinstance(hl, str): hl = [hl]
        html += f"""
        <div class="item">
          <div class="item-head">
            <span>{proj.get('title')}</span>
            <span>{proj.get('tech_stack')}</span>
          </div>
          <ul>{''.join([f"<li>{b}</li>" for b in hl])}</ul>
        </div>
        """

    html += """<div class="sec-title">Education</div>"""
    for edu in resume_data.get("education", []):
        html += f"""
        <div class="item">
          <div class="item-head">
            <span>{edu.get('degree')} in {edu.get('field_of_study')}</span>
            <span>{edu.get('start_year')} – {edu.get('end_year')}</span>
          </div>
          <div class="item-sub">{edu.get('institution')} | CGPA: {edu.get('grade_or_gpa')}</div>
        </div>
        """

    html += """<div class="sec-title">Certifications</div><ul>"""
    for c in resume_data.get("certifications", []):
        html += f"<li><strong>{c.get('title')}</strong> – {c.get('issuing_organization')} ({c.get('issue_date')})</li>"
    html += "</ul></body></html>"
    return html

def main():
    database.init_db()
    p = database.get_full_portfolio()
    samples_dir = os.path.join(os.path.dirname(__file__), "samples")
    os.makedirs(samples_dir, exist_ok=True)

    # 1. Customization for JD 1 (Full Stack)
    jd1_an = gemini_service.analyze_job_description(SAMPLE_JD_1["description"])
    m1 = gemini_service.match_portfolio_with_jd(p, jd1_an)
    resume1 = gemini_service.assemble_customized_resume(
        portfolio=p,
        jd_analysis=jd1_an,
        selected_skill_names=[s["name"] for s in m1["matched_skills"]],
        selected_project_ids=[1, 3],
        selected_experience_ids=[1, 2],
        selected_cert_ids=[1, 3],
        custom_summary=m1["tailored_summary"]
    )
    docx1 = docx_generator.generate_docx_bytes(resume1)
    with open(os.path.join(samples_dir, "Resume_Aarav_Sharma_FullStack.docx"), "wb") as f:
        f.write(docx1)
    with open(os.path.join(samples_dir, "Resume_Aarav_Sharma_FullStack.html"), "w", encoding="utf-8") as f:
        f.write(build_html_resume(resume1))

    # 2. Customization for JD 2 (AI/ML)
    jd2_an = gemini_service.analyze_job_description(SAMPLE_JD_2["description"])
    m2 = gemini_service.match_portfolio_with_jd(p, jd2_an)
    resume2 = gemini_service.assemble_customized_resume(
        portfolio=p,
        jd_analysis=jd2_an,
        selected_skill_names=[s["name"] for s in m2["matched_skills"]],
        selected_project_ids=[2, 1],
        selected_experience_ids=[1],
        selected_cert_ids=[2, 3],
        custom_summary=m2["tailored_summary"]
    )
    docx2 = docx_generator.generate_docx_bytes(resume2)
    with open(os.path.join(samples_dir, "Resume_Aarav_Sharma_AIML.docx"), "wb") as f:
        f.write(docx2)
    with open(os.path.join(samples_dir, "Resume_Aarav_Sharma_AIML.html"), "w", encoding="utf-8") as f:
        f.write(build_html_resume(resume2))

    # 3. Export Sheets JSON
    sheets_data = sheets_service.format_portfolio_for_sheets()
    with open(os.path.join(samples_dir, "exported_portfolio_sheets.json"), "w", encoding="utf-8") as f:
        json.dump(sheets_data, f, indent=2)

    print("Successfully pre-generated sample resumes and exports in samples/ directory!")

if __name__ == "__main__":
    main()

