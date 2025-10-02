from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from io import BytesIO

def set_narrow_margins(doc):
    """Set narrow margins for maximum space"""
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

def create_resume_docx(profile, jd_analysis, tailored_summary, match_details, selected_projects, optimized_experiences):
    """Create a professional, ATS-friendly, 1-PAGE resume"""
    doc = Document()
    
    # Set narrow margins
    set_narrow_margins(doc)
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(10)
    
    # Reduce spacing
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(2)
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    
    personal = profile.get('personal', {})
    
    # ==================== HEADER ====================
    # Name
    name_para = doc.add_paragraph()
    name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name_run = name_para.add_run(personal.get('name', 'YOUR NAME').upper())
    name_run.bold = True
    name_run.font.size = Pt(16)
    name_para.paragraph_format.space_after = Pt(2)
    
    # Contact Info
    contact_para = doc.add_paragraph()
    contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact_parts = []
    
    if personal.get('email'):
        contact_parts.append(personal['email'])
    if personal.get('phone'):
        contact_parts.append(personal['phone'])
    if personal.get('location'):
        contact_parts.append(personal['location'])
    if personal.get('linkedin'):
        contact_parts.append(personal['linkedin'])
    
    contact_run = contact_para.add_run(' | '.join(contact_parts))
    contact_run.font.size = Pt(9)
    contact_para.paragraph_format.space_after = Pt(6)
    
    # ==================== PROFESSIONAL SUMMARY ====================
    add_section_header(doc, 'PROFESSIONAL SUMMARY')
    summary_para = doc.add_paragraph(tailored_summary)
    summary_para.paragraph_format.space_after = Pt(6)
    summary_para.runs[0].font.size = Pt(10)
    
    # ==================== SKILLS ====================
    add_section_header(doc, 'TECHNICAL SKILLS')
    
    # Reorder skills - matched first
    all_skills = profile.get('skills', {}).get('technical', [])
    matched_skills = [s for s in all_skills if s.lower() in [m.lower() for m in match_details.get('matched_skills', [])]]
    other_skills = [s for s in all_skills if s not in matched_skills]
    ordered_skills = matched_skills + other_skills
    
    skills_para = doc.add_paragraph(', '.join(ordered_skills[:18]))
    skills_para.paragraph_format.space_after = Pt(6)
    skills_para.runs[0].font.size = Pt(10)
    
    # ==================== EXPERIENCE ====================
    if optimized_experiences:
        add_section_header(doc, 'PROFESSIONAL EXPERIENCE')
        
        for idx, exp in enumerate(optimized_experiences[:2]):
            # Role and Company
            role_para = doc.add_paragraph()
            role_run = role_para.add_run(f"{exp.get('role', 'Role')} | {exp.get('company', 'Company')}")
            role_run.bold = True
            role_run.font.size = Pt(10)
            role_para.paragraph_format.space_after = Pt(1)
            
            # Duration
            duration_para = doc.add_paragraph()
            duration_run = duration_para.add_run(exp.get('duration', ''))
            duration_run.italic = True
            duration_run.font.size = Pt(9)
            duration_para.paragraph_format.space_after = Pt(2)
            
            # Responsibilities
            for resp in exp.get('responsibilities', [])[:3]:
                bullet_para = doc.add_paragraph(resp, style='List Bullet')
                bullet_para.paragraph_format.space_after = Pt(1)
                bullet_para.paragraph_format.left_indent = Inches(0.25)
                bullet_para.runs[0].font.size = Pt(9.5)
            
            if idx < len(optimized_experiences) - 1:
                doc.add_paragraph().paragraph_format.space_after = Pt(3)
    
    # ==================== PROJECTS ====================
    if selected_projects:
        add_section_header(doc, 'PROJECTS')
        
        for idx, proj in enumerate(selected_projects):
            # Project name
            proj_para = doc.add_paragraph()
            proj_run = proj_para.add_run(proj.get('name', 'Project'))
            proj_run.bold = True
            proj_run.font.size = Pt(10)
            proj_para.paragraph_format.space_after = Pt(1)
            
            # Description (truncated for space)
            desc = proj.get('description', '')
            if len(desc) > 150:
                desc = desc[:150] + '...'
            desc_para = doc.add_paragraph(desc)
            desc_para.paragraph_format.space_after = Pt(1)
            desc_para.runs[0].font.size = Pt(9.5)
            
            # Tech stack
            if proj.get('tech_stack'):
                tech_para = doc.add_paragraph()
                tech_run = tech_para.add_run(f"Tech: {', '.join(proj['tech_stack'][:8])}")
                tech_run.italic = True
                tech_run.font.size = Pt(9)
                tech_para.paragraph_format.space_after = Pt(3)
    
    # ==================== EDUCATION ====================
    education = profile.get('education', [])
    if education:
        add_section_header(doc, 'EDUCATION')
        
        for edu in education[:2]:
            # Degree
            degree_para = doc.add_paragraph()
            degree_run = degree_para.add_run(edu.get('degree', 'Degree'))
            degree_run.bold = True
            degree_run.font.size = Pt(10)
            degree_para.paragraph_format.space_after = Pt(1)
            
            # Institution and year
            inst_text = f"{edu.get('institution', 'Institution')}"
            if edu.get('year'):
                inst_text += f" | {edu.get('year')}"
            if edu.get('gpa'):
                inst_text += f" | GPA: {edu.get('gpa')}"
            
            inst_para = doc.add_paragraph(inst_text)
            inst_para.paragraph_format.space_after = Pt(3)
            inst_para.runs[0].font.size = Pt(9.5)
    
    # ==================== CERTIFICATIONS ====================
    certifications = profile.get('certifications', [])
    if certifications:
        add_section_header(doc, 'CERTIFICATIONS')
        
        cert_texts = []
        for cert in certifications[:3]:
            cert_text = f"{cert.get('name', '')} ({cert.get('issuer', '')})"
            cert_texts.append(cert_text)
        
        cert_para = doc.add_paragraph(' | '.join(cert_texts))
        cert_para.runs[0].font.size = Pt(9)
        cert_para.paragraph_format.space_after = Pt(3)
    
    # Save to BytesIO
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    
    return file_stream

def add_section_header(doc, text):
    """Add a section header"""
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0, 0, 0)
    para.paragraph_format.space_before = Pt(6)
    para.paragraph_format.space_after = Pt(3)
    
    return para