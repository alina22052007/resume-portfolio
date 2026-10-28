"""
Native Pure-Python Microsoft Word (.docx) Document Generator
Constructs standard OpenXML .docx packages using Python standard library (zipfile, xml)
Zero third-party dependencies required. 100% compliant with MS Word, Google Docs, LibreOffice.
"""

import io
import zipfile
import xml.sax.saxutils as saxutils
from typing import Dict, List, Any

def escape(text: str) -> str:
    if not text:
        return ""
    return saxutils.escape(str(text))

def build_docx_xml(resume_data: Dict[str, Any]) -> str:
    header = resume_data.get("header", {})
    name = header.get("name", "Candidate Name")
    title = header.get("title", "Professional Title")
    email = header.get("email", "")
    phone = header.get("phone", "")
    location = header.get("location", "")
    linkedin = header.get("linkedin", "")
    github = header.get("github", "")
    summary = resume_data.get("summary", "")

    # Contact line
    contact_parts = [p for p in [email, phone, location, linkedin, github] if p]
    contact_str = " | ".join(contact_parts)

    body_xml = []

    # Title & Header
    body_xml.append(f"""
    <w:p>
      <w:pPr>
        <w:jc w:val="center"/>
        <w:spacing w:after="80"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
          <w:b/>
          <w:sz w:val="38"/>
          <w:color w:val="1E3A8A"/>
        </w:rPr>
        <w:t>{escape(name)}</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:pPr>
        <w:jc w:val="center"/>
        <w:spacing w:after="100"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
          <w:sz w:val="24"/>
          <w:color w:val="4B5563"/>
        </w:rPr>
        <w:t>{escape(title)}</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:pPr>
        <w:jc w:val="center"/>
        <w:spacing w:after="240"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
          <w:sz w:val="18"/>
          <w:color w:val="374151"/>
        </w:rPr>
        <w:t>{escape(contact_str)}</w:t>
      </w:r>
    </w:p>
    """)

    def add_section_heading(text: str):
        return f"""
        <w:p>
          <w:pPr>
            <w:spacing w:before="200" w:after="100"/>
            <w:pBdr>
              <w:bottom w:val="single" w:sz="8" w:space="4" w:color="2563EB"/>
            </w:pBdr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
              <w:b/>
              <w:sz w:val="24"/>
              <w:color w:val="1E3A8A"/>
            </w:rPr>
            <w:t>{escape(text.upper())}</w:t>
          </w:r>
        </w:p>
        """

    # Professional Summary
    if summary:
        body_xml.append(add_section_heading("Professional Summary"))
        body_xml.append(f"""
        <w:p>
          <w:pPr>
            <w:spacing w:after="160"/>
            <w:jc w:val="both"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
              <w:sz w:val="20"/>
            </w:rPr>
            <w:t>{escape(summary)}</w:t>
          </w:r>
        </w:p>
        """)

    # Technical Skills
    skills = resume_data.get("skills", [])
    if skills:
        body_xml.append(add_section_heading("Technical Competencies"))
        grouped = {}
        for s in skills:
            cat = s.get("category", "technical").capitalize()
            grouped.setdefault(cat, []).append(s.get("name", ""))
        
        for cat, items in grouped.items():
            body_xml.append(f"""
            <w:p>
              <w:pPr>
                <w:spacing w:after="80"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
                  <w:b/>
                  <w:sz w:val="20"/>
                  <w:color w:val="1F2937"/>
                </w:rPr>
                <w:t>{escape(cat)}: </w:t>
              </w:r>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
                  <w:sz w:val="20"/>
                </w:rPr>
                <w:t>{escape(", ".join(items))}</w:t>
              </w:r>
            </w:p>
            """)

    # Experience
    experience = resume_data.get("experience", [])
    if experience:
        body_xml.append(add_section_heading("Work Experience"))
        for exp in experience:
            title_line = f"{exp.get('job_title', '')} | {exp.get('company', '')}"
            date_line = f"{exp.get('start_date', '')} – {exp.get('end_date') or 'Present'} | {exp.get('location', '')}"
            body_xml.append(f"""
            <w:p>
              <w:pPr>
                <w:spacing w:before="120" w:after="40"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
                  <w:b/>
                  <w:sz w:val="22"/>
                  <w:color w:val="111827"/>
                </w:rPr>
                <w:t>{escape(title_line)}</w:t>
              </w:r>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
                  <w:i/>
                  <w:sz w:val="18"/>
                  <w:color w:val="6B7280"/>
                </w:rPr>
                <w:tab/>
                <w:t>{escape(date_line)}</w:t>
              </w:r>
            </w:p>
            """)
            
            # Bullets
            hl = exp.get("highlights", [])
            if isinstance(hl, str):
                hl = [h.strip() for h in hl.split("\n") if h.strip()]
            for bullet in hl:
                clean_b = bullet.lstrip("•-* ").strip()
                body_xml.append(f"""
                <w:p>
                  <w:pPr>
                    <w:ind w:left="360"/>
                    <w:spacing w:after="60"/>
                  </w:pPr>
                  <w:r>
                    <w:rPr>
                      <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
                      <w:sz w:val="20"/>
                    </w:rPr>
                    <w:t>• {escape(clean_b)}</w:t>
                  </w:r>
                </w:p>
                """)

    # Projects
    projects = resume_data.get("projects", [])
    if projects:
        body_xml.append(add_section_heading("Key Projects"))
        for p in projects:
            p_title = p.get("title", "")
            p_stack = p.get("tech_stack", "")
            body_xml.append(f"""
            <w:p>
              <w:pPr>
                <w:spacing w:before="120" w:after="40"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
                  <w:b/>
                  <w:sz w:val="22"/>
                  <w:color w:val="111827"/>
                </w:rPr>
                <w:t>{escape(p_title)}</w:t>
              </w:r>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
                  <w:i/>
                  <w:sz w:val="18"/>
                  <w:color w:val="2563EB"/>
                </w:rPr>
                <w:t> ({escape(p_stack)})</w:t>
              </w:r>
            </w:p>
            """)
            hl = p.get("highlights", [])
            if isinstance(hl, str):
                hl = [h.strip() for h in hl.split("\n") if h.strip()]
            for bullet in hl:
                clean_b = bullet.lstrip("•-* ").strip()
                body_xml.append(f"""
                <w:p>
                  <w:pPr>
                    <w:ind w:left="360"/>
                    <w:spacing w:after="60"/>
                  </w:pPr>
                  <w:r>
                    <w:rPr>
                      <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
                      <w:sz w:val="20"/>
                    </w:rPr>
                    <w:t>• {escape(clean_b)}</w:t>
                  </w:r>
                </w:p>
                """)

    # Education
    education = resume_data.get("education", [])
    if education:
        body_xml.append(add_section_heading("Education"))
        for edu in education:
            deg_line = f"{edu.get('degree', '')} in {edu.get('field_of_study', '')}"
            school_line = f"{edu.get('institution', '')} ({edu.get('start_year', '')} - {edu.get('end_year', '')}) | GPA: {edu.get('grade_or_gpa', '')}"
            body_xml.append(f"""
            <w:p>
              <w:pPr>
                <w:spacing w:before="100" w:after="40"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
                  <w:b/>
                  <w:sz w:val="20"/>
                </w:rPr>
                <w:t>{escape(deg_line)}</w:t>
              </w:r>
            </w:p>
            <w:p>
              <w:pPr>
                <w:spacing w:after="100"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
                  <w:sz w:val="18"/>
                  <w:color w:val="4B5563"/>
                </w:rPr>
                <w:t>{escape(school_line)}</w:t>
              </w:r>
            </w:p>
            """)

    # Certifications
    certs = resume_data.get("certifications", [])
    if certs:
        body_xml.append(add_section_heading("Certifications"))
        for c in certs:
            c_text = f"{c.get('title', '')} – {c.get('issuing_organization', '')} ({c.get('issue_date', '')})"
            body_xml.append(f"""
            <w:p>
              <w:pPr>
                <w:ind w:left="360"/>
                <w:spacing w:after="60"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
                  <w:sz w:val="20"/>
                </w:rPr>
                <w:t>• {escape(c_text)}</w:t>
              </w:r>
            </w:p>
            """)

    document_content = "".join(body_xml)

    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {document_content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""

def generate_docx_bytes(resume_data: Dict[str, Any]) -> bytes:
    """Creates a complete .docx file in memory and returns bytes."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        # [Content_Types].xml
        z.writestr("[Content_Types].xml", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>""")

        # _rels/.rels
        z.writestr("_rels/.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""")

        # word/document.xml
        z.writestr("word/document.xml", build_docx_xml(resume_data))

    return buf.getvalue()

if __name__ == "__main__":
    test_data = {
        "header": {"name": "Test User", "title": "Software Engineer", "email": "test@test.com"},
        "summary": "Experienced engineer.",
        "skills": [{"name": "Python", "category": "technical"}],
        "experience": [{"job_title": "Dev", "company": "Co", "highlights": ["Built stuff"]}],
        "education": [{"degree": "B.Tech", "institution": "Univ"}],
        "projects": [{"title": "Proj", "tech_stack": "Python"}],
        "certifications": [{"title": "AWS", "issuing_organization": "Amazon"}]
    }
    b = generate_docx_bytes(test_data)
    print(f"Generated docx bytes: {len(b)} bytes")

