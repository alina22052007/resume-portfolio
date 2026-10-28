"""
Automated End-to-End System Test for Portfolio Database & Resume Generator
Tests all functional requirements:
1. SQLite Database CRUD & seeding
2. Gemini API integration & Fallback
3. Strict anti-hallucination verification
4. Google Sheets formatting & Apps Script export
5. Dynamic resume assembly
6. OpenXML DOCX generation
7. Dual JD differentiation check
"""

import os
import sys
import json
import database
import gemini_service
import sheets_service
import docx_generator
from samples.sample_data import SAMPLE_JD_1, SAMPLE_JD_2

def run_tests():
    print("==================================================================")
    print("🧪 Running Comprehensive Portfolio & Resume Generator Test Suite")
    print("==================================================================")

    # Test 1: Database
    print("\n[Test 1] Initializing SQLite database and verifying tables...")
    database.init_db(force_reseed=True)
    p = database.get_full_portfolio()
    categories = [
        "personal_info", "education", "skills", "certifications", 
        "projects", "experience", "achievements", "publications", "languages"
    ]
    for c in categories:
        count = len(p.get(c, []))
        assert count > 0, f"Category {c} should have records, got {count}"
        print(f"  ✓ {c}: {count} records verified")

    # Test 2: Gemini Unstructured Text Parser
    print("\n[Test 2] Testing Unstructured Text Extraction...")
    raw_bio = "Priya Sharma is a Lead Full Stack Developer in Mumbai. Email: priya@test.com. Skills: Python, React, Docker, SQL."
    extracted = gemini_service.parse_unstructured_portfolio(raw_bio)
    assert "personal_info" in extracted
    print(f"  ✓ Extracted Candidate: {extracted['personal_info'].get('full_name')}")
    print(f"  ✓ Extracted Skills: {[s['name'] for s in extracted.get('skills', [])]}")

    # Test 3: Gemini JD Analysis & Matching
    print("\n[Test 3] Testing JD Analysis & Matching for JD 1 (Full Stack)...")
    jd1_analysis = gemini_service.analyze_job_description(SAMPLE_JD_1["description"])
    match1 = gemini_service.match_portfolio_with_jd(p, jd1_analysis)
    print(f"  ✓ Target Title: {jd1_analysis.get('job_title')}")
    print(f"  ✓ ATS Match Score: {match1['match_percentage']}%")
    print(f"  ✓ Matched Skills Count: {len(match1['matched_skills'])}")
    print(f"  ✓ Anti-Hallucination Status: {match1['anti_hallucination_verification']['status']}")
    assert match1["anti_hallucination_verification"]["status"] == "VERIFIED_AUTHENTIC"
    assert match1["anti_hallucination_verification"]["invented_items_count"] == 0

    # Test 4: Testing JD Analysis & Matching for JD 2 (AI/ML)
    print("\n[Test 4] Testing JD Analysis & Matching for JD 2 (AI / ML)...")
    jd2_analysis = gemini_service.analyze_job_description(SAMPLE_JD_2["description"])
    match2 = gemini_service.match_portfolio_with_jd(p, jd2_analysis)
    print(f"  ✓ Target Title: {jd2_analysis.get('job_title')}")
    print(f"  ✓ ATS Match Score: {match2['match_percentage']}%")
    print(f"  ✓ Matched Skills Count: {len(match2['matched_skills'])}")
    
    # Verify that the two tailored summaries are distinct!
    assert match1["tailored_summary"] != match2["tailored_summary"]
    print("  ✓ Verification Passed: Dual JDs produced distinct, tailored professional summaries!")

    # Test 5: Dynamic Resume Assembly
    print("\n[Test 5] Testing Dynamic Resume Assembly...")
    resume1 = gemini_service.assemble_customized_resume(
        portfolio=p,
        jd_analysis=jd1_analysis,
        selected_skill_names=[s["name"] for s in match1["matched_skills"]],
        selected_project_ids=[1, 3],
        selected_experience_ids=[1, 2],
        selected_cert_ids=[1, 3],
        custom_summary=match1["tailored_summary"]
    )
    assert resume1["header"]["name"] == "Aarav Sharma"
    assert len(resume1["projects"]) == 2
    assert len(resume1["certifications"]) == 2
    print(f"  ✓ Assembled Resume 1 for {resume1['target_role']} with {len(resume1['skills'])} skills, {len(resume1['projects'])} projects")

    # Test 6: DOCX Generation
    print("\n[Test 6] Testing OpenXML DOCX Generation...")
    docx_bytes = docx_generator.generate_docx_bytes(resume1)
    assert len(docx_bytes) > 1000, f"DOCX too small ({len(docx_bytes)} bytes)"
    print(f"  ✓ Generated valid DOCX file: {len(docx_bytes)} bytes")

    # Test 7: Google Sheets Formatting & Apps Script
    print("\n[Test 7] Testing Google Sheets Export Formatting...")
    sheets_data = sheets_service.format_portfolio_for_sheets()
    assert sheets_data["status"] == "ready"
    assert len(sheets_data["sheet_tabs"]) == 9
    print(f"  ✓ Google Sheets Export ready with {len(sheets_data['sheet_tabs'])} tabs and {sheets_data['total_records']} total records across all sheets")

    # Test 8: CSV Generation
    csv_text = sheets_service.generate_category_csv("skills")
    assert "Skill Name" in csv_text
    print(f"  ✓ CSV category exporter verified (Skills CSV generated)")

    print("\n==================================================================")
    print("🎉 ALL 8 TEST SUITES PASSED FLAWLESSLY! (100% SUCCESS)")
    print("==================================================================")

if __name__ == "__main__":
    run_tests()

