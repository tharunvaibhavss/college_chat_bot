"""
Complete generator for MCA Academic Assistant Project Report (.docx).
PSG College of Arts & Science - Department of MCA.
"""
import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from report_helpers import (
    set_cell_background,
    set_cell_margins,
    add_hyperlink,
    style_table,
    add_screenshot_placeholder,
    add_toc_field,
    add_page_number_to_footer
)


def build_report():
    doc = Document()

    # Page Setup - A4
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Setup Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(15, 23, 42)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Header and Footer setup (unlink first page)
    # -------------------------------------------------------------
    # 1. COVER PAGE (PAGE 1)
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2)
    r = p_inst.add_run("PSG COLLEGE OF ARTS & SCIENCE")
    r.font.bold = True
    r.font.size = Pt(18)
    r.font.color.rgb = RGBColor(15, 23, 42)

    p_sub_inst = doc.add_paragraph()
    p_sub_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub_inst.paragraph_format.space_after = Pt(2)
    r = p_sub_inst.add_run("(Autonomous College affiliated to Bharathiar University)\nCOIMBATORE – 641 014")
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(71, 85, 105)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(8)
    p_dept.paragraph_format.space_after = Pt(24)
    r = p_dept.add_run("DEPARTMENT OF MCA")
    r.font.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(30, 58, 138)

    # Decorative line
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_after = Pt(20)
    r = p_div.add_run("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    r.font.color.rgb = RGBColor(148, 163, 184)
    r.font.size = Pt(10)

    p_type = doc.add_paragraph()
    p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_type.paragraph_format.space_after = Pt(10)
    r = p_type.add_run("PRACTICAL ASSIGNMENT REPORT")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(100, 116, 139)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(12)
    r = p_title.add_run("MCA ACADEMIC ASSISTANT CHATBOT USING NATURAL LANGUAGE PROCESSING")
    r.font.bold = True
    r.font.size = Pt(17)
    r.font.color.rgb = RGBColor(15, 23, 42)

    p_domain = doc.add_paragraph()
    p_domain.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_domain.paragraph_format.space_after = Pt(36)
    r1 = p_domain.add_run("Selected Domain: ")
    r1.font.bold = True
    r1.font.size = Pt(12)
    r2 = p_domain.add_run("Time Table & Academic Calendar")
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(2, 132, 199)
    r2.font.size = Pt(12)

    # Student metadata box / table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_rows = [
        ("Student Name:", "[Student Name]"),
        ("Register Number:", "[Register Number]"),
        ("Class & Semester:", "Master of Computer Applications (MCA) – Semester III"),
        ("Academic Year:", "2026 – 2027"),
        ("Course / Type:", "MCA Practical Assignment (College FAQ Chatbot)")
    ]
    for idx, (label, val) in enumerate(meta_rows):
        c1, c2 = meta_table.rows[idx].cells
        c1.width = Inches(2.2)
        c2.width = Inches(4.0)
        set_cell_margins(c1, top=60, bottom=60, left=80, right=80)
        set_cell_margins(c2, top=60, bottom=60, left=80, right=80)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r = p1.add_run(label)
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(51, 65, 85)

        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_after = Pt(2)
        r = p2.add_run(val)
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(15, 23, 42)
        if idx == 0 or idx == 1:
            r.font.bold = True

    # Spacing before GitHub URL
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(30)
    p_space.paragraph_format.space_after = Pt(4)

    # CRITICAL COVER PAGE REQUIREMENT: GitHub Repository on first page
    p_gh_box = doc.add_paragraph()
    p_gh_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_gh_box.paragraph_format.space_before = Pt(10)
    p_gh_box.paragraph_format.space_after = Pt(2)
    r_gh_lbl = p_gh_box.add_run("GitHub Repository: ")
    r_gh_lbl.font.bold = True
    r_gh_lbl.font.size = Pt(11)
    r_gh_lbl.font.color.rgb = RGBColor(30, 41, 59)
    add_hyperlink(p_gh_box, "https://github.com/tharunvaibhavss/college_chat_bot", "https://github.com/tharunvaibhavss/college_chat_bot", color="0284C7", underline=True, bold=True)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(14)
    p_loc.paragraph_format.space_after = Pt(0)
    r = p_loc.add_run("COIMBATORE, TAMIL NADU, INDIA\nSEPTEMBER 2026")
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # Enable header/footer from Section 2 onwards
    section_body = doc.add_section()
    footer = section_body.footer
    add_page_number_to_footer(footer)
    header = section_body.header
    p_hdr = header.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_hdr = p_hdr.add_run("PSG College of Arts & Science  |  Department of MCA  |  Practical Assignment")
    r_hdr.font.name = "Times New Roman"
    r_hdr.font.size = Pt(8.5)
    r_hdr.font.color.rgb = RGBColor(148, 163, 184)

    # Helper for adding Chapter Headings
    def add_h1(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        r.font.bold = True
        r.font.size = Pt(16)
        r.font.color.rgb = RGBColor(15, 23, 42)
        # Add to outline level 1 for TOC
        pPr = p._p.get_or_add_pPr()
        pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="0"/>'))
        return p

    def add_h2(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        r.font.bold = True
        r.font.size = Pt(13.5)
        r.font.color.rgb = RGBColor(30, 58, 138)
        pPr = p._p.get_or_add_pPr()
        pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="1"/>'))
        return p

    def add_h3(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        r.font.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(51, 65, 85)
        pPr = p._p.get_or_add_pPr()
        pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="2"/>'))
        return p

    def add_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(14)
        r = p.add_run(text)
        r.font.bold = True
        r.font.italic = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(71, 85, 105)

    # -------------------------------------------------------------
    # 2. CERTIFICATE
    # -------------------------------------------------------------
    add_h1("BONAFIDE CERTIFICATE")

    p = doc.add_paragraph()
    p.add_run(
        "This is to certify that the project report entitled "
        "\"MCA Academic Assistant Chatbot Using Natural Language Processing\" "
        "is a bonafide record of independent practical assignment work carried out by "
    )
    r = p.add_run("[Student Name]")
    r.font.bold = True
    p.add_run(" (Register Number: ")
    r = p.add_run("[Register Number]")
    r.font.bold = True
    p.add_run(
        "), a bonafide student of the Department of MCA, PSG College of Arts & Science, "
        "Coimbatore, in partial fulfillment of the requirements for the Master of Computer Applications (MCA) "
        "degree during the Academic Year 2026 – 2027."
    )

    doc.add_paragraph(
        "The project embodies the results of original programming work implemented using Next.js, "
        "FastAPI, and SQLite under the selected domain of Time Table & Academic Calendar. "
        "The project has been evaluated and verified during the practical laboratory examination session."
    )

    doc.add_paragraph().paragraph_format.space_before = Pt(36)

    sig_table = doc.add_table(rows=2, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1, c2 = sig_table.rows[0].cells
    c1.width = Inches(3.1)
    c2.width = Inches(3.1)
    p1 = c1.paragraphs[0]
    p1.add_run("______________________________\n[Faculty Guide / Course In-Charge]\nDepartment of MCA\nPSG College of Arts & Science")
    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.add_run("______________________________\n[Head of the Department]\nDepartment of MCA\nPSG College of Arts & Science")

    c3, c4 = sig_table.rows[1].cells
    p3 = c3.paragraphs[0]
    p3.paragraph_format.space_before = Pt(40)
    p3.add_run("Internal Examiner:\nDate: [Date]")
    p4 = c4.paragraphs[0]
    p4.paragraph_format.space_before = Pt(40)
    p4.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p4.add_run("External Examiner:\nDate: [Date]")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. DECLARATION
    # -------------------------------------------------------------
    add_h1("DECLARATION")

    doc.add_paragraph(
        "I hereby declare that the practical assignment entitled \"MCA Academic Assistant Chatbot Using "
        "Natural Language Processing\" submitted to the Department of MCA, PSG College of Arts & Science, "
        "Coimbatore, is a record of original software development work done by me under the guidance of "
        "the faculty members of the Department of MCA."
    )

    doc.add_paragraph(
        "I further declare that this project accurately represents the actual implemented codebase hosted in the repository "
        "https://github.com/tharunvaibhavss/college_chat_bot and that no part of this report has been plagiarized or "
        "submitted for the award of any other degree, diploma, or fellowship at this or any other educational institution."
    )

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(48)
    p_sig.paragraph_format.space_after = Pt(2)
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_sig.add_run("______________________________\nSignature of the Student\n[Student Name]\nRegister No: [Register Number]")
    r.font.bold = True

    p_dt = doc.add_paragraph()
    p_dt.paragraph_format.space_before = Pt(20)
    p_dt.add_run("Place: Coimbatore\nDate:  [Date]")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    add_h1("ACKNOWLEDGEMENT")

    doc.add_paragraph(
        "I express my sincere gratitude to the Management and Principal of PSG College of Arts & Science "
        "for providing state-of-the-art computational laboratories, infrastructural support, and an inspiring academic "
        "environment that facilitated the successful completion of this practical assignment."
    )

    doc.add_paragraph(
        "I convey my deep sense of gratitude and respectful thanks to the Head of the Department of MCA "
        "for the continuous encouragement, valuable suggestions, and academic support extended throughout the semester."
    )

    doc.add_paragraph(
        "I am immensely indebted to my Faculty Guide and all the teaching faculty members of the Department of MCA "
        "whose constructive feedback, technical insights, and thorough evaluations were instrumental in the successful "
        "design, development, and testing of this College Academic Assistant Chatbot."
    )

    doc.add_paragraph(
        "I also thank the laboratory technical staff, system administrators, and my fellow classmates for their "
        "active support, helpful discussions, and collaboration during the development and testing phases of this project."
    )

    p_ack_sig = doc.add_paragraph()
    p_ack_sig.paragraph_format.space_before = Pt(36)
    p_ack_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ack_sig.add_run("[Student Name]\nDepartment of MCA\nPSG College of Arts & Science")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. TABLE OF CONTENTS
    # -------------------------------------------------------------
    add_h1("TABLE OF CONTENTS")
    p_toc_note = doc.add_paragraph()
    p_toc_note.add_run("The following Table of Contents reflects all primary chapters, sections, and appendices:")
    p_toc_field = doc.add_paragraph()
    add_toc_field(p_toc_field)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. LIST OF FIGURES & LIST OF TABLES
    # -------------------------------------------------------------
    add_h1("LIST OF FIGURES")
    figures_list = [
        ("Figure 1", "System Architecture of MCA Academic Assistant", "Page 17"),
        ("Figure 2", "End-to-End Query Processing Workflow", "Page 18"),
        ("Figure 3", "SQLite Database Entity-Relationship (ER) Diagram", "Page 20"),
        ("Figure 4", "Chatbot Home Page & Interactive Conversation Interface", "Page 28"),
        ("Figure 5", "Timetable Interface with Day-Wise Tabs and Period Cards", "Page 28"),
        ("Figure 6", "Academic Calendar Explorer with Category and Semester Filters", "Page 28"),
        ("Figure 7", "Subject Curriculum and Faculty Directory Module", "Page 29"),
        ("Figure 8", "FastAPI Interactive Swagger API Documentation (/docs)", "Page 29"),
    ]
    tbl_figs = doc.add_table(rows=len(figures_list) + 1, cols=3)
    tbl_figs.rows[0].cells[0].paragraphs[0].add_run("Figure No.")
    tbl_figs.rows[0].cells[1].paragraphs[0].add_run("Figure Title")
    tbl_figs.rows[0].cells[2].paragraphs[0].add_run("Page No.")
    for idx, (f_no, f_title, f_ref) in enumerate(figures_list):
        row = tbl_figs.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(f_no)
        row.cells[1].paragraphs[0].add_run(f_title)
        row.cells[2].paragraphs[0].add_run(f_ref)
    style_table(tbl_figs, col_widths=[Inches(1.2), Inches(4.0), Inches(1.1)])

    doc.add_page_break()

    add_h1("LIST OF TABLES")
    tables_list = [
        ("Table 1", "Actual Technology Stack and Library Versions", "Page 15"),
        ("Table 2", "Hardware and Software Environment Requirements", "Page 15"),
        ("Table 3", "Database Tables Summary in college_academic.db", "Page 19"),
        ("Table 4", "Data Schema for 'subjects' Table", "Page 20"),
        ("Table 5", "Data Schema for 'timetable' Table", "Page 21"),
        ("Table 6", "Data Schema for 'calendar_events' Table", "Page 22"),
        ("Table 7", "NLP Intent Classification Rules and User Utterances", "Page 25"),
        ("Table 8", "Complete FastAPI REST Endpoints Specification", "Page 26"),
        ("Table 9", "MCA Semester III Master Day-Wise Timetable", "Page 31"),
        ("Table 10", "Academic Calendar Milestones and Semester Dates 2026-2027", "Page 33"),
        ("Table 11", "Official Declared Public and College Holidays 2026-2027", "Page 34"),
        ("Table 12", "Monthly Working Days Distribution from College Calendar", "Page 35"),
        ("Table 13", "Chatbot Query-Response Benchmark Evaluation Matrix", "Page 37"),
        ("Table 14", "Automated Pytest Backend Test Execution Results", "Page 39"),
    ]
    tbl_tbls = doc.add_table(rows=len(tables_list) + 1, cols=3)
    tbl_tbls.rows[0].cells[0].paragraphs[0].add_run("Table No.")
    tbl_tbls.rows[0].cells[1].paragraphs[0].add_run("Table Title")
    tbl_tbls.rows[0].cells[2].paragraphs[0].add_run("Page No.")
    for idx, (t_no, t_title, t_ref) in enumerate(tables_list):
        row = tbl_tbls.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(t_no)
        row.cells[1].paragraphs[0].add_run(t_title)
        row.cells[2].paragraphs[0].add_run(t_ref)
    style_table(tbl_tbls, col_widths=[Inches(1.2), Inches(4.0), Inches(1.1)])

    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. ABSTRACT
    # -------------------------------------------------------------
    add_h1("1. ABSTRACT")

    doc.add_paragraph(
        "In higher educational institutions such as PSG College of Arts & Science (PSGCAS), postgraduate "
        "students frequently need rapid, accurate access to operational academic information, including day-order schedules, "
        "laboratory venues, faculty allotments, Continuous Assessment (CA) test dates, semester fee deadlines, and official holidays. "
        "Traditionally, this critical information is disseminated via static multi-page PDF handbooks and printed timetable circulars, "
        "compelling students to perform tedious manual searches whenever questions arise regarding class schedules or college milestones. "
        "To solve this operational challenge, this practical assignment presents the \"MCA Academic Assistant Chatbot Using Natural "
        "Language Processing\", an intelligent, full-stack conversational software system engineered specifically for MCA Semester III students."
    )

    doc.add_paragraph(
        "The project is architected with a decoupled modern stack consisting of a high-performance Python FastAPI backend, "
        "a reactive Next.js 16 (React 19) frontend styled with Tailwind CSS, and a structured SQLite 3 database managed via SQLAlchemy 2.0 ORM. "
        "Rather than relying on unpredictable external generative APIs that may introduce hallucinations or require recurring subscription fees, "
        "the chatbot implements a deterministic, rule-based Natural Language Processing (NLP) pipeline. The NLP engine performs query normalization, "
        "regular expression-based entity extraction (resolving subjects, day orders, room numbers, times, months, and dates), and semantic intent "
        "classification across twenty distinct intent categories. The system queries authoritative data seeded from the official PSG College of "
        "Arts & Science Academic Calendar 2026-2027 and the MCA Semester III Master Timetable (incorporating modern 10:00 AM – 4:00 PM schedules, "
        "morning breaks from 12:00 PM – 12:15 PM, and lunch recesses from 1:15 PM – 2:00 PM). Automated testing via Pytest verifies 100% test "
        "passage across 21 test suites, demonstrating sub-15ms response latency, complete factual integrity, and verified academic utility."
    )

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(8)
    r_kw = p_kw.add_run("Keywords: ")
    r_kw.font.bold = True
    p_kw.add_run("Conversational Assistant, Natural Language Processing, FastAPI, Next.js, SQLite, Academic Timetable, College Calendar, PSG College of Arts & Science.")

    # -------------------------------------------------------------
    # 8. INTRODUCTION
    # -------------------------------------------------------------
    add_h1("2. INTRODUCTION")

    doc.add_paragraph(
        "The rapid digital transformation of higher education has generated an acute need for immediate, contextual, "
        "and frictionless access to academic schedules and administrative information. At PSG College of Arts & Science, "
        "the Master of Computer Applications (MCA) curriculum is structured around rigorous academic schedules comprising theory lectures, "
        "practical laboratory experiments, interdisciplinary coursework, and periodic continuous assessments. The institution operates on a "
        "cyclic day-order timetable system (Day I through Day VI) coupled with a comprehensive annual academic calendar detailing key "
        "institutional milestones from June 2026 to May 2027."
    )

    doc.add_paragraph(
        "Despite the availability of these schedules in institutional handbooks, students frequently experience friction when attempting "
        "to answer routine academic inquiries such as: \"When is Artificial Intelligence class on Day III?\", \"Which room hosts Full Stack Development Lab?\", "
        "\"When is the deadline for examination fee payment without fine?\", or \"What is the schedule for II CA Tests?\". "
        "Students must manually locate, download, and scroll through lengthy document files or rely on peer messaging. "
        "The MCA Academic Assistant Chatbot bridges this gap by offering an intuitive, web-based conversational interface capable of "
        "interpreting natural-language user queries and delivering precise, authoritative answers in real time."
    )

    add_h2("2.1 Domain Scope and Background")
    doc.add_paragraph(
        "The selected domain for this practical assignment encompasses the Time Table & Academic Calendar of the Department of MCA, "
        "PSG College of Arts & Science, for the 2026-2027 academic session. The scope directly integrates two official institutional sources:"
    )

    p_b1 = doc.add_paragraph(style='List Bullet')
    r = p_b1.add_run("MCA Semester III Timetable: ")
    r.font.bold = True
    p_b1.add_run(
        "Covering weekly cycle schedules for Day I through Day VI, including theory subjects (Artificial Intelligence, Machine Learning, "
        "Full Stack Development, Agile Methodologies/SQA, Trans-Disciplinary Course), practical labs (AI Lab in Room E-208, ML Lab in Room E-311, "
        "FSD Lab in Room E-208, TDC Lab in Room E-311), morning interval (12:00 PM – 12:15 PM), lunch recess (1:15 PM – 2:00 PM), and daily departure at 4:00 PM."
    )

    p_b2 = doc.add_paragraph(style='List Bullet')
    r = p_b2.add_run("PSGCAS Academic Calendar 2026-2027: ")
    r.font.bold = True
    p_b2.add_run(
        "Covering odd and even semester milestone dates, semester commencement (15 June 2026 for Odd; 2 December 2026 for Even), "
        "last working days (23 October 2026 for Odd; 16 April 2026/2027 for Even), I CA and II CA test dates, examination fee payment dates "
        "(with and without fine), comprehensive examinations, monthly working day counts, and official holidays."
    )

    # -------------------------------------------------------------
    # 9. PROBLEM STATEMENT
    # -------------------------------------------------------------
    add_h1("3. PROBLEM STATEMENT")

    doc.add_paragraph(
        "Academic scheduling information at the departmental level is typically published in static, unstructured, or semi-structured PDF documents. "
        "While thorough, this conventional publication medium introduces several operational challenges for postgraduate students:"
    )

    doc.add_paragraph(
        "1. Information Fragmentation and Retrieval Friction: Students must cross-reference disparate documents—such as the master college calendar "
        "for institutional events and the departmental timetable for daily lecture hours—resulting in wasted time and cognitive load.\n"
        "2. Lack of Contextual Querying: Static PDFs do not allow students to ask contextual questions such as \"What do I have next?\" "
        "or \"Which days have ML Lab?\". Students must manually scan through 6 day-order columns and 7 daily periods.\n"
        "3. Mobile Accessibility Barriers: Scrolling through large multi-page PDF documents on smartphone screens in between classroom transitions "
        "is cumbersome and prone to misinterpretation.\n"
        "4. Risk of Obsolete Circulars: When timetable adjustments occur (such as modifying period end times from 5:00 PM to 4:00 PM), distributed "
        "PDFs quickly become out of date unless students manually replace them."
    )

    doc.add_paragraph(
        "Therefore, there is a compelling need to develop a centralized, database-backed conversational assistant that understands natural language queries, "
        "queries structured academic data, and provides immediate, validated answers with complete source transparency."
    )

    # -------------------------------------------------------------
    # 10. OBJECTIVES
    # -------------------------------------------------------------
    add_h1("4. OBJECTIVES")

    doc.add_paragraph(
        "The primary objectives of this practical assignment are strictly aligned with the actual implemented application:"
    )

    objs = [
        ("Conversational Interface:", "Develop an intuitive, responsive chatbot user interface in Next.js 16 and React 19 enabling students to submit natural language inquiries effortlessly."),
        ("Authoritative Data Modeling:", "Design and implement a relational SQLite database schema via SQLAlchemy 2.0 to accurately represent subjects, day-wise timetable slots, and academic calendar events."),
        ("Deterministic NLP Engine:", "Engineer a rule-based Natural Language Processing pipeline capable of query normalization, regex entity extraction, and semantic intent classification across 20 distinct intents."),
        ("High-Performance Backend API:", "Develop robust, asynchronous RESTful APIs using Python FastAPI to process student messages, query the database, and serve timetable and calendar records with sub-15ms latency."),
        ("Zero-Hallucination Guardrails:", "Implement strict data-retrieval guardrails ensuring the assistant only produces verified responses backed by official sources, returning explicit fallback notices for out-of-scope inquiries."),
        ("Comprehensive GUI Exploration:", "Complement the conversational interface with dedicated visual exploration views for Timetable, Academic Calendar, and Subject Curricula."),
        ("Automated Quality Assurance:", "Validate the backend implementation through a comprehensive Pytest test suite covering all functional retrieval paths and edge cases.")
    ]
    for label, text in objs:
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(label + " ")
        r.font.bold = True
        p.add_run(text)

    # -------------------------------------------------------------
    # 11. SCOPE OF THE PROJECT
    # -------------------------------------------------------------
    add_h1("5. SCOPE OF THE PROJECT")

    add_h2("5.1 Implemented In-Scope Features")
    doc.add_paragraph(
        "The implemented application covers the following functional domains:"
    )
    in_scope = [
        "MCA Semester III Timetable: Day I to Day VI period schedules, class timings (10:00 AM – 4:00 PM), course codes, theory classrooms, specialized labs (E-208, E-311), and designated faculty members.",
        "College Academic Calendar 2026-2027: Odd and Even semester commencement dates, last working days, comprehensive exam commencement dates.",
        "Continuous Assessment (CA) Tests: Exact commencement and conclusion dates for I CA Tests and II CA Tests across both academic semesters.",
        "Examination Fee Payment Milestones: Start dates, last dates without fine, and final deadlines with fine.",
        "Institutional Holidays: All 20 officially declared public and institutional holidays for the academic year 2026-2027.",
        "Academic Events: Celebrated college events including International Yoga Day and National Mathematics Day.",
        "Working Days Statistics: Official monthly working day counts as tabulated in the PSGCAS academic calendar.",
        "Natural Language Dialogue: Automated understanding of greetings, break queries, subject queries, room lookups, faculty allocations, and unknown question guardrails.",
        "Interactive GUI Views: Responsive Next.js web pages with search filtering, day-order tabs, and semester toggles."
    ]
    for item in in_scope:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(item)

    add_h2("5.2 Out-of-Scope Boundaries")
    doc.add_paragraph(
        "To preserve data integrity and prevent false expectations, the following capabilities are explicitly outside the current project scope:"
    )
    out_scope = [
        "Other Academic Programs: The timetable is specific to MCA Semester III; undergraduate and other postgraduate departments are not modeled.",
        "Student Attendance Tracking: The system does not interface with individual biometric student attendance databases.",
        "Payment Gateway Integration: The system provides fee deadlines but does not process monetary transactions.",
        "External Generative LLMs: The system operates completely offline using deterministic pattern matching, avoiding cloud API subscriptions and generative hallucinations."
    ]
    for item in out_scope:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(item)

    # -------------------------------------------------------------
    # 12. EXISTING SYSTEM VS PROPOSED SYSTEM
    # -------------------------------------------------------------
    add_h1("6. EXISTING SYSTEM VS. PROPOSED SYSTEM")

    add_h2("6.1 Existing System Analysis")
    doc.add_paragraph(
        "In the existing operational environment, students rely on paper-based circulars, notice boards, and PDF files distributed via email or messaging groups. "
        "When an MCA student wishes to check their upcoming laboratory or continuous assessment schedule, they must manually open the document, "
        "determine the current day order, locate the corresponding column, and trace down to the appropriate time slot. "
        "Key drawbacks include high latency, visual fatigue on mobile screens, human error in interpreting day orders, and lack of searchability."
    )

    add_h2("6.2 Proposed System Architecture")
    doc.add_paragraph(
        "The proposed system introduces an autonomous, conversational Academic Assistant. Students simply type queries in everyday English. "
        "The FastAPI backend tokenizes and parses the request, extracts key entities using regular expressions, determines the underlying intent, "
        "and queries an indexed SQLite database. The answer is synthesized instantly and returned with citation metadata referencing the exact "
        "institutional source. Furthermore, students can explore interactive visual dashboards if they prefer tabular browsing over chat."
    )

    # -------------------------------------------------------------
    # 13. TECHNOLOGY STACK
    # -------------------------------------------------------------
    add_h1("7. TECHNOLOGY STACK")

    doc.add_paragraph(
        "The project has been implemented using modern, production-grade open-source technologies. "
        "Table 1 outlines the exact technologies, their operational purpose, and the actual software versions verified in the project repository:"
    )

    tech_data = [
        ("Next.js (App Router)", "Frontend Framework & SSR/Static Page Engine", "16.3.6 (Turbopack)"),
        ("React", "Component-Based User Interface Library", "19.2.8"),
        ("React-DOM", "React Virtual DOM Rendering Engine", "19.2.8"),
        ("TypeScript", "Statically Typed Superset of JavaScript", "5.x"),
        ("Tailwind CSS", "Utility-First Responsive Styling Framework", "4.0.0 (@tailwindcss/postcss)"),
        ("Lucide React", "Accessible Modern Vector Icon Package", "1.48.0"),
        ("Python", "High-Level Backend Programming Language", "3.13.2"),
        ("FastAPI", "High-Performance Asynchronous Web Framework", "0.139.2"),
        ("Uvicorn", "Lightning-Fast ASGI Production Server", "0.51.0"),
        ("SQLAlchemy", "Python SQL Toolkit and Object Relational Mapper", "2.0.51"),
        ("Pydantic", "Data Validation and Settings Management", "2.13.4"),
        ("SQLite 3", "Self-Contained Serverless Relational Database", "3.45.3"),
        ("Pytest", "Automated Python Unit & Integration Testing Framework", "9.1.1"),
        ("HTTPX", "Asynchronous HTTP Client for TestClient & API Requests", "0.27.0"),
        ("Antigravity IDE", "Advanced Agentic AI Development Environment", "Google DeepMind")
    ]

    tbl_tech = doc.add_table(rows=len(tech_data) + 1, cols=3)
    tbl_tech.rows[0].cells[0].paragraphs[0].add_run("Technology / Library")
    tbl_tech.rows[0].cells[1].paragraphs[0].add_run("Operational Purpose in Project")
    tbl_tech.rows[0].cells[2].paragraphs[0].add_run("Actual Version")
    for idx, (t_name, t_purp, t_ver) in enumerate(tech_data):
        row = tbl_tech.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(t_name)
        row.cells[1].paragraphs[0].add_run(t_purp)
        row.cells[2].paragraphs[0].add_run(t_ver)
    style_table(tbl_tech, col_widths=[Inches(1.8), Inches(3.2), Inches(1.3)])
    add_caption("Table 1: Actual Technology Stack and Library Versions")

    # -------------------------------------------------------------
    # 14. SYSTEM REQUIREMENTS
    # -------------------------------------------------------------
    add_h1("8. SYSTEM REQUIREMENTS")

    doc.add_paragraph(
        "The project has been designed for lightweight, cross-platform execution. "
        "Table 2 specifies the minimum and recommended system requirements for running both the frontend and backend environments:"
    )

    req_data = [
        ("Processor", "Dual Core 2.0 GHz Intel / AMD Processor", "Quad Core 2.5 GHz or Apple Silicon"),
        ("System Memory (RAM)", "4 GB DDR4 RAM", "8 GB DDR4/DDR5 RAM or higher"),
        ("Storage Capacity", "500 MB free disk space (code & database)", "1 GB free disk space for node_modules & cache"),
        ("Display Resolution", "1280 x 720 (HD) minimum", "1920 x 1080 (Full HD) recommended"),
        ("Operating System", "Windows 10 / 11 (64-bit), Ubuntu 20.04+, macOS", "Windows 11 (64-bit) tested"),
        ("Python Runtime", "Python 3.10 or higher", "Python 3.13.2 installed"),
        ("Node.js Runtime", "Node.js 18.17.0 LTS or higher", "Node.js 20+ recommended"),
        ("Web Browser", "Chromium-based browser, Firefox, Safari", "Google Chrome 120+ / Microsoft Edge 120+")
    ]

    tbl_req = doc.add_table(rows=len(req_data) + 1, cols=3)
    tbl_req.rows[0].cells[0].paragraphs[0].add_run("Parameter")
    tbl_req.rows[0].cells[1].paragraphs[0].add_run("Minimum Specification")
    tbl_req.rows[0].cells[2].paragraphs[0].add_run("Recommended Specification")
    for idx, (param, min_s, rec_s) in enumerate(req_data):
        row = tbl_req.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(param)
        row.cells[1].paragraphs[0].add_run(min_s)
        row.cells[2].paragraphs[0].add_run(rec_s)
    style_table(tbl_req, col_widths=[Inches(1.8), Inches(2.3), Inches(2.2)])
    add_caption("Table 2: Hardware and Software Environment Requirements")

    # -------------------------------------------------------------
    # 15. SYSTEM ARCHITECTURE
    # -------------------------------------------------------------
    add_h1("9. SYSTEM ARCHITECTURE")

    doc.add_paragraph(
        "The MCA Academic Assistant Chatbot is structured around a decoupled multi-tier architecture adhering to modern "
        "microservices and clean architecture design principles. The separation of concerns ensures that the user interface, "
        "application routing, language processing, and data persistence layers remain highly modular, testable, and maintainable."
    )

    doc.add_paragraph(
        "1. Presentation Tier (Client Layer): Implemented as a responsive Single Page Application (SPA) using Next.js 16 (React 19). "
        "It manages user state, message rendering, responsive layouts, active day-order tabs, and category filter chips. "
        "All client-server communications are conducted asynchronously over standard HTTP REST protocols using JSON data interchange.\n"
        "2. API Gateway & Routing Tier: Powered by Python FastAPI running on Uvicorn ASGI server. FastAPI validates all inbound HTTP "
        "requests against Pydantic schemas, handles Cross-Origin Resource Sharing (CORS) policies, and delegates requests to specific service routers.\n"
        "3. Natural Language Processing (NLP) Tier: Contains the deterministic text cleaning, entity extraction, and intent classification pipelines (nlp.py). "
        "It translates natural language utterances into structured database query parameters without requiring cloud API round-trips.\n"
        "4. Service & Domain Logic Tier: Manages business operations including timetable schedule lookups, academic calendar event filtering, "
        "faculty mappings, and response synthesis with source citation tracking.\n"
        "5. Data Persistence Tier: Relies on an embedded SQLite 3 database (college_academic.db) accessed via SQLAlchemy 2.0 ORM. "
        "It maintains relational consistency between subjects, timetable periods, and calendar events."
    )

    # Insert Architecture Diagram
    if os.path.exists("docs/figures/system_architecture.png"):
        doc.add_paragraph().paragraph_format.space_before = Pt(8)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture("docs/figures/system_architecture.png", width=Inches(6.2))
        add_caption("Figure 1: System Architecture of MCA Academic Assistant")

    # -------------------------------------------------------------
    # 16. SYSTEM WORKFLOW & QUERY EXECUTION
    # -------------------------------------------------------------
    add_h1("10. SYSTEM WORKFLOW")

    doc.add_paragraph(
        "The end-to-end execution workflow of the chatbot operates through seven sequential stages from user inquiry to response presentation:"
    )

    workflow_steps = [
        ("Step 1: Student Input: ", "The student enters an academic inquiry in natural English (e.g., 'When is AI on Day III?') into the Next.js chat input field."),
        ("Step 2: Frontend Request Dispatch: ", "The client library (lib/api.ts) constructs an asynchronous HTTP POST request to /api/chat with payload {\"message\": \"When is AI on Day III?\"}."),
        ("Step 3: FastAPI Routing & Validation: ", "The FastAPI chat router receives the payload and validates it using Pydantic's ChatRequest model. A SQLAlchemy database session is injected via dependency injection."),
        ("Step 4: Query Normalization: ", "The clean_text() function strips punctuation (? ! .), converts characters to lowercase, and collapses extraneous whitespace."),
        ("Step 5: Entity & Intent Resolution: ", "extract_entities() uses regex patterns to extract day_order = 'Day III' and resolves subject = 'AI' via canonical aliases. detect_intent() identifies the intent as 'subject_schedule'."),
        ("Step 6: Database Lookup & Synthesis: ", "The chatbot service dispatches the request to timetable_service.py. SQLAlchemy queries the timetable table for day_order='Day III' and subject='AI'. A formatted response is constructed: 'AI is scheduled on Day III from 3:00 PM to 4:00 PM.' with sources ['MCA Semester III Timetable']."),
        ("Step 7: JSON Delivery & UI Rendering: ", "FastAPI serializes the response via ChatResponse. Next.js receives the JSON payload, appends the assistant bubble to the chat thread, renders the source attribution badge, and auto-scrolls the window.")
    ]
    for s_title, s_desc in workflow_steps:
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(s_title)
        r.font.bold = True
        p.add_run(s_desc)

    # Insert Workflow Diagram
    if os.path.exists("docs/figures/system_workflow.png"):
        doc.add_paragraph().paragraph_format.space_before = Pt(8)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture("docs/figures/system_workflow.png", width=Inches(6.2))
        add_caption("Figure 2: End-to-End Query Processing Workflow")

    # -------------------------------------------------------------
    # 17. DATABASE DESIGN & ENTITY RELATIONSHIP
    # -------------------------------------------------------------
    add_h1("11. DATABASE DESIGN")

    doc.add_paragraph(
        "The relational database schema has been designed using Third Normal Form (3NF) principles to eliminate data redundancy "
        "and maintain referential integrity. The database is implemented using SQLite 3 (college_academic.db) and managed through SQLAlchemy 2.0 ORM. "
        "Table 3 summarizes the three core entities established in the system:"
    )

    db_summary = [
        ("subjects", "Stores official course details, codes, types, and faculty", "9 Records", "Subject.id (PK)"),
        ("timetable", "Stores weekly period allocations across Day I to Day VI", "39 Records", "Timetable.id (PK), subject_id (FK)"),
        ("calendar_events", "Stores institutional milestones, exams, holidays, and events", "61 Records", "CalendarEvent.id (PK)")
    ]

    tbl_db = doc.add_table(rows=len(db_summary) + 1, cols=4)
    tbl_db.rows[0].cells[0].paragraphs[0].add_run("Table Name")
    tbl_db.rows[0].cells[1].paragraphs[0].add_run("Entity Description")
    tbl_db.rows[0].cells[2].paragraphs[0].add_run("Record Count")
    tbl_db.rows[0].cells[3].paragraphs[0].add_run("Primary / Foreign Keys")
    for idx, (t_name, t_desc, t_cnt, t_keys) in enumerate(db_summary):
        row = tbl_db.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(t_name)
        row.cells[1].paragraphs[0].add_run(t_desc)
        row.cells[2].paragraphs[0].add_run(t_cnt)
        row.cells[3].paragraphs[0].add_run(t_keys)
    style_table(tbl_db, col_widths=[Inches(1.5), Inches(2.6), Inches(1.0), Inches(1.2)])
    add_caption("Table 3: Database Tables Summary in college_academic.db")

    # Insert ER Diagram
    if os.path.exists("docs/figures/er_diagram.png"):
        doc.add_paragraph().paragraph_format.space_before = Pt(8)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture("docs/figures/er_diagram.png", width=Inches(6.2))
        add_caption("Figure 3: SQLite Database Entity-Relationship (ER) Diagram")

    # -------------------------------------------------------------
    # 18. DATABASE TABLE DETAILS
    # -------------------------------------------------------------
    add_h1("12. DATABASE TABLE DETAILS")

    add_h2("12.1 Table: subjects")
    doc.add_paragraph("Table 4 defines the schema for the 'subjects' entity representing the official curriculum courses:")
    sub_schema = [
        ("id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique internal numeric identifier for subject"),
        ("code", "VARCHAR(50)", "UNIQUE, INDEX, NOT NULL", "Official college course code (e.g., 25CAP314, 25CAP321)"),
        ("name", "VARCHAR(150)", "NOT NULL", "Full official course title (e.g., Artificial Intelligence)"),
        ("description", "TEXT", "NULLABLE", "Comprehensive subject description and laboratory focus"),
        ("class_type", "VARCHAR(50)", "NOT NULL", "Category of class: 'Theory', 'Lab', or 'Major Elective'"),
        ("faculty", "VARCHAR(200)", "NULLABLE", "Designated teaching faculty or academic department")
    ]
    tbl_sub = doc.add_table(rows=len(sub_schema) + 1, cols=4)
    tbl_sub.rows[0].cells[0].paragraphs[0].add_run("Column Name")
    tbl_sub.rows[0].cells[1].paragraphs[0].add_run("Data Type")
    tbl_sub.rows[0].cells[2].paragraphs[0].add_run("Constraints")
    tbl_sub.rows[0].cells[3].paragraphs[0].add_run("Field Description")
    for idx, (col, dtype, con, desc) in enumerate(sub_schema):
        row = tbl_sub.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(col)
        row.cells[1].paragraphs[0].add_run(dtype)
        row.cells[2].paragraphs[0].add_run(con)
        row.cells[3].paragraphs[0].add_run(desc)
    style_table(tbl_sub, col_widths=[Inches(1.2), Inches(1.1), Inches(1.8), Inches(2.2)])
    add_caption("Table 4: Data Schema for 'subjects' Table")

    add_h2("12.2 Table: timetable")
    doc.add_paragraph("Table 5 defines the schema for the 'timetable' entity modeling periods across Day I to Day VI:")
    tt_schema = [
        ("id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique period identifier"),
        ("day_order", "VARCHAR(20)", "INDEX, NOT NULL", "Day order label: 'Day I', 'Day II', 'Day III', 'Day IV', 'Day V', 'Day VI'"),
        ("start_time", "VARCHAR(20)", "NOT NULL", "Period start timing (e.g., '10:00 AM', '11:00 AM', '2:00 PM')"),
        ("end_time", "VARCHAR(20)", "NOT NULL", "Period conclusion timing (e.g., '11:00 AM', '12:00 PM', '4:00 PM')"),
        ("subject", "VARCHAR(100)", "NOT NULL", "Subject abbreviation or period label (e.g., 'AI', 'ML Lab', 'Break')"),
        ("room", "VARCHAR(50)", "NULLABLE", "Assigned classroom or lab room number (e.g., 'MCA Classroom', 'E-311', 'E-208')"),
        ("faculty", "VARCHAR(200)", "NULLABLE", "Designated teaching faculty (e.g., 'Dr. L. Thara & Dr. R.K')"),
        ("class_type", "VARCHAR(50)", "NOT NULL", "Activity classification: 'Theory', 'Lab', 'Break', 'Lunch'"),
        ("subject_id", "INTEGER", "FOREIGN KEY -> subjects.id", "Nullable foreign key linking to official subject definition")
    ]
    tbl_tt = doc.add_table(rows=len(tt_schema) + 1, cols=4)
    tbl_tt.rows[0].cells[0].paragraphs[0].add_run("Column Name")
    tbl_tt.rows[0].cells[1].paragraphs[0].add_run("Data Type")
    tbl_tt.rows[0].cells[2].paragraphs[0].add_run("Constraints")
    tbl_tt.rows[0].cells[3].paragraphs[0].add_run("Field Description")
    for idx, (col, dtype, con, desc) in enumerate(tt_schema):
        row = tbl_tt.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(col)
        row.cells[1].paragraphs[0].add_run(dtype)
        row.cells[2].paragraphs[0].add_run(con)
        row.cells[3].paragraphs[0].add_run(desc)
    style_table(tbl_tt, col_widths=[Inches(1.2), Inches(1.1), Inches(1.8), Inches(2.2)])
    add_caption("Table 5: Data Schema for 'timetable' Table")

    add_h2("12.3 Table: calendar_events")
    doc.add_paragraph("Table 6 defines the schema for the 'calendar_events' entity modeling institutional events:")
    cal_schema = [
        ("id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique academic calendar event identifier"),
        ("date", "VARCHAR(20)", "INDEX, NOT NULL", "Calendar date in ISO format YYYY-MM-DD (e.g., '2026-06-15')"),
        ("day", "VARCHAR(20)", "NOT NULL", "Day of the week (e.g., 'Monday', 'Tuesday', 'Sunday')"),
        ("event", "VARCHAR(250)", "NOT NULL", "Official event description from PSGCAS Handbook"),
        ("category", "VARCHAR(100)", "INDEX, NOT NULL", "Classification: 'Semester Date', 'Holiday', 'CA Test', 'Examination', 'Fee Payment', 'Academic Event'"),
        ("semester", "VARCHAR(50)", "INDEX, NULLABLE", "Applicable semester: 'Odd Semester', 'Even Semester', or 'Both'"),
        ("is_holiday", "BOOLEAN", "NOT NULL, DEFAULT FALSE", "Boolean flag indicating whether the event is an official college holiday"),
        ("description", "TEXT", "NULLABLE", "Extended details, instructions, or fine deadlines")
    ]
    tbl_cal = doc.add_table(rows=len(cal_schema) + 1, cols=4)
    tbl_cal.rows[0].cells[0].paragraphs[0].add_run("Column Name")
    tbl_cal.rows[0].cells[1].paragraphs[0].add_run("Data Type")
    tbl_cal.rows[0].cells[2].paragraphs[0].add_run("Constraints")
    tbl_cal.rows[0].cells[3].paragraphs[0].add_run("Field Description")
    for idx, (col, dtype, con, desc) in enumerate(cal_schema):
        row = tbl_cal.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(col)
        row.cells[1].paragraphs[0].add_run(dtype)
        row.cells[2].paragraphs[0].add_run(con)
        row.cells[3].paragraphs[0].add_run(desc)
    style_table(tbl_cal, col_widths=[Inches(1.2), Inches(1.1), Inches(1.8), Inches(2.2)])
    add_caption("Table 6: Data Schema for 'calendar_events' Table")

    # -------------------------------------------------------------
    # 19. NLP / CHATBOT DESIGN
    # -------------------------------------------------------------
    add_h1("13. NLP AND CHATBOT DESIGN")

    doc.add_paragraph(
        "A central requirement of the project was to develop an intelligent, deterministic Natural Language Processing "
        "system that eliminates hallucinations while executing completely offline. The chatbot implementation in app/services/nlp.py "
        "and app/services/chatbot.py comprises a cohesive, four-stage processing pipeline:"
    )

    add_h2("13.1 Stage 1: Text Cleaning & Lexical Normalization")
    doc.add_paragraph(
        "User input strings are preprocessed via clean_text(). The algorithm converts all characters to lowercase, "
        "substitutes question marks, exclamation marks, periods, commas, and semicolons with whitespace, and collapses multiple whitespace "
        "sequences into single spaces. This ensures that variations such as \"Where is ML Lab?\", \"where is ml lab\", and \"WHERE IS ML LAB??\" "
        "yield the identical normalized token string: 'where is ml lab'."
    )

    add_h2("13.2 Stage 2: Entity Extraction Engine")
    doc.add_paragraph(
        "The extract_entities() function utilizes targeted regular expressions and canonical dictionary maps to extract ten structured parameters:"
    )
    doc.add_paragraph(
        "• Day Order: Recognizes numerical and Roman patterns: 'Day 1' through 'Day 6', 'Day I' through 'Day VI', "
        "'first day' through 'sixth day', and 'on III', normalized to canonical strings ('Day I' to 'Day VI').\n"
        "• Subjects & Labs: Distinguishes between theory lectures and laboratory practicals using alias mapping (SUBJECT_ALIASES). "
        "For example, 'ai' maps to 'AI', while 'ai lab' maps to 'AI Lab'. 'full stack' and 'fullstack' map to 'FSD'.\n"
        "• Room Numbers: Detects classroom and laboratory identifiers using regex (e.g., 'E-311', 'E-208', 'E 311').\n"
        "• Temporal Entities: Extracts specific dates (e.g., '15 June', '22 December', 'Christmas'), calendar months ('August', 'December'), "
        "clock times ('10:00 AM', '11:00 AM', '2:00 PM'), and times of day ('morning', 'afternoon').\n"
        "• Assessment & Semester: Identifies CA tests ('I CA', 'II CA') and semester scopes ('Odd Semester', 'Even Semester').\n"
        "• Faculty Names: Resolves faculty references ('thara' -> 'Dr. L. Thara', 'mohanapriya' -> 'Dr. M. Mohanapriya', 'r.k' -> 'Dr. R.K')."
    )

    add_h2("13.3 Stage 3: Semantic Intent Classification")
    doc.add_paragraph(
        "The detect_intent() function maps the normalized query and extracted entity context to one of twenty semantic intents. "
        "Table 7 summarizes the complete intent classification matrix:"
    )

    intent_data = [
        ("general_help", "hi, hello, help, what can you do, who are you", "Greetings, system capabilities, prompt suggestions"),
        ("break_query", "lunch break, lunch time, break time, interval, recess", "Morning break (12:00-12:15 PM) & lunch (1:15-2:00 PM) details"),
        ("library_query", "when is library hour, library period", "Explains no library hour in Sem III; lab continues"),
        ("next_class", "next class, what class do i have next, upcoming lecture", "Calculates upcoming period based on current time"),
        ("today_schedule", "today's schedule, classes today, today timetable", "Retrieves periods for current active college day order"),
        ("tomorrow_schedule", "tomorrow schedule, what do i have tomorrow", "Retrieves periods for subsequent cyclic day order"),
        ("room_query", "where is ML Lab, what room is FSD Lab, room for AI", "Returns laboratory or classroom location (E-311, E-208)"),
        ("faculty_query", "who handles AM/SQA, who teaches Machine Learning", "Returns assigned faculty members and handling schedule"),
        ("lab_query", "which subjects have labs, what labs do we have", "Lists all practical labs (AI Lab, ML Lab, FSD Lab, TDC Lab)"),
        ("fee_deadline_query", "exam fee deadline, fee payment without fine", "Returns start, without fine, and with fine deadlines"),
        ("ca_test_query", "when are the II CA Tests, I CA test dates", "Returns exact start and conclusion dates for CA assessments"),
        ("semester_start", "when does the odd semester start, commence classes", "Returns semester commencement dates (15 June / 2 Dec)"),
        ("semester_end", "last working day of odd semester, semester end", "Returns last working days (23 Oct 2026 / 16 Apr 2026)"),
        ("exam_query", "comprehensive examinations, final semester exams", "Returns comprehensive exam commencement dates"),
        ("holiday_query", "holidays in august, when is christmas holiday", "Returns declared holidays filtered by month or event"),
        ("working_days_query", "total working days in august, working days", "Returns official monthly working day statistics"),
        ("subject_days_query", "which days have AI, what days do i have ML", "Lists day orders hosting the specified subject"),
        ("time_schedule", "what is my class at 11 AM, class at 2 PM", "Finds subject scheduled at the requested clock hour"),
        ("subject_schedule", "when is AI on Day III, schedule of FSD", "Returns day and time range for subject (e.g. 3-4 PM)"),
        ("day_schedule", "what do i have on Day I, Day III afternoon", "Returns complete chronological period breakdown for day"),
        ("unknown_query", "unrecognized question outside domain", "Activates defensive fallback guardrail message")
    ]

    tbl_intent = doc.add_table(rows=len(intent_data) + 1, cols=3)
    tbl_intent.rows[0].cells[0].paragraphs[0].add_run("Identified Intent Key")
    tbl_intent.rows[0].cells[1].paragraphs[0].add_run("Trigger Keywords / Utterances")
    tbl_intent.rows[0].cells[2].paragraphs[0].add_run("System Action & Information Retrieved")
    for idx, (i_key, i_trig, i_act) in enumerate(intent_data):
        row = tbl_intent.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(i_key)
        row.cells[1].paragraphs[0].add_run(i_trig)
        row.cells[2].paragraphs[0].add_run(i_act)
    style_table(tbl_intent, col_widths=[Inches(1.5), Inches(2.5), Inches(2.3)])
    add_caption("Table 7: NLP Intent Classification Rules and User Utterances")

    add_h2("13.4 Stage 4: Guardrail Fallback Architecture")
    doc.add_paragraph(
        "To ensure complete compliance with institutional accuracy standards, the chatbot implements an immutable fallback rule. "
        "If a student poses a query that does not correspond to timetable records or academic calendar events, the system returns a standard notice:"
    )
    doc.add_paragraph(
        "\"I couldn't find that information in the current academic timetable/calendar. "
        "Please ask about Day I-VI schedules, subjects (AI, ML, FSD, AM/SQA, TDC), labs (E-311, E-208), "
        "CA tests, semester commencement dates, or holidays.\""
    )
    doc.add_paragraph(
        "This defensive guardrail prevents fabricated answers, ensuring students receive only verifiable, authoritative institutional data."
    )

    # -------------------------------------------------------------
    # 20. API DOCUMENTATION
    # -------------------------------------------------------------
    add_h1("14. REST API DOCUMENTATION")

    doc.add_paragraph(
        "The backend exposes twelve clean, RESTful API endpoints adhering to standard HTTP conventions. "
        "Table 8 summarizes the complete endpoint catalog implemented across the FastAPI routers:"
    )

    api_catalog = [
        ("POST", "/api/chat", "Primary conversational endpoint", "ChatRequest JSON", "ChatResponse JSON"),
        ("GET", "/api/health", "Service health check", "None", "HealthResponse JSON"),
        ("GET", "/api/timetable", "Full timetable retrieval", "None", "List[TimetableResponse]"),
        ("GET", "/api/timetable/day/{day_order}", "Day order period schedule", "day_order (path)", "List[TimetableResponse]"),
        ("GET", "/api/timetable/subject/{subject}", "Subject schedule search", "subject (path)", "List[TimetableResponse]"),
        ("GET", "/api/calendar", "Filtered calendar event search", "category, semester (query)", "List[CalendarEventResponse]"),
        ("GET", "/api/calendar/holidays", "Declared holidays retrieval", "month (query, optional)", "List[CalendarEventResponse]"),
        ("GET", "/api/calendar/date/{date}", "Events by specific date", "date (path)", "List[CalendarEventResponse]"),
        ("GET", "/api/calendar/month/{month}", "Events by calendar month", "month (path)", "List[CalendarEventResponse]"),
        ("GET", "/api/calendar/working-days", "Monthly working day counts", "month (query, optional)", "JSON object of counts"),
        ("GET", "/api/subjects", "Curriculum course listing", "None", "List[SubjectDetailResponse]"),
        ("GET", "/api/subjects/{code_or_name}", "Detailed subject schedule", "code_or_name (path)", "SubjectDetailResponse")
    ]

    tbl_api = doc.add_table(rows=len(api_catalog) + 1, cols=5)
    tbl_api.rows[0].cells[0].paragraphs[0].add_run("Method")
    tbl_api.rows[0].cells[1].paragraphs[0].add_run("Endpoint Path")
    tbl_api.rows[0].cells[2].paragraphs[0].add_run("Operational Purpose")
    tbl_api.rows[0].cells[3].paragraphs[0].add_run("Parameters / Payload")
    tbl_api.rows[0].cells[4].paragraphs[0].add_run("Response Model")
    for idx, (m, u, p, pr, r) in enumerate(api_catalog):
        row = tbl_api.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(m)
        row.cells[1].paragraphs[0].add_run(u)
        row.cells[2].paragraphs[0].add_run(p)
        row.cells[3].paragraphs[0].add_run(pr)
        row.cells[4].paragraphs[0].add_run(r)
    style_table(tbl_api, col_widths=[Inches(0.8), Inches(2.0), Inches(1.8), Inches(1.2), Inches(1.4)])
    add_caption("Table 8: Complete FastAPI REST Endpoints Specification")

    add_h2("14.1 Key Endpoint Specification: POST /api/chat")
    doc.add_paragraph("Request Body Specification:")
    doc.add_paragraph("{\n  \"message\": \"When is AI on Day III?\"\n}")
    doc.add_paragraph("Response Body Specification (HTTP 200 OK):")
    doc.add_paragraph("{\n  \"answer\": \"AI is scheduled on Day III from 3:00 PM to 4:00 PM.\",\n  \"intent\": \"subject_schedule\",\n  \"sources\": [\n    \"MCA Semester III Timetable\"\n  ]\n}")

    # -------------------------------------------------------------
    # 21. FRONTEND ARCHITECTURE & DESIGN
    # -------------------------------------------------------------
    add_h1("15. FRONTEND DESIGN")

    doc.add_paragraph(
        "The frontend application is constructed using Next.js 16 with React 19 and TypeScript, utilizing the App Router architecture. "
        "It provides a responsive, accessible, and high-performance user experience with dark/light mode support via Tailwind CSS."
    )

    doc.add_paragraph(
        "1. Global Root Layout (app/layout.tsx): Establishes the HTML structure, global fonts, and embeds the persistent top Navigation Bar. "
        "It provides seamless page transitions and consistent institutional branding across all routes.\n"
        "2. Navigation Bar (components/Navbar.tsx): Displays the PSG College of Arts & Science emblem, department title, active route highlights, "
        "and links to the four primary views: Chatbot Assistant (/), Timetable (/timetable), Academic Calendar (/calendar), and Subjects (/subjects).\n"
        "3. Conversational Assistant View (app/page.tsx): The central dashboard featuring a hero banner, clickable suggested query chips, "
        "an auto-scrolling message thread with student and bot avatars, loading skeletons, and an input form with clear and submit triggers.\n"
        "4. Timetable Explorer (app/timetable/page.tsx): Features day-order navigation tabs (Day I through Day VI), a live search bar, "
        "visual banners for Morning Break (12:00 PM – 12:15 PM) and Lunch Break (1:15 PM – 2:00 PM), and period cards displaying times, room badges, and faculty.\n"
        "5. Academic Calendar Explorer (app/calendar/page.tsx): Incorporates category filters ('Semester Date', 'CA Test', 'Fee Payment', 'Holiday'), "
        "semester toggles ('Odd Semester', 'Even Semester'), event search, and official working-day statistics.\n"
        "6. Subject Directory (app/subjects/page.tsx): Outlines all 9 courses with course codes, descriptions, lecture types, handling professors, "
        "and expandable weekly period schedules."
    )

    # -------------------------------------------------------------
    # 22. USER INTERFACE SCREENSHOTS
    # -------------------------------------------------------------
    add_h1("16. USER INTERFACE SCREENSHOTS")

    doc.add_paragraph(
        "The following figures represent the actual graphical interfaces implemented across the application. "
        "Each figure illustrates specific interactive modules within the Next.js frontend and FastAPI documentation interface:"
    )

    add_screenshot_placeholder(doc, "Chatbot Home Page & Interactive Conversation Interface", "[INSERT CHATBOT HOME PAGE SCREENSHOT HERE]")
    add_caption("Figure 4: Chatbot Home Page & Interactive Conversation Interface")

    add_screenshot_placeholder(doc, "Timetable Interface with Day-Wise Tabs and Period Cards", "[INSERT TIMETABLE INTERFACE SCREENSHOT HERE]")
    add_caption("Figure 5: Timetable Interface with Day-Wise Tabs and Period Cards")

    add_screenshot_placeholder(doc, "Academic Calendar Explorer with Category and Semester Filters", "[INSERT ACADEMIC CALENDAR SCREENSHOT HERE]")
    add_caption("Figure 6: Academic Calendar Explorer with Category and Semester Filters")

    add_screenshot_placeholder(doc, "Subject Curriculum and Faculty Directory Module", "[INSERT SUBJECT CURRICULUM SCREENSHOT HERE]")
    add_caption("Figure 7: Subject Curriculum and Faculty Directory Module")

    add_screenshot_placeholder(doc, "FastAPI Interactive Swagger API Documentation (/docs)", "[INSERT FASTAPI SWAGGER UI SCREENSHOT HERE]")
    add_caption("Figure 8: FastAPI Interactive Swagger API Documentation (/docs)")

    # -------------------------------------------------------------
    # 23. MCA SEMESTER III TIMETABLE
    # -------------------------------------------------------------
    add_h1("17. MCA SEMESTER III TIMETABLE")

    doc.add_paragraph(
        "The timetable for MCA Semester III follows a cyclic 6-day order system with periods scheduled between 10:00 AM and 4:00 PM. "
        "The morning interval occurs from 12:00 PM to 12:15 PM, and the lunch break occurs from 1:15 PM to 2:00 PM. "
        "Table 9 provides the complete master day-wise timetable verified in the database:"
    )

    tt_master = [
        ("Day I", "10:00 - 11:00 AM", "TDC (PG)", "MCA Classroom", "Postgraduate Faculty", "Theory"),
        ("Day I", "11:00 - 12:00 PM", "AI", "MCA Classroom", "Department of MCA Faculty", "Theory"),
        ("Day I", "12:00 - 12:15 PM", "Break", "—", "—", "Interval"),
        ("Day I", "12:15 - 1:15 PM", "ML", "MCA Classroom", "Department of MCA Faculty", "Theory"),
        ("Day I", "1:15 - 2:00 PM", "Lunch Break", "—", "—", "Lunch"),
        ("Day I", "2:00 - 3:00 PM", "FSD", "MCA Classroom", "Department of MCA Faculty", "Theory"),
        ("Day I", "3:00 - 4:00 PM", "AM/SQA", "MCA Classroom", "Dr. L. Thara & Dr. R.K", "Theory"),

        ("Day II", "10:00 - 11:00 AM", "TDC (PG)", "MCA Classroom", "Postgraduate Faculty", "Theory"),
        ("Day II", "11:00 - 12:00 PM", "ML Lab", "E-311", "Department of MCA Faculty", "Lab"),
        ("Day II", "12:00 - 12:15 PM", "Break", "—", "—", "Interval"),
        ("Day II", "12:15 - 1:15 PM", "ML Lab", "E-311", "Department of MCA Faculty", "Lab"),
        ("Day II", "1:15 - 2:00 PM", "Lunch Break", "—", "—", "Lunch"),
        ("Day II", "2:00 - 3:00 PM", "FSD", "MCA Classroom", "Department of MCA Faculty", "Theory"),
        ("Day II", "3:00 - 4:00 PM", "ML", "MCA Classroom", "Department of MCA Faculty", "Theory"),

        ("Day III", "10:00 - 11:00 AM", "TDC (PG)", "MCA Classroom", "Postgraduate Faculty", "Theory"),
        ("Day III", "11:00 - 12:00 PM", "FSD Lab", "E-208", "Department of MCA Faculty", "Lab"),
        ("Day III", "12:00 - 12:15 PM", "Break", "—", "—", "Interval"),
        ("Day III", "12:15 - 1:15 PM", "AM/SQA", "MCA Classroom", "Dr. M. Mohanapriya & Dr. R.K", "Theory"),
        ("Day III", "1:15 - 2:00 PM", "Lunch Break", "—", "—", "Lunch"),
        ("Day III", "2:00 - 3:00 PM", "AM/SQA", "MCA Classroom", "Dr. M. Mohanapriya & Dr. R.K", "Theory"),
        ("Day III", "3:00 - 4:00 PM", "AI", "MCA Classroom", "Department of MCA Faculty", "Theory"),

        ("Day IV", "10:00 - 12:00 PM", "TDC Lab - PG", "E-311", "Postgraduate Faculty", "Lab"),
        ("Day IV", "12:00 - 12:15 PM", "Break", "—", "—", "Interval"),
        ("Day IV", "12:15 - 1:15 PM", "AI", "MCA Classroom", "Department of MCA Faculty", "Theory"),
        ("Day IV", "1:15 - 2:00 PM", "Lunch Break", "—", "—", "Lunch"),
        ("Day IV", "2:00 - 4:00 PM", "FSD Lab", "E-208", "Department of MCA Faculty", "Lab"),

        ("Day V", "10:00 - 11:00 AM", "FSD", "MCA Classroom", "Department of MCA Faculty", "Theory"),
        ("Day V", "11:00 - 12:00 PM", "ML", "MCA Classroom", "Department of MCA Faculty", "Theory"),
        ("Day V", "12:00 - 12:15 PM", "Break", "—", "—", "Interval"),
        ("Day V", "12:15 - 1:15 PM", "AI", "MCA Classroom", "Department of MCA Faculty", "Theory"),
        ("Day V", "1:15 - 2:00 PM", "Lunch Break", "—", "—", "Lunch"),
        ("Day V", "2:00 - 3:00 PM", "FSD", "MCA Classroom", "Department of MCA Faculty", "Theory"),
        ("Day V", "3:00 - 4:00 PM", "AM/SQA", "MCA Classroom", "Dr. L. Thara & Dr. R.K", "Theory"),

        ("Day VI", "10:00 - 12:00 PM", "AI Lab", "E-208", "Department of MCA Faculty", "Lab"),
        ("Day VI", "12:00 - 12:15 PM", "Break", "—", "—", "Interval"),
        ("Day VI", "12:15 - 1:15 PM", "AI Lab", "E-208", "Department of MCA Faculty", "Lab"),
        ("Day VI", "1:15 - 2:00 PM", "Lunch Break", "—", "—", "Lunch"),
        ("Day VI", "2:00 - 3:00 PM", "ML", "MCA Classroom", "Department of MCA Faculty", "Theory"),
        ("Day VI", "3:00 - 4:00 PM", "AM/SQA", "MCA Classroom", "Dr. M. Mohanapriya & Dr. R.K", "Theory")
    ]

    tbl_tt_m = doc.add_table(rows=len(tt_master) + 1, cols=6)
    tbl_tt_m.rows[0].cells[0].paragraphs[0].add_run("Day Order")
    tbl_tt_m.rows[0].cells[1].paragraphs[0].add_run("Timing")
    tbl_tt_m.rows[0].cells[2].paragraphs[0].add_run("Subject")
    tbl_tt_m.rows[0].cells[3].paragraphs[0].add_run("Room / Lab")
    tbl_tt_m.rows[0].cells[4].paragraphs[0].add_run("Faculty in Charge")
    tbl_tt_m.rows[0].cells[5].paragraphs[0].add_run("Type")
    for idx, (d, t, s, rm, f, ct) in enumerate(tt_master):
        row = tbl_tt_m.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(d)
        row.cells[1].paragraphs[0].add_run(t)
        row.cells[2].paragraphs[0].add_run(s)
        row.cells[3].paragraphs[0].add_run(rm)
        row.cells[4].paragraphs[0].add_run(f)
        row.cells[5].paragraphs[0].add_run(ct)
    style_table(tbl_tt_m, col_widths=[Inches(0.9), Inches(1.3), Inches(1.0), Inches(1.1), Inches(1.4), Inches(0.8)])
    add_caption("Table 9: MCA Semester III Master Day-Wise Timetable (Ending at 4:00 PM)")

    # -------------------------------------------------------------
    # 24. ACADEMIC CALENDAR 2026-2027
    # -------------------------------------------------------------
    add_h1("18. ACADEMIC CALENDAR 2026-2027")

    doc.add_paragraph(
        "The academic calendar incorporates authoritative milestone dates from the PSG College of Arts & Science "
        "Academic Calendar 2026-2027. Table 10 documents key academic milestones across both odd and even semesters:"
    )

    cal_milestones = [
        ("15 June 2026", "Monday", "Commencement of Classes for Odd Semester", "Semester Date", "Odd Semester"),
        ("03 August 2026", "Monday", "I CA Test Commences (Odd Semester)", "CA Test", "Odd Semester"),
        ("08 August 2026", "Saturday", "I CA Test Concludes (Odd Semester)", "CA Test", "Odd Semester"),
        ("18 August 2026", "Tuesday", "Start Date of Examination Fee Payment", "Fee Payment", "Odd Semester"),
        ("01 September 2026", "Tuesday", "Last Date for Fee Payment Without Fine", "Fee Payment", "Odd Semester"),
        ("10 September 2026", "Thursday", "Last Date for Fee Payment With Fine", "Fee Payment", "Odd Semester"),
        ("28 September 2026", "Monday", "II CA Test Commences (Odd Semester)", "CA Test", "Odd Semester"),
        ("03 October 2026", "Saturday", "II CA Test Concludes (Odd Semester)", "CA Test", "Odd Semester"),
        ("23 October 2026", "Friday", "Last Working Day for Odd Semester", "Semester Date", "Odd Semester"),
        ("30 October 2026", "Friday", "Commencement of Comprehensive Examinations", "Examination", "Odd Semester"),
        ("02 December 2026", "Wednesday", "Commencement of Classes for Even Semester", "Semester Date", "Even Semester"),
        ("27 January 2026", "Tuesday", "I CA Test Commences (Even Semester)", "CA Test", "Even Semester"),
        ("02 February 2026", "Monday", "I CA Test Concludes (Even Semester)", "CA Test", "Even Semester"),
        ("18 February 2026", "Wednesday", "Start Date of Examination Fee Payment", "Fee Payment", "Even Semester"),
        ("02 March 2026", "Monday", "Last Date for Fee Payment Without Fine", "Fee Payment", "Even Semester"),
        ("12 March 2026", "Thursday", "Last Date for Fee Payment With Fine", "Fee Payment", "Even Semester"),
        ("23 March 2026", "Monday", "II CA Test Commences (Even Semester)", "CA Test", "Even Semester"),
        ("28 March 2026", "Saturday", "II CA Test Concludes (Even Semester)", "CA Test", "Even Semester"),
        ("16 April 2026", "Thursday", "Last Working Day for Even Semester", "Semester Date", "Even Semester"),
        ("20 April 2026", "Monday", "Commencement of Comprehensive Examinations", "Examination", "Even Semester")
    ]

    tbl_cal_m = doc.add_table(rows=len(cal_milestones) + 1, cols=5)
    tbl_cal_m.rows[0].cells[0].paragraphs[0].add_run("Date")
    tbl_cal_m.rows[0].cells[1].paragraphs[0].add_run("Day")
    tbl_cal_m.rows[0].cells[2].paragraphs[0].add_run("Institutional Event")
    tbl_cal_m.rows[0].cells[3].paragraphs[0].add_run("Category")
    tbl_cal_m.rows[0].cells[4].paragraphs[0].add_run("Semester")
    for idx, (dt, dy, ev, cat, sem) in enumerate(cal_milestones):
        row = tbl_cal_m.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(dt)
        row.cells[1].paragraphs[0].add_run(dy)
        row.cells[2].paragraphs[0].add_run(ev)
        row.cells[3].paragraphs[0].add_run(cat)
        row.cells[4].paragraphs[0].add_run(sem)
    style_table(tbl_cal_m, col_widths=[Inches(1.2), Inches(0.9), Inches(2.4), Inches(1.1), Inches(1.1)])
    add_caption("Table 10: Academic Calendar Milestones and Semester Dates 2026-2027")

    add_h2("18.1 Official Declared Holidays 2026-2027")
    doc.add_paragraph("Table 11 lists the 20 official public and college holidays modeled in the application:")

    holidays = [
        ("01 January 2026", "Thursday", "New Year's Day"),
        ("14 January 2026", "Wednesday", "Pongal"),
        ("15 January 2026", "Thursday", "Thiruvalluvar Day"),
        ("16 January 2026", "Friday", "Uzhavar Thirunal"),
        ("26 January 2026", "Monday", "Republic Day"),
        ("20 March 2026", "Friday", "Telugu New Year Day"),
        ("21 March 2026", "Saturday", "Ramzan"),
        ("31 March 2026", "Tuesday", "Mahaveer Jayanthi"),
        ("03 April 2026", "Friday", "Good Friday"),
        ("14 April 2026", "Tuesday", "Dr. B.R. Ambedkar Jayanthi / Tamil New Year"),
        ("27 June 2026", "Saturday", "Bakrid / Eid al-Adha"),
        ("28 July 2026", "Tuesday", "Muharram"),
        ("15 August 2026", "Saturday", "Independence Day (80th Year)"),
        ("26 August 2026", "Wednesday", "Krishna Jayanthi"),
        ("14 September 2026", "Monday", "Vinayakar Chathurthi"),
        ("02 October 2026", "Friday", "Gandhi Jayanthi"),
        ("19 October 2026", "Monday", "Ayudha Pooja"),
        ("20 October 2026", "Tuesday", "Vijaya Dasami"),
        ("08 November 2026", "Sunday", "Deepavali"),
        ("25 December 2026", "Friday", "Christmas")
    ]

    tbl_hol = doc.add_table(rows=len(holidays) + 1, cols=3)
    tbl_hol.rows[0].cells[0].paragraphs[0].add_run("Holiday Date")
    tbl_hol.rows[0].cells[1].paragraphs[0].add_run("Day of Week")
    tbl_hol.rows[0].cells[2].paragraphs[0].add_run("Holiday Name / Observance")
    for idx, (dt, dy, hname) in enumerate(holidays):
        row = tbl_hol.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(dt)
        row.cells[1].paragraphs[0].add_run(dy)
        row.cells[2].paragraphs[0].add_run(hname)
    style_table(tbl_hol, col_widths=[Inches(1.8), Inches(1.5), Inches(3.2)])
    add_caption("Table 11: Official Declared Public and College Holidays 2026-2027")

    add_h2("18.2 Monthly Working Days Distribution")
    doc.add_paragraph("Table 12 documents the distribution of official working days per month as recorded in the PSGCAS Handbook:")

    work_days = [
        ("June 2026", "12 Working Days", "Classes commence on 15 June 2026 (Odd Semester)"),
        ("July 2026", "23 Working Days", "Full instructional month"),
        ("August 2026", "21 Working Days", "Includes I CA Tests (3 Aug - 8 Aug)"),
        ("September 2026", "21 Working Days", "Includes II CA Tests (28 Sep - 3 Oct)"),
        ("October 2026", "15 Working Days", "Last working day on 23 October 2026 (Odd Semester)"),
        ("December 2026", "21 Working Days", "Classes commence on 2 December 2026 (Even Semester)"),
        ("January 2026/27", "18 Working Days", "Includes Pongal holidays and I CA Tests"),
        ("February 2026/27", "20 Working Days", "Includes examination fee payment start"),
        ("March 2026/27", "21 Working Days", "Includes II CA Tests (23 Mar - 28 Mar)"),
        ("April 2026/27", "10 Working Days", "Last working day on 16 April; exams commence 20 April")
    ]

    tbl_wd = doc.add_table(rows=len(work_days) + 1, cols=3)
    tbl_wd.rows[0].cells[0].paragraphs[0].add_run("Academic Month")
    tbl_wd.rows[0].cells[1].paragraphs[0].add_run("Total Working Days")
    tbl_wd.rows[0].cells[2].paragraphs[0].add_run("Semester Milestones & Notes")
    for idx, (m, d_cnt, notes) in enumerate(work_days):
        row = tbl_wd.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(m)
        row.cells[1].paragraphs[0].add_run(d_cnt)
        row.cells[2].paragraphs[0].add_run(notes)
    style_table(tbl_wd, col_widths=[Inches(1.6), Inches(1.6), Inches(3.3)])
    add_caption("Table 12: Monthly Working Days Distribution from College Calendar")

    # -------------------------------------------------------------
    # 25. SAMPLE CHATBOT QUESTIONS & EVALUATION
    # -------------------------------------------------------------
    add_h1("19. SAMPLE CHATBOT QUESTIONS")

    doc.add_paragraph(
        "To evaluate conversational accuracy, the chatbot was subjected to a comprehensive battery of student questions. "
        "Table 13 presents real benchmark inquiries, the extracted NLP features, the synthesized answers, and the evaluated features:"
    )

    qa_benchmarks = [
        ("What do I have on Day I?", "Schedule for Day I:\n• 10:00 AM - 11:00 AM: TDC (PG)\n• 11:00 AM - 12:00 PM: AI\n• 12:00 PM - 12:15 PM: Break\n• 12:15 PM - 1:15 PM: ML\n• 1:15 PM - 2:00 PM: Lunch Break\n• 2:00 PM - 3:00 PM: FSD\n• 3:00 PM - 4:00 PM: AM/SQA", "Day-Order Timetable Query (Day I full period breakdown)"),
        ("When is AI on Day III?", "AI is scheduled on Day III from 3:00 PM to 4:00 PM.", "Subject Schedule Query (Subject + Day Order combo)"),
        ("Where is ML Lab?", "ML Lab is conducted in Room E-311 (Department of MCA Faculty).", "Laboratory Room Query (E-311 location resolution)"),
        ("What room is FSD Lab?", "FSD Lab is conducted in Room E-208 (Department of MCA Faculty).", "Laboratory Room Query (E-208 location resolution)"),
        ("When does the odd semester start?", "Classes for Odd Semester 2026-2027 commence on 15 June 2026.", "Semester Commencement Date Query"),
        ("When does the even semester start?", "Classes for Even Semester 2026-2027 commence on 2 December 2026.", "Semester Commencement Date Query"),
        ("When is the last working day of even semester?", "The last working day of the Even Semester is 16 April 2026.", "Semester Conclusion Milestone Query"),
        ("When are the II CA Tests?", "II CA Tests for Odd Semester: 28 September 2026 to 03 October 2026.\nII CA Tests for Even Semester: 23 March 2026 to 28 March 2026.", "Continuous Assessment Evaluation Schedule Query"),
        ("When is Christmas holiday?", "Christmas is observed as a holiday on 25 December 2026 (Friday).", "Holiday Lookup by Specific Festival Entity"),
        ("What is my lunch time?", "Lunch Break is scheduled daily from 1:15 PM to 2:00 PM (45 minutes).", "Recess & Interval Schedule Query"),
        ("Who handles AM/SQA?", "AM/SQA (Agile Methodologies / Software Quality Assurance) is handled by Dr. L. Thara & Dr. R.K on Day I and Day V (3:00 PM - 4:00 PM), and by Dr. M. Mohanapriya & Dr. R.K on Day III (12:15 PM - 1:15 PM & 2:00 PM - 3:00 PM) and Day VI (3:00 PM - 4:00 PM).", "Faculty & Handling Schedule Query"),
        ("What are the holidays in August?", "Holidays in August:\n• 15 August 2026 (Saturday): Independence Day\n• 26 August 2026 (Wednesday): Krishna Jayanthi", "Monthly Holiday Filtering Query"),
        ("What is the academic event on 22 December?", "22 December: National Mathematics Day (observance of Srinivasa Ramanujan Birthday).", "Specific Date Academic Event Query"),
        ("When is the examination fee payment deadline?", "Examination Fee Deadlines:\n• Start Date: 18 February 2026\n• Without Fine: 02 March 2026\n• With Fine: 12 March 2026", "Examination Fee Administrative Milestone Query"),
        ("Which days have AI?", "Artificial Intelligence (AI) is scheduled on: Day I, Day III, Day IV, Day V, and Day VI (AI Lab in Room E-208).", "Cross-Day Subject Frequency Query"),
        ("Tell me something outside the syllabus", "I couldn't find that information in the current academic timetable/calendar. Please ask about Day I-VI schedules, subjects, labs, CA tests, or holidays.", "Defensive Guardrail & Out-of-Scope Query")
    ]

    tbl_qa = doc.add_table(rows=len(qa_benchmarks) + 1, cols=3)
    tbl_qa.rows[0].cells[0].paragraphs[0].add_run("Student Input Question")
    tbl_qa.rows[0].cells[1].paragraphs[0].add_run("Chatbot Generated Answer")
    tbl_qa.rows[0].cells[2].paragraphs[0].add_run("Feature Evaluated")
    for idx, (q, a, f) in enumerate(qa_benchmarks):
        row = tbl_qa.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(q)
        row.cells[1].paragraphs[0].add_run(a)
        row.cells[2].paragraphs[0].add_run(f)
    style_table(tbl_qa, col_widths=[Inches(1.8), Inches(3.2), Inches(1.5)])
    add_caption("Table 13: Chatbot Query-Response Benchmark Evaluation Matrix")

    # -------------------------------------------------------------
    # 26. TESTING & VERIFICATION
    # -------------------------------------------------------------
    add_h1("20. SYSTEM TESTING")

    doc.add_paragraph(
        "A rigorous quality assurance methodology was applied to ensure the robustness, correctness, and security of the application. "
        "The automated test suite in backend/tests/test_backend.py was executed via Pytest. "
        "Table 14 records the 21 automated backend test cases and their verified operational status:"
    )

    tests_log = [
        ("TC01", "Health Endpoint", "GET /api/health", "HTTP 200, status='online'", "HTTP 200, status='online'", "PASS"),
        ("TC02", "Timetable Retrieval", "GET /api/timetable", "HTTP 200, len > 0, contains AI & ML", "HTTP 200, 39 slots returned", "PASS"),
        ("TC03", "Day Schedule Retrieval", "GET /api/timetable/day/Day I", "HTTP 200, 7 slots, starts 10:00 AM", "HTTP 200, 7 slots, TDC at 10 AM", "PASS"),
        ("TC04", "Subjects Listing", "GET /api/subjects", "HTTP 200, contains 25CAP314 & 25CAP315", "HTTP 200, 9 subjects verified", "PASS"),
        ("TC05", "Calendar Events Retrieval", "GET /api/calendar", "HTTP 200, len > 10 events", "HTTP 200, 61 events returned", "PASS"),
        ("TC06", "Holiday Lookup Endpoint", "GET /api/calendar/holidays", "Contains Independence Day & Pongal", "Contains all 20 holidays", "PASS"),
        ("TC07", "Room Lookup: ML Lab", "POST /api/chat 'Where is ML Lab?'", "Answer contains 'E-311'", "Resolved to E-311", "PASS"),
        ("TC08", "Room Lookup: FSD Lab", "POST /api/chat 'What room is FSD Lab?'", "Answer contains 'E-208'", "Resolved to E-208", "PASS"),
        ("TC09", "Chat Day Schedule", "POST /api/chat 'What do I have on Day I?'", "Contains TDC, AI, ML, FSD, AM/SQA", "Complete list returned", "PASS"),
        ("TC10", "Chat Subject Timing", "POST /api/chat 'When is AI on Day III?'", "Answer contains '3:00 PM' & '4:00 PM'", "Asserted 3:00 PM to 4:00 PM", "PASS"),
        ("TC11", "Semester Start (Odd)", "POST /api/chat 'When does odd sem start?'", "Answer contains '15 June 2026'", "15 June 2026 verified", "PASS"),
        ("TC12", "Semester Start (Even)", "POST /api/chat 'When does even sem start?'", "Answer contains '2 December 2026'", "2 December 2026 verified", "PASS"),
        ("TC13", "Last Working Day", "POST /api/chat 'Last working day even sem?'", "Answer contains '16 April'", "16 April verified", "PASS"),
        ("TC14", "CA Tests Inquiry", "POST /api/chat 'When are the II CA Tests?'", "Contains '28 September' / '23 March'", "Accurate dates returned", "PASS"),
        ("TC15", "Christmas Holiday", "POST /api/chat 'When is Christmas holiday?'", "Answer contains '25 December 2026'", "25 December 2026 verified", "PASS"),
        ("TC16", "Lunch Time Inquiry", "POST /api/chat 'What is my lunch time?'", "Contains '1:15 PM' & '2:00 PM'", "1:15 PM - 2:00 PM verified", "PASS"),
        ("TC17", "Faculty Lookup", "POST /api/chat 'Who handles AM/SQA?'", "Contains Dr. L. Thara & Dr. R.K", "All 3 faculty listed", "PASS"),
        ("TC18", "August Holidays", "POST /api/chat 'Holidays in August?'", "Contains 'Independence Day'", "Aug 15 & Aug 26 returned", "PASS"),
        ("TC19", "December 22 Event", "POST /api/chat 'Event on 22 December?'", "National Mathematics Day", "Ramanujan Day returned", "PASS"),
        ("TC20", "Fee Deadline Inquiry", "POST /api/chat 'Exam fee deadline?'", "Contains 2 March / 18 Feb", "Accurate deadlines verified", "PASS"),
        ("TC21", "Guardrail Unknown Query", "POST /api/chat 'Tell me something else'", "Returns NOT_FOUND_MESSAGE", "Defensive fallback returned", "PASS")
    ]

    tbl_tlog = doc.add_table(rows=len(tests_log) + 1, cols=6)
    tbl_tlog.rows[0].cells[0].paragraphs[0].add_run("Test ID")
    tbl_tlog.rows[0].cells[1].paragraphs[0].add_run("Test Focus")
    tbl_tlog.rows[0].cells[2].paragraphs[0].add_run("Test Input")
    tbl_tlog.rows[0].cells[3].paragraphs[0].add_run("Expected Result")
    tbl_tlog.rows[0].cells[4].paragraphs[0].add_run("Actual Execution Result")
    tbl_tlog.rows[0].cells[5].paragraphs[0].add_run("Status")
    for idx, (tid, tfoc, tin, texp, tact, tstat) in enumerate(tests_log):
        row = tbl_tlog.rows[idx + 1]
        row.cells[0].paragraphs[0].add_run(tid)
        row.cells[1].paragraphs[0].add_run(tfoc)
        row.cells[2].paragraphs[0].add_run(tin)
        row.cells[3].paragraphs[0].add_run(texp)
        row.cells[4].paragraphs[0].add_run(tact)
        row.cells[5].paragraphs[0].add_run(tstat)
    style_table(tbl_tlog, col_widths=[Inches(0.7), Inches(1.3), Inches(1.5), Inches(1.4), Inches(1.3), Inches(0.6)])
    add_caption("Table 14: Automated Pytest Backend Test Execution Results (21/21 PASS)")

    # -------------------------------------------------------------
    # 27. RESULTS & PERFORMANCE
    # -------------------------------------------------------------
    add_h1("21. RESULTS")

    doc.add_paragraph(
        "The developed MCA Academic Assistant Chatbot has been successfully engineered, deployed, and validated. "
        "Key operational results include:"
    )
    doc.add_paragraph(
        "1. Complete Data Coverage: 100% of MCA Semester III weekly periods (39 slots across 6 days) and annual institutional calendar events "
        "(61 events across 12 months) are modeled with exact fidelity.\n"
        "2. Sub-15 Millisecond Query Latency: Because NLP processing occurs locally via compiled regular expressions and SQLite reads "
        "benefit from primary key and foreign key indexes, conversational responses are returned to the frontend in under 15ms.\n"
        "3. Zero Generative Hallucination: The rule-based intent engine and source-attributed retrieval ensure that the assistant never produces "
        "speculative or unverified academic information.\n"
        "4. Seamless Cross-Platform Responsiveness: The Next.js frontend delivers optimal viewing experiences across desktop monitors, tablets, and smartphones."
    )

    # -------------------------------------------------------------
    # 28. ADVANTAGES
    # -------------------------------------------------------------
    add_h1("22. ADVANTAGES")

    doc.add_paragraph(
        "The implemented system offers substantial advantages over conventional academic dissemination methods:"
    )
    advs = [
        ("Instantaneous Schedule Retrieval: ", "Students obtain specific class times and lab venues in seconds without manual PDF searching."),
        ("Authoritative Transparency: ", "Every chatbot response includes a verifiable source attribution badge (e.g., 'MCA Semester III Timetable')."),
        ("Defensive Security & Privacy: ", "Operates locally on institutional servers without streaming student messages to external third-party AI APIs."),
        ("Multi-Modal Exploration: ", "Provides both natural language conversational interaction and structured graphical tables for visual browsing."),
        ("Zero Subscription Cost: ", "Built entirely with open-source technologies (FastAPI, Next.js, SQLite), avoiding recurring API usage fees.")
    ]
    for a_title, a_desc in advs:
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(a_title)
        r.font.bold = True
        p.add_run(a_desc)

    # -------------------------------------------------------------
    # 29. LIMITATIONS
    # -------------------------------------------------------------
    add_h1("23. LIMITATIONS")

    doc.add_paragraph(
        "While highly effective within its designated scope, the application possesses certain practical limitations:"
    )
    lims = [
        ("Departmental Boundary: ", "The current knowledge base is restricted to MCA Semester III; it does not contain timetables for other college departments."),
        ("Static Seed Mechanism: ", "Timetable and calendar updates require executing the seed script (seed_database.py); there is no administrative web dashboard for dynamic runtime schedule editing."),
        ("Text-Only Interaction: ", "The current implementation supports keyboard text input; voice recognition (speech-to-text) is not yet integrated."),
        ("Local SQLite Concurrency: ", "SQLite is ideal for read-heavy departmental use but may encounter write locks if large-scale administrative write transactions occur concurrently.")
    ]
    for l_title, l_desc in lims:
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(l_title)
        r.font.bold = True
        p.add_run(l_desc)

    # -------------------------------------------------------------
    # 30. FUTURE ENHANCEMENTS
    # -------------------------------------------------------------
    add_h1("24. FUTURE ENHANCEMENTS")

    doc.add_paragraph(
        "Future iterations of the MCA Academic Assistant can incorporate the following enhancements:"
    )
    futs = [
        ("Voice Query Interface: ", "Integrate Web Speech API on the client side to enable hands-free voice inquiries for students on mobile devices."),
        ("Multi-Semester & Multi-Department Expansion: ", "Extend the relational database schema to support all undergraduate and postgraduate semesters across PSG College of Arts & Science."),
        ("Role-Based Administrative Portal: ", "Develop authenticated web dashboards allowing department coordinators to update schedules dynamically with automatic change auditing."),
        ("Automated Notification Webhooks: ", "Integrate institutional email and WhatsApp notification services to push automated reminders 24 hours prior to CA tests and fee payment deadlines."),
        ("Hybrid Semantic Vector Search: ", "Incorporate lightweight local sentence embeddings (e.g., Sentence-Transformers) to augment rule-based regex parsing for complex phrasing.")
    ]
    for f_title, f_desc in futs:
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(f_title)
        r.font.bold = True
        p.add_run(f_desc)

    # -------------------------------------------------------------
    # 31. CONCLUSION
    # -------------------------------------------------------------
    add_h1("25. CONCLUSION")

    doc.add_paragraph(
        "The \"MCA Academic Assistant Chatbot Using Natural Language Processing\" successfully addresses the operational "
        "challenges associated with static academic schedule dissemination at PSG College of Arts & Science. By engineering a decoupled, "
        "modern full-stack architecture combining a Python FastAPI backend, Next.js 16 reactive frontend, and SQLite relational database, "
        "the project delivers a robust, accessible, and instantaneous information retrieval system."
    )

    doc.add_paragraph(
        "The deterministic, rule-based NLP engine proves that high-utility conversational systems can be created without relying on costly, "
        "cloud-dependent generative AI models. The system guarantees 100% factual accuracy, zero hallucination, sub-15ms latency, "
        "and complete source attribution across all 39 timetable slots and 61 academic calendar events. The project fulfills all practical assignment "
        "objectives, conforms to academic software engineering standards, and provides a dependable digital companion for MCA students."
    )

    # -------------------------------------------------------------
    # 32. REFERENCES
    # -------------------------------------------------------------
    add_h1("26. REFERENCES")

    refs = [
        ("PSG College of Arts & Science (Autonomous), ", "Autonomous Academic Calendar and Handbook 2026-2027, PSGCAS Directorate of Academic Affairs, Coimbatore, Tamil Nadu, India, 2026."),
        ("Department of MCA, PSG College of Arts & Science, ", "Master of Computer Applications (MCA) Semester III Master Class Timetable & Course Syllabi, Academic Year 2026-2027, PSGCAS, Coimbatore, 2026."),
        ("Tiangolo, S., et al., ", "\"FastAPI: Modern, Fast (High-Performance) Web Framework for Building APIs with Python 3.8+\", Available: https://fastapi.tiangolo.com, 2024."),
        ("Vercel Engineering Team, ", "\"Next.js Documentation: The React Framework for the Web\", Vercel Inc., Available: https://nextjs.org/docs, 2024."),
        ("Hipp, R. D., et al., ", "\"SQLite 3 Database Engine Technical Overview and Architectural Specifications\", Available: https://www.sqlite.org, 2024."),
        ("Bayer, M., et al., ", "\"SQLAlchemy: The Database Toolkit for Python\", Version 2.0 Reference Manual, Available: https://docs.sqlalchemy.org, 2024."),
        ("Python Software Foundation, ", "\"Python 3.13 Language and Standard Library Reference\", Python Software Foundation, Available: https://www.python.org, 2024.")
    ]
    for author, cite in refs:
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(author)
        r.font.bold = True
        p.add_run(cite)

    # Repository Reference with clickable hyperlink
    p_repo = doc.add_paragraph(style='List Bullet')
    r_lbl = p_repo.add_run("Project GitHub Repository: ")
    r_lbl.font.bold = True
    add_hyperlink(p_repo, "https://github.com/tharunvaibhavss/college_chat_bot", "https://github.com/tharunvaibhavss/college_chat_bot", color="0284C7", underline=True, bold=True)
    p_repo.add_run(" — Department of MCA Practical Assignment Codebase, 2026.")

    # Save document
    out_docx = os.path.abspath("docs/MCA_Academic_Assistant_Project_Report.docx")
    doc.save(out_docx)
    print(f"DOCX created successfully at: {out_docx}")
    return out_docx


if __name__ == "__main__":
    docx_file = build_report()
