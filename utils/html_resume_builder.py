# utils/html_resume_builder.py

from io import BytesIO

def create_html_resume(profile, jd_analysis, tailored_summary, match_details, selected_projects, optimized_experiences):
    """
    Create a beautiful HTML resume with modern design
    Returns: HTML string
    """
    
    personal = profile.get('personal', {})
    
    # Reorder skills - matched first
    all_skills = profile.get('skills', {}).get('technical', [])
    matched_skills = [s for s in all_skills if s.lower() in [m.lower() for m in match_details.get('matched_skills', [])]]
    other_skills = [s for s in all_skills if s not in matched_skills]
    ordered_skills = (matched_skills + other_skills)[:15]  # Top 15 skills
    
    # Build HTML
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{personal.get('name', 'Resume')}</title>
    <style>
        /* Fallback to system fonts for offline PDF reliability (similar to Roboto) */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        body {{ font-family: 'Roboto', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Roboto', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: white;
        }}
        
        .container {{
            width: 210mm;
            min-height: 297mm;
            margin: 0 auto;
            background: white;
            display: flex;
            page-break-inside: avoid;  /* Better PDF pagination */
        }}
        
        /* Left Sidebar */
        .sidebar {{
            width: 35%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            page-break-inside: avoid;
        }}
        
        .profile-section {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .name {{
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .title {{
            font-size: 14px;
            font-weight: 300;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        
        .contact-item {{
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            font-size: 11px;
            word-break: break-all;
        }}
        
        .contact-icon {{
            width: 20px;
            margin-right: 10px;
            font-weight: 500;
        }}
        
        .sidebar-section {{
            margin-top: 35px;
        }}
        
        .sidebar-heading {{
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 8px;
        }}
        
        .skill-item {{
            margin-bottom: 12px;
        }}
        
        .skill-name {{
            font-size: 11px;
            margin-bottom: 4px;
            font-weight: 400;
        }}
        
        .skill-bar {{
            background: rgba(255,255,255,0.2);
            height: 6px;
            border-radius: 3px;
            overflow: hidden;
        }}
        
        .skill-fill {{
            background: white;
            height: 100%;
            border-radius: 3px;
        }}
        
        .education-item {{
            margin-bottom: 20px;
            font-size: 11px;
        }}
        
        .education-degree {{
            font-weight: 500;
            margin-bottom: 4px;
        }}
        
        .education-school {{
            opacity: 0.9;
            margin-bottom: 2px;
        }}
        
        .education-year {{
            opacity: 0.8;
            font-size: 10px;
        }}
        
        /* Right Main Content */
        .main-content {{
            width: 65%;
            padding: 40px 35px;
            page-break-inside: avoid;
        }}
        
        .section {{
            margin-bottom: 28px;
            page-break-inside: avoid;  /* Prevent sections from splitting across pages */
        }}
        
        .section-heading {{
            font-size: 18px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 6px;
        }}
        
        .summary-text {{
            font-size: 11px;
            line-height: 1.7;
            text-align: justify;
            color: #555;
        }}
        
        .experience-item {{
            margin-bottom: 22px;
        }}
        
        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 6px;
        }}
        
        .job-title {{
            font-size: 13px;
            font-weight: 700;
            color: #333;
        }}
        
        .job-duration {{
            font-size: 10px;
            color: #777;
            font-style: italic;
        }}
        
        .job-company {{
            font-size: 11px;
            color: #667eea;
            font-weight: 500;
            margin-bottom: 8px;
        }}
        
        .job-responsibilities {{
            list-style: none;
            padding-left: 0;
        }}
        
        .job-responsibilities li {{
            font-size: 10.5px;
            line-height: 1.6;
            margin-bottom: 5px;
            padding-left: 15px;
            position: relative;
            color: #555;
        }}
        
        .job-responsibilities li:before {{
            content: "▸";
            position: absolute;
            left: 0;
            color: #667eea;
            font-weight: bold;
        }}
        
        .project-item {{
            margin-bottom: 18px;
        }}
        
        .project-name {{
            font-size: 12px;
            font-weight: 700;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .project-description {{
            font-size: 10.5px;
            line-height: 1.6;
            color: #555;
            margin-bottom: 5px;
        }}
        
        .project-tech {{
            font-size: 10px;
            color: #667eea;
            font-style: italic;
        }}
        
        .certifications-list {{
            font-size: 10.5px;
            color: #555;
        }}
        
        .cert-item {{
            margin-bottom: 8px;
        }}
        
        .cert-name {{
            font-weight: 500;
            color: #333;
        }}
        
        @media print {{
            .container {{
                width: 100%;
                margin: 0;
                box-shadow: none;
            }}
            
            body {{
                margin: 0;
                padding: 0;
                -webkit-print-color-adjust: exact;  /* Preserve colors/gradients in PDF */
                color-adjust: exact;
                print-color-adjust: exact;
            }}
            
            .sidebar {{
                -webkit-print-color-adjust: exact;
                color-adjust: exact;
                print-color-adjust: exact;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- LEFT SIDEBAR -->
        <div class="sidebar">
            <div class="profile-section">
                <div class="name">{personal.get('name', 'YOUR NAME')}</div>
                <div class="title">{jd_analysis.get('role_type', 'Professional')}</div>
            </div>
            
            <!-- Contact -->
            <div class="sidebar-section">
                <div class="sidebar-heading">Contact</div>
"""
    
    # Add contact info
    if personal.get('email'):
        html += f'                   <div class="contact-item"><span class="contact-icon">✉</span>{personal["email"]}</div>\n'
    if personal.get('phone'):
        html += f'                   <div class="contact-item"><span class="contact-icon">☎</span>{personal["phone"]}</div>\n'
    if personal.get('location'):
        html += f'                   <div class="contact-item"><span class="contact-icon">📍</span>{personal["location"]}</div>\n'
    if personal.get('linkedin'):
        html += f'                   <div class="contact-item"><span class="contact-icon">💼</span>{personal["linkedin"]}</div>\n'
    
    html += """
            </div>
            
            <!-- Skills -->
            <div class="sidebar-section">
                <div class="sidebar-heading">Skills</div>
"""
    
    # Add skills with visual bars (matched skills get higher bars)
    for skill in ordered_skills[:10]:  # Top 10 skills for sidebar
        is_matched = skill.lower() in [m.lower() for m in match_details.get('matched_skills', [])]
        width = "95%" if is_matched else "75%"
        html += f"""
                <div class="skill-item">
                    <div class="skill-name">{skill}</div>
                    <div class="skill-bar">
                        <div class="skill-fill" style="width: {width};"></div>
                    </div>
                </div>
"""
    
    html += """
            </div>
            
            <!-- Education -->
"""
    
    education = profile.get('education', [])
    if education:
        html += """
            <div class="sidebar-section">
                <div class="sidebar-heading">Education</div>
"""
        for edu in education[:2]:  # Max 2 for space
            html += f"""
                <div class="education-item">
                    <div class="education-degree">{edu.get('degree', 'Degree')}</div>
                    <div class="education-school">{edu.get('institution', 'Institution')}</div>
                    <div class="education-year">{edu.get('year', '')}</div>
                </div>
"""
        html += """
            </div>
"""
    
    html += """
        </div>
        
        <!-- RIGHT MAIN CONTENT -->
        <div class="main-content">
            <!-- Professional Summary -->
            <div class="section">
                <div class="section-heading">Professional Summary</div>
                <div class="summary-text">
                    """ + tailored_summary + """
                </div>
            </div>
"""
    
    # Experience section
    if optimized_experiences:
        html += """
            <!-- Experience -->
            <div class="section">
                <div class="section-heading">Professional Experience</div>
"""
        for exp in optimized_experiences[:2]:  # Max 2 for space
            html += f"""
                <div class="experience-item">
                    <div class="job-header">
                        <div class="job-title">{exp.get('role', 'Role')}</div>
                        <div class="job-duration">{exp.get('duration', '')}</div>
                    </div>
                    <div class="job-company">{exp.get('company', 'Company')}</div>
                    <ul class="job-responsibilities">
"""
            for resp in exp.get('responsibilities', [])[:3]:
                html += f"                           <li>{resp}</li>\n"
            
            html += """
                    </ul>
                </div>
"""
        html += """
            </div>
"""
    
    # Projects section
    if selected_projects:
        html += """
            <!-- Projects -->
            <div class="section">
                <div class="section-heading">Key Projects</div>
"""
        for proj in selected_projects[:3]:
            desc = proj.get('description', '')
            if len(desc) > 180:
                desc = desc[:180] + '...'
            
            html += f"""
                <div class="project-item">
                    <div class="project-name">{proj.get('name', 'Project')}</div>
                    <div class="project-description">{desc}</div>
                    <div class="project-tech">Technologies: {', '.join(proj.get('tech_stack', [])[:6])}</div>
                </div>
"""
        html += """
            </div>
"""
    
    # Certifications section
    certifications = profile.get('certifications', [])
    if certifications:
        html += """
            <!-- Certifications -->
            <div class="section">
                <div class="section-heading">Certifications</div>
                <div class="certifications-list">
"""
        for cert in certifications[:3]:
            html += f"""
                    <div class="cert-item">
                        <span class="cert-name">{cert.get('name', 'Certification')}</span> - {cert.get('issuer', 'Issuer')} ({cert.get('year', '')})
                    </div>
"""
        html += """
                </div>
            </div>
"""
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    return html


def html_to_pdf(html_string, output_filename='resume.pdf'):
    """
    Convert HTML string to PDF using pdfkit (wkhtmltopdf engine—no async issues)
    Returns: BytesIO object with PDF bytes, or None on error (triggers DOCX fallback)
    """
    try:
        import pdfkit
        
        # PDF options optimized for your resume template (A4, margins, CSS support)
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'UTF-8',
            'no-outline': None,  # No table of contents
            'print-media-type': None,  # Apply @media print styles (preserves gradients/colors)
            'disable-smart-shrinking': None,  # Preserve exact layout (flexbox, widths)
            'enable-local-file-access': None,  # For any local resources
            'dpi': 300,  # Higher resolution for crisp small fonts (10-13px) and details
            'javascript-delay': 1000,  # Wait for fonts/CSS to load (your HTML is static, but safe)
            'lowquality': False  # High quality output (no compression artifacts)
        }
        
        # If wkhtmltopdf path issues arise (unlikely since test worked), uncomment below:
        # config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\wkhtmltopdf.exe')
        # pdf_bytes = pdfkit.from_string(html_string, False, options=options, configuration=config)
        
        # Generate PDF bytes directly (False = return bytes, not save to file)
        pdf_bytes = pdfkit.from_string(html_string, False, options=options)
        
        if not pdf_bytes or len(pdf_bytes) == 0:
            raise Exception("Empty PDF output generated—check HTML content")
        
        # Wrap in BytesIO for Streamlit download compatibility
        pdf_buffer = BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        return pdf_buffer
        
    except ImportError:
        print("pdfkit not installed. Run: pip install pdfkit")
        return None
    except FileNotFoundError:
        print("wkhtmltopdf executable not found. Ensure it's installed and in PATH (test with 'wkhtmltopdf --version').")
        return None
    except Exception as e:
        print(f"Error converting to PDF with pdfkit: {e}")
        return None
