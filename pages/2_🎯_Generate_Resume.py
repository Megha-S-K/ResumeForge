import json
import os
import sys
import base64
import streamlit as st

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.url_extractor import extract_from_url
from utils.ai_analyzer import (
    analyze_job_description, 
    generate_tailored_summary, 
    calculate_match_score,
    generate_skill_recommendations,
    select_best_projects, 
    optimize_experience_bullets
)
from style import local_css, inject_custom_components
from utils.docx_builder import create_resume_docx
from utils.html_resume_builder import create_html_resume, html_to_pdf

# Page configuration
st.set_page_config(
    page_title="Generate Resume - ResumeForge AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
local_css("style.css")
inject_custom_components()

# Initialize session state
def init_session_state():
    defaults = {
        'jd_text': '',
        'generated': False,
        'jd_analysis': None,
        'match_details': None,
        'recommendations': None,
        'selected_skills': set(),
        'tailored_summary': ''
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Load profile
def load_profile():
    try:
        with open('data/user_profile.json', 'r') as f:
            return json.load(f)
    except:
        return None

# Header
st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 3.5rem;">🎯</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style="
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    ">
        Generate Tailored Resume
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
    <p style="
        text-align: center;
        font-size: 1.125rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    ">
        Paste a job URL or description, and watch AI create a perfectly tailored resume! 🚀
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# Check profile
profile = load_profile()
if not profile or not profile.get('personal', {}).get('name'):
    st.error("❌ Please create your profile first!")
    st.info("👈 Go to **Profile Builder** in the sidebar to create your profile.")
    st.stop()

# Job Description Input
st.header("📋 Step 1: Input Job Description")

tab1, tab2 = st.tabs(["🔗 Paste URL", "📝 Paste Text"])

with tab1:
    st.write("**Paste a job posting URL (LinkedIn, Indeed, company website, etc.)**")
    url = st.text_input("Job URL:", placeholder="https://www.linkedin.com/jobs/view/...")
    
    if url:
        with st.spinner("🔍 Extracting job description from URL..."):
            success, extracted_text, error = extract_from_url(url)
        
        if success:
            st.success("✅ Job description extracted successfully!")
            st.session_state.jd_text = extracted_text
        else:
            st.error(f"❌ {error}")
            st.info("👇 Try pasting the text directly in the 'Paste Text' tab instead.")

with tab2:
    st.write("**Copy and paste the complete job description:**")
    st.text_area("Job Description:", height=300, key="jd_text")

# Get current JD text
jd_text = st.session_state.jd_text
has_valid_jd = jd_text and len(jd_text) > 100

# Action Buttons (Always visible when not generated)
if not st.session_state.generated:
    col_extract, col_generate = st.columns([1, 1])
    
    with col_extract:
        if st.button("Extract Job Description", 
                    use_container_width=True, 
                    type="primary",
                    key="extract_btn"):
            pass
    
    with col_generate:
        if st.button("🚀 Generate Tailored Resume", 
                    type="primary", 
                    use_container_width=True, 
                    disabled=not has_valid_jd):
            st.session_state.generated = True
            
            # Center the spinner messages
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            

            # Analyze JD
            with st.spinner("🤖 AI is analyzing the job description..."):
                analysis_result = analyze_job_description(jd_text)
            
            if not analysis_result['success']:
                st.error(f"❌ Error analyzing job: {analysis_result['error']}")
                st.session_state.generated = False
                st.markdown("</div>", unsafe_allow_html=True)
                st.stop()
            
            st.session_state.jd_analysis = analysis_result['data']
            
            # Calculate Match Score
            with st.spinner("🎯 Calculating your match score..."):
                st.session_state.match_details = calculate_match_score(
                    profile, st.session_state.jd_analysis
                )
            
            # Generate Skill Recommendations
            with st.spinner("🤖 Analyzing skill gaps..."):
                st.session_state.recommendations = generate_skill_recommendations(
                    profile, st.session_state.jd_analysis
                )
            
            # Generate Tailored Summary
            with st.spinner("✨ Generating tailored summary..."):
                st.session_state.tailored_summary = generate_tailored_summary(
                    profile, st.session_state.jd_analysis
                )
            st.markdown("</div>", unsafe_allow_html=True)
            st.session_state.selected_skills = set()
            st.rerun()

# Display Generated Content
if st.session_state.generated and st.session_state.jd_analysis:
    st.write("---")
    
    jd_analysis = st.session_state.jd_analysis
    match_details = st.session_state.match_details
    recommendations = st.session_state.recommendations
    tailored_summary = st.session_state.tailored_summary
    
    # Display Analysis (Aesthetic Layout) - CORRECTED SECTION
    st.markdown("""
    <h1 style="
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    ">
        Job Analysis Results
    </h1>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✔️ Required Skills")
        required_skills = jd_analysis.get('required_skills', [])[:10]
        cols_skills = st.columns(2)
        for i, skill in enumerate(required_skills):
            with cols_skills[i % 2]:
                st.write(f"• {skill}")

    with col2:
        st.subheader("Role Information")
        
        # Stack Position and Level vertically with proper spacing/padding
        with st.container():  # Container for grouping and implicit padding
            st.metric("Position", jd_analysis.get('role_type', 'N/A'))
            st.markdown("")  # Adds a small vertical space (like padding)
            st.metric("Level", jd_analysis.get('seniority_level', 'N/A'))
    
    # Match Score
    score = match_details['score']
    # Render Match Score Card
    match_score_text = (
        'Excellent Match! 🎉' if score >= 80 else ('Good Match! 👍' if score >= 60 else "Moderate Match – Let's improve it!")
    )
    st.markdown(f"""
    <div class='card' style='padding:2rem 1.5rem;margin-bottom:1.5rem;'>
        <h2 style='margin-bottom:0.5rem;'>🎯 Your Match Score</h2>
        <div style='display:flex;align-items:center;gap:1.5rem;'>
            <div style='flex:1;'>
                <div style='background:linear-gradient(90deg,#6366f1,#8b5cf6);height:22px;border-radius:10px;overflow:hidden;'>
                    <div style='width:{score}%;background:#10b981;height:100%;border-radius:10px;'></div>
                </div>
            </div>
            <span style='font-weight:bold;font-size:1.5rem;color:#10b981;'>{score}%</span>
        </div>
        <p style='margin-top:0.5rem;color:#94a3b8;font-size:1.1rem;'>
            {match_score_text}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Matching and Missing Skills
    matched_skills_html = "".join([
        f'<li style="margin-bottom:0.4rem;font-weight:500;"> {skill}</li>'
        for skill in match_details['matched_skills'][:15]
    ])
    
    missing_skills_html = (
        "<ul style='list-style:none;padding-left:0;margin:0;'>" + "".join([
            f'<li style="margin-bottom:0.4rem;font-weight:500;"> {skill}</li>'
            for skill in match_details['missing_skills'][:10]
        ]) + "</ul>"
        if match_details['missing_skills']
        else '<div style="color:#10b981;font-weight:500;">🎉 You have all required skills!</div>'
    )

    st.markdown(f"""
    <div style='display:flex;gap:2rem;flex-wrap:wrap;'>
        <div class='card' style='flex:1;min-width:260px;padding:1.2rem;'>
            <h3 style='margin-bottom:0.5rem;'>✔️ Your Matching Skills</h3>
            <ul style='list-style:none;padding-left:0;margin:0;'>
                {matched_skills_html}
            </ul>
        </div>
        <div class='card' style='flex:1;min-width:260px;padding:1.2rem;'>
            <h3 style='margin-bottom:0.5rem;'>⚠️ Missing Skills</h3>
            {missing_skills_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    # AI SKILL RECOMMENDATIONS (Interactive and Aesthetic)
    st.header("💡 AI Skill Recommendations")
    
    if recommendations['has_recommendations']:
        st.caption("**Boost your match! Select skills from below and update all at once.**")
        
        selected_skills_list = list(st.session_state.selected_skills)
        
        # Critical Missing Skills Expander
        with st.expander("🚨 Critical Skills (Must-Have from Job)", expanded=True):
            if recommendations['critical_missing']:
                cols = st.columns(3)
                for idx, skill in enumerate(recommendations['critical_missing']):
                    with cols[idx % 3]:
                        is_checked = skill in st.session_state.selected_skills
                        if st.checkbox(f"**{skill}**", value=is_checked, key=f"crit_{idx}"):
                            st.session_state.selected_skills.add(skill)
                        else:
                            st.session_state.selected_skills.discard(skill)
            else:
                st.write("No critical skills missing! 🎉")
        
        
        # AI Suggestions Expander
        with st.expander("🤖 AI-Suggested Skills", expanded=False):
            st.caption("Tailored to your profile and this role.")
            if recommendations['ai_suggestions']:
                cols = st.columns(3)
                for idx, skill in enumerate(recommendations['ai_suggestions']):
                    with cols[idx % 3]:
                        is_checked = skill in st.session_state.selected_skills
                        if st.checkbox(f"**{skill}**", value=is_checked, key=f"ai_{idx}"):
                            st.session_state.selected_skills.add(skill)
                        else:
                            st.session_state.selected_skills.discard(skill)
            else:
                st.write("No AI suggestions at this time.")
        
        # Preview Selected Skills (Dynamic and Aesthetic)
        st.write("---")
        selected_skills_list = list(st.session_state.selected_skills)
        if selected_skills_list:
            st.header(f"**Preview: {len(selected_skills_list)} skill selected across categories**")
            for skill in selected_skills_list:
                st.write(f"✔️ {skill}")

        st.caption("💡 Tip: Check any combination of skills, then update your profile below. Regenerate to see the impact!")
        
        
        # Update Profile Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Update Profile with Selected Skills", 
                        type="primary", 
                        use_container_width=True,
                        disabled=len(selected_skills_list) == 0):
                
                added_count = 0
                for skill in selected_skills_list:
                    if skill not in profile['skills']['technical']:
                        profile['skills']['technical'].append(skill)
                        added_count += 1
                
                with open('data/user_profile.json', 'w') as f:
                    json.dump(profile, f, indent=2)
                
                st.success(f"✅ Profile updated! Added {added_count} new skill(s).")
                st.session_state.selected_skills = set()
                
                if st.button("🔄 Regenerate Resume with Updated Profile", 
                            type="secondary", 
                            use_container_width=True):
                    profile = load_profile()
                    st.session_state.match_details = calculate_match_score(profile, jd_analysis)
                    st.session_state.recommendations = generate_skill_recommendations(profile, jd_analysis)
                    st.session_state.tailored_summary = generate_tailored_summary(profile, jd_analysis)
                    st.rerun()
    else:
        st.success("🎉 Your profile already matches this job perfectly!")
    
    # Tailored Summary
    st.header("📝 Tailored Professional Summary")
    st.info(tailored_summary)
    
    # Resume Preview
    st.header("📄 Resume Preview")
    
    col_preview1, col_preview2 = st.columns(2)
    
    with col_preview1:
        st.subheader("### Professional Summary")
        st.write(tailored_summary)
        
        st.subheader("### Skills")
        all_user_skills = profile.get('skills', {}).get('technical', [])
        matched_skills = [s for s in all_user_skills if s.lower() in [m.lower() for m in match_details['matched_skills']]]
        other_skills = [s for s in all_user_skills if s not in matched_skills]
        ordered_skills = matched_skills + other_skills
        st.write(", ".join(ordered_skills[:15]))
    
    with col_preview2:
        st.subheader("### Experience")
        for exp in profile.get('experience', [])[:3]:
            st.write(f"**{exp['role']}** at {exp['company']} | {exp['duration']}")
            for resp in exp.get('responsibilities', [])[:3]:
                st.write(f"• {resp}")
        
        st.subheader("### Projects")
        for proj in profile.get('projects', [])[:3]:
            st.write(f"**{proj['name']}**")
            st.write(proj['description'])
            st.write(f"*Technologies: {', '.join(proj['tech_stack'])}*")
        
        st.subheader("### Education")
        for edu in profile.get('education', []):
            st.write(f"**{edu['degree']}** - {edu['institution']} ({edu['year']})")
    
    st.write("---")
    
    # Generate Resume Files
    with st.spinner("✨ Creating your stunning resume..."):
        selected_projects = select_best_projects(profile, jd_analysis, max_projects=3)
        jd_keywords = jd_analysis.get('keywords', [])
        optimized_experiences = optimize_experience_bullets(
            profile.get('experience', []), 
            jd_keywords, 
            max_bullets=3
        )
        
        html_resume = create_html_resume(
            profile, jd_analysis, tailored_summary, match_details,
            selected_projects, optimized_experiences
        )
        
        st.success("✅ Resume generated successfully!")
        
        # Preview
        st.subheader("📄 Live Preview")
        b64_html = base64.b64encode(html_resume.encode()).decode()
        iframe_html = f'<iframe src="data:text/html;base64,{b64_html}" width="100%" height="800px" style="border: 2px solid #667eea; border-radius: 10px;"></iframe>'
        st.components.v1.html(iframe_html, height=820, scrolling=True)
        
        # Download Options
        st.write("---")
        st.subheader("💾 Download Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.spinner("📄 Generating PDF..."):
                pdf_file = html_to_pdf(html_resume)
            
            if pdf_file:
                company_name = jd_analysis.get('role_type', 'job').replace(' ', '_')
                pdf_filename = f"resume_{company_name}_{profile['personal']['name'].replace(' ', '_')}.pdf"
                
                st.download_button(
                    label="📄 Download Beautiful PDF",
                    data=pdf_file,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            else:
                st.error("PDF generation failed. Please try DOCX format.")
        
        with col2:
            with st.spinner("📝 Generating DOCX..."):
                docx_file = create_resume_docx(
                    profile, jd_analysis, tailored_summary, match_details,
                    selected_projects, optimized_experiences
                )
            
            company_name = jd_analysis.get('role_type', 'job').replace(' ', '_')
            docx_filename = f"resume_{company_name}_{profile['personal']['name'].replace(' ', '_')}.docx"
            
            st.download_button(
                label="📝 Download Plain DOCX",
                data=docx_file,
                file_name=docx_filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        
        st.balloons()
        st.success("🎉 Your tailored resume is ready! Choose your preferred format above.")

# Footer
st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)