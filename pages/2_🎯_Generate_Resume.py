import streamlit as st
import json
import os
import sys

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.url_extractor import extract_from_url
from utils.ai_analyzer import analyze_job_description, generate_tailored_summary, calculate_match_score

st.set_page_config(page_title="Generate Resume", page_icon="🎯", layout="wide")

st.title("🎯 Generate Tailored Resume")
st.write("Paste a job URL or description, and watch AI create a perfectly tailored resume!")

# Check if profile exists
def load_profile():
    try:
        with open('data/user_profile.json', 'r') as f:
            return json.load(f)
    except:
        return None

profile = load_profile()

if not profile or not profile.get('personal', {}).get('name'):
    st.error("❌ Please create your profile first!")
    st.info("👈 Go to **Profile Builder** in the sidebar to create your profile.")
    st.stop()

st.success(f"✅ Profile loaded: {profile['personal']['name']}")

st.write("---")

# Job Description Input
st.header("📋 Step 1: Input Job Description")

# Initialize session state for JD text
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = ""

tab1, tab2 = st.tabs(["🔗 Paste URL", "📝 Paste Text"])

with tab1:
    st.write("**Paste a job posting URL (LinkedIn, Indeed, company website, etc.)**")
    url = st.text_input("Job URL:", placeholder="https://www.linkedin.com/jobs/view/...")
    
    if url:
        with st.spinner("🔍 Extracting job description from URL..."):
            success, extracted_text, error = extract_from_url(url)
        
        if success:
            st.success("✅ Job description extracted successfully!")
            # Save to session state
            st.session_state.jd_text = extracted_text
            
            # Show extracted content (view only; edit in other tab)
            st.text_area("Extracted Content:", value=st.session_state.jd_text, height=300, disabled=True)
            
            st.info("👉 The extracted text is ready! Click 'Generate Resume' below or switch to the 'Paste Text' tab to edit it.")
        else:
            st.error(f"❌ {error}")
            st.info("👇 Try pasting the text directly in the 'Paste Text' tab instead.")

with tab2:
    st.write("**Copy and paste the complete job description:**")
    st.text_area("Job Description:", height=300, key="jd_text")

# Get the current JD text after tabs
jd_text = st.session_state.jd_text

# Generate Resume Button
if jd_text and len(jd_text) > 100:
    st.write("---")
    
    if st.button("🚀 Generate Tailored Resume", type="primary", use_container_width=True):
        
        # Step 1: Analyze JD
        with st.spinner("🤖 AI is analyzing the job description..."):
            analysis_result = analyze_job_description(jd_text)
        
        if not analysis_result['success']:
            st.error(f"❌ Error analyzing job: {analysis_result['error']}")
            st.stop()
        
        jd_analysis = analysis_result['data']
        
        st.success("✅ Job analysis complete!")
        
        # Display Analysis
        st.write("---")
        st.header("📊 Job Analysis Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Role Information")
            st.write(f"**Position:** {jd_analysis.get('role_type', 'N/A')}")
            st.write(f"**Level:** {jd_analysis.get('seniority_level', 'N/A')}")
            
            st.subheader("✅ Required Skills")
            for skill in jd_analysis.get('required_skills', [])[:10]:
                st.write(f"• {skill}")
        
        with col2:
            st.subheader("⭐ Nice-to-Have Skills")
            for skill in jd_analysis.get('nice_to_have_skills', [])[:10]:
                st.write(f"• {skill}")
        
        # Calculate Match Score
        with st.spinner("🎯 Calculating your match score..."):
            match_details = calculate_match_score(profile, jd_analysis)
        
        st.write("---")
        st.header("🎯 Your Match Score")
        
        score = match_details['score']
        
        # Display score with color
        if score >= 80:
            st.success(f"# {score}% - Excellent Match! 🎉")
        elif score >= 60:
            st.warning(f"# {score}% - Good Match! 👍")
        else:
            st.info(f"# {score}% - Moderate Match")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Your Matching Skills")
            for skill in match_details['matched_skills'][:15]:
                st.write(f"✅ {skill}")
        
        with col2:
            st.subheader("⚠️ Missing Skills")
            if match_details['missing_skills']:
                for skill in match_details['missing_skills'][:10]:
                    st.write(f"⚠️ {skill}")
            else:
                st.write("🎉 You have all required skills!")
        
        # Generate Tailored Summary
        st.write("---")
        st.header("📝 Tailored Professional Summary")
        
        with st.spinner("✨ Generating tailored summary..."):
            tailored_summary = generate_tailored_summary(profile, jd_analysis)
        
        st.info(tailored_summary)
        
        # Resume Preview
        st.write("---")
        st.header("📄 Resume Preview")
        
        st.write("### Professional Summary")
        st.write(tailored_summary)
        
        st.write("### Skills")
        # Reorder skills to match job
        all_user_skills = profile.get('skills', {}).get('technical', [])
        matched_skills = [s for s in all_user_skills if s.lower() in [m.lower() for m in match_details['matched_skills']]]
        other_skills = [s for s in all_user_skills if s not in matched_skills]
        ordered_skills = matched_skills + other_skills
        
        st.write(", ".join(ordered_skills[:15]))
        
        st.write("### Experience")
        for exp in profile.get('experience', [])[:3]:
            st.write(f"**{exp['role']}** at {exp['company']} | {exp['duration']}")
            for resp in exp.get('responsibilities', [])[:3]:
                st.write(f"• {resp}")
        
        st.write("### Projects")
        for proj in profile.get('projects', [])[:3]:
            st.write(f"**{proj['name']}**")
            st.write(proj['description'])
            st.write(f"*Technologies: {', '.join(proj['tech_stack'])}*")
        
        st.write("### Education")
        for edu in profile.get('education', []):
            st.write(f"**{edu['degree']}** - {edu['institution']} ({edu['year']})")
        
        st.write("---")
        
        # Optimize content for resume
        from utils.ai_analyzer import select_best_projects, optimize_experience_bullets
        
        # Select best matching projects
        selected_projects = select_best_projects(profile, jd_analysis, max_projects=3)
        
        # Optimize experience bullets with keywords
        jd_keywords = jd_analysis.get('keywords', []) + jd_analysis.get('required_skills', [])
        optimized_experiences = optimize_experience_bullets(profile.get('experience', []), jd_keywords, max_bullets=3)
        
        # Generate DOCX
        st.header("📥 Download Your Resume")
        
        # Import the builder
        from utils.docx_builder import create_resume_docx
        
        with st.spinner("📝 Creating your resume document..."):
            resume_file = create_resume_docx(profile, jd_analysis, tailored_summary, match_details, selected_projects, optimized_experiences)
        
        # Company name for filename
        company_name = jd_analysis.get('role_type', 'job').replace(' ', '_')
        filename = f"resume_{company_name}_{profile['personal']['name'].replace(' ', '_')}.docx"
        
        # Download button
        st.download_button(
            label="📥 Download Resume (DOCX)",
            data=resume_file,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
            type="primary"
        )
        
        st.success("🎉 Your tailored resume is ready! Click the button above to download.")
        st.balloons()

else:
    st.info("👆 Paste a job URL or description above to get started!")
