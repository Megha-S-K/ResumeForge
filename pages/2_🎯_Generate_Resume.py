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

# Initialize generation session state
if 'generated' not in st.session_state:
    st.session_state.generated = False
if 'jd_analysis' not in st.session_state:
    st.session_state.jd_analysis = None
if 'match_details' not in st.session_state:
    st.session_state.match_details = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'selected_skills' not in st.session_state:
    st.session_state.selected_skills = set()
if 'tailored_summary' not in st.session_state:
    st.session_state.tailored_summary = ""

# Generate Resume Button (only active if not generated or after clear)
if jd_text and len(jd_text) > 100:
    st.write("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🚀 Generate Tailored Resume", type="primary", use_container_width=True, disabled=st.session_state.generated):
            st.session_state.generated = True
            
            # Step 1: Analyze JD
            with st.spinner("🤖 AI is analyzing the job description..."):
                analysis_result = analyze_job_description(jd_text)
            
            if not analysis_result['success']:
                st.error(f"❌ Error analyzing job: {analysis_result['error']}")
                st.session_state.generated = False
                st.stop()
            
            st.session_state.jd_analysis = analysis_result['data']
            st.success("✅ Job analysis complete!")
            
            # Calculate Match Score
            with st.spinner("🎯 Calculating your match score..."):
                st.session_state.match_details = calculate_match_score(profile, st.session_state.jd_analysis)
            
            # AI SKILL RECOMMENDATIONS
            with st.spinner("🤖 Analyzing skill gaps..."):
                from utils.ai_analyzer import generate_skill_recommendations
                st.session_state.recommendations = generate_skill_recommendations(profile, st.session_state.jd_analysis)
            
            # Generate Tailored Summary
            with st.spinner("✨ Generating tailored summary..."):
                st.session_state.tailored_summary = generate_tailored_summary(profile, st.session_state.jd_analysis)
            
            # Clear previous selections
            st.session_state.selected_skills = set()
            
            st.rerun()  # Rerun to show persisted UI
    
    # Clear Button (to change JD or restart)
    if st.session_state.generated:
        if st.button("🗑️ Clear & Restart (Change Job)", type="secondary"):
            for key in ['generated', 'jd_analysis', 'match_details', 'recommendations', 'tailored_summary', 'selected_skills']:
                del st.session_state[key]
            st.rerun()

# Render Generated Content (Persisted Across Reruns)
if st.session_state.generated and st.session_state.jd_analysis:
    st.write("---")
    st.info("📊 Resume generated! Interact below to customize skills.")
    
    jd_analysis = st.session_state.jd_analysis
    match_details = st.session_state.match_details
    recommendations = st.session_state.recommendations
    tailored_summary = st.session_state.tailored_summary
    
    # Display Analysis (Aesthetic Layout)
    st.header("📊 Job Analysis Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Role Information")
        st.metric("Position", jd_analysis.get('role_type', 'N/A'))
        st.metric("Level", jd_analysis.get('seniority_level', 'N/A'))
        
        st.subheader("✅ Required Skills")
        for skill in jd_analysis.get('required_skills', [])[:10]:
            st.write(f"• {skill}")
    
    with col2:
        st.subheader("⭐ Nice-to-Have Skills")
        for skill in jd_analysis.get('nice_to_have_skills', [])[:10]:
            st.write(f"• {skill}")
    
    # Match Score
    st.header("🎯 Your Match Score")
    
    score = match_details['score']
    
    # Display score with color and metric for aesthetics
    score_col1, score_col2 = st.columns([1, 3])
    with score_col1:
        if score >= 80:
            st.success(f"#{score}%")
        elif score >= 60:
            st.warning(f"#{score}%")
        else:
            st.info(f"#{score}%")
    with score_col2:
        if score >= 80:
            st.write("Excellent Match! 🎉")
        elif score >= 60:
            st.write("Good Match! 👍")
        else:
            st.write("Moderate Match – Let's improve it!")
    
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
            st.success("🎉 You have all required skills!")
    
    # AI SKILL RECOMMENDATIONS (Interactive and Aesthetic)
    st.header("💡 AI Skill Recommendations")
    
    if recommendations['has_recommendations']:
        st.info("**Boost your match! Select skills from below and update all at once.**")
        
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
        
        # Nice-to-Have Skills Expander
        with st.expander("⭐ Nice-to-Have Skills", expanded=False):
            if recommendations['nice_to_have_missing']:
                cols = st.columns(3)
                for idx, skill in enumerate(recommendations['nice_to_have_missing']):
                    with cols[idx % 3]:
                        is_checked = skill in st.session_state.selected_skills
                        if st.checkbox(f"**{skill}**", value=is_checked, key=f"nice_{idx}"):
                            st.session_state.selected_skills.add(skill)
                        else:
                            st.session_state.selected_skills.discard(skill)
            else:
                st.write("No nice-to-have skills suggested.")
        
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
            st.success(f"**Preview: {len(selected_skills_list)} skill(s) selected across categories**")
            for skill in selected_skills_list:
                st.write(f"✅ {skill}")
        else:
            st.info("👆 Select skills from the expanders above to see a preview.")
        
        st.caption("💡 Tip: Check any combination of skills, then update your profile below. Regenerate to see the impact!")
        
        # Centered Update Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Update Profile with Selected Skills", 
                        type="primary", 
                        use_container_width=True,
                        disabled=len(selected_skills_list) == 0):
                
                # Add selected skills to profile (batch update)
                added_count = 0
                for skill in selected_skills_list:
                    if skill not in profile['skills']['technical']:
                        profile['skills']['technical'].append(skill)
                        added_count += 1
                
                # Save to file
                with open('data/user_profile.json', 'w') as f:
                    json.dump(profile, f, indent=2)
                
                st.success(f"✅ Profile updated! Added {added_count} new skill(s).")
                #st.balloons()
                
                # Clear selections (but keep generated state)
                st.session_state.selected_skills = set()
                
                # Optional Regenerate Button
                if st.button("🔄 Regenerate Resume with Updated Profile", 
                            type="secondary", 
                            use_container_width=True):
                    # Reload profile from file for fresh computation
                    profile = load_profile()
                    # Recompute everything with new profile
                    st.session_state.match_details = calculate_match_score(profile, jd_analysis)
                    st.session_state.recommendations = generate_skill_recommendations(profile, jd_analysis)
                    st.session_state.tailored_summary = generate_tailored_summary(profile, jd_analysis)
                    st.session_state.selected_skills = set()
                    st.rerun()
            else:
                st.info("Select at least one skill to enable update.")
    else:
        st.success("🎉 Your profile already matches this job perfectly! No recommendations needed.")
    
    # Tailored Summary
    st.header("📝 Tailored Professional Summary")
    
    with st.container():
        st.info(tailored_summary)
    
    # Resume Preview (Aesthetic)
    st.header("📄 Resume Preview")
    
    col_preview1, col_preview2 = st.columns(2)
    
    with col_preview1:
        st.subheader("### Professional Summary")
        st.write(tailored_summary)
        
        st.subheader("### Skills")
        # Reorder skills to match job
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
    
    # Optimize content for resume
    from utils.ai_analyzer import select_best_projects, optimize_experience_bullets
    
    # Select best matching projects
    selected_projects = select_best_projects(profile, jd_analysis, max_projects=3)
    
    # Optimize experience bullets with keywords
    jd_keywords = jd_analysis.get('keywords', []) + jd_analysis.get('required_skills', [])
    optimized_experiences = optimize_experience_bullets(profile.get('experience', []), jd_keywords, max_bullets=3)
    
    # Generate Resume
    st.write("---")
    st.header("📥 Your Beautiful Resume")
        
    # Import builders
    from utils.docx_builder import create_resume_docx
    from utils.html_resume_builder import create_html_resume, html_to_pdf
    from utils.ai_analyzer import select_best_projects, optimize_experience_bullets
        
    with st.spinner("✨ Creating your stunning resume..."):
        # Select best projects
        selected_projects = select_best_projects(profile, jd_analysis, max_projects=3)
            
        # Optimize experience bullets
        jd_keywords = jd_analysis.get('keywords', [])
        optimized_experiences = optimize_experience_bullets(
            profile.get('experience', []), 
            jd_keywords, 
            max_bullets=3
        )
            
        # Create HTML resume
        html_resume = create_html_resume(
            profile, 
            jd_analysis, 
            tailored_summary, 
            match_details,
            selected_projects,
            optimized_experiences
        )
        
        st.success("✅ Resume generated successfully!")
        
        # Preview Section
        st.subheader("📄 Live Preview")
        st.info("👀 This is how your resume will look:")
        
        # Show HTML preview in iframe
        import base64
        b64_html = base64.b64encode(html_resume.encode()).decode()
        iframe_html = f'<iframe src="data:text/html;base64,{b64_html}" width="100%" height="800px" style="border: 2px solid #667eea; border-radius: 10px;"></iframe>'
        st.components.v1.html(iframe_html, height=820, scrolling=True)
        
        # Download Buttons
        st.write("---")
        st.subheader("💾 Download Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # PDF Download
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
            # DOCX Download (backup option)
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

else:
    st.info("👆 Paste a job URL or description above to get started!")