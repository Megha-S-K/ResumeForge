import json
import os
from datetime import datetime
import streamlit as st
import json
import os
from datetime import datetime
from style import local_css, inject_custom_components
#from sidebar_nav import render_sidebar, show_profile_status


# Page configuration
st.set_page_config(
    page_title="Build Profile - ResumeForge AI",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
local_css("style.css")
inject_custom_components()

# Page header
st.markdown("""
    <div style="text-align: center; margin: 1rem 0;">
        <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">📝</div>
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
        Build Your Complete Profile
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
    <p style="
        text-align: center;
        font-size: 1.125rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    ">
        Your information is automatically saved as you type! ✨
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# Create data folder
if not os.path.exists('data'):
    os.makedirs('data')

# Load profile from file
def load_profile():
    try:
        with open('data/user_profile.json', 'r') as f:
            return json.load(f)
    except:
        return {
            'personal': {},
            'experience': [],
            'projects': [],
            'skills': {'technical': [], 'soft': []},
            'education': [],
            'certifications': []
        }

# Save profile to file
def save_profile(profile_data):
    try:
        profile_data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('data/user_profile.json', 'w') as f:
            json.dump(profile_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving: {e}")
        return False

# Initialize with saved data
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = load_profile()

# Auto-save function
def auto_save():
    save_profile(st.session_state.profile_data)

# ==================== PERSONAL INFORMATION ====================
st.header("👤 Personal Information")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Full Name *", 
                        value=st.session_state.profile_data.get('personal', {}).get('name', ''),
                        key="name_input")
    email = st.text_input("Email *", 
                        value=st.session_state.profile_data.get('personal', {}).get('email', ''),
                        key="email_input")

with col2:
    phone = st.text_input("Phone", 
                        value=st.session_state.profile_data.get('personal', {}).get('phone', ''),
                        key="phone_input")
    linkedin = st.text_input("LinkedIn", 
                             value=st.session_state.profile_data.get('personal', {}).get('linkedin', ''),
                             key="linkedin_input")

location = st.text_input("Location", 
                         value=st.session_state.profile_data.get('personal', {}).get('location', ''),
                         key="location_input")

summary = st.text_area("Professional Summary", 
                       value=st.session_state.profile_data.get('personal', {}).get('summary', ''),
                       height=120,
                       key="summary_input")

# Auto-save personal info
st.session_state.profile_data['personal'] = {
    'name': name, 'email': email, 'phone': phone,
    'linkedin': linkedin, 'location': location, 'summary': summary
}

st.write("---")

# ==================== WORK EXPERIENCE ====================
st.header("💼 Work Experience")
st.caption("Leave empty if you're a fresher - this section won't appear in your resume")

# Edit mode tracking
if 'editing_exp' not in st.session_state:
    st.session_state.editing_exp = None

# Display existing experiences
for idx, exp in enumerate(st.session_state.profile_data.get('experience', [])):
    if st.session_state.editing_exp == idx:
        # Edit mode
        with st.container():
            st.subheader(f"✏️ Editing Experience #{idx + 1}")
            col1, col2 = st.columns(2)
            with col1:
                edit_company = st.text_input("Company", value=exp.get('company', ''), key=f"edit_exp_comp_{idx}")
                edit_role = st.text_input("Role", value=exp.get('role', ''), key=f"edit_exp_role_{idx}")
            with col2:
                edit_duration = st.text_input("Duration", value=exp.get('duration', ''), key=f"edit_exp_dur_{idx}")
            
            edit_resp = st.text_area("Responsibilities (one per line)", 
                                     value='\n'.join(exp.get('responsibilities', [])),
                                     height=150,
                                     key=f"edit_exp_resp_{idx}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Changes", key=f"save_exp_{idx}", type="primary"):
                    st.session_state.profile_data['experience'][idx] = {
                        'company': edit_company,
                        'role': edit_role,
                        'duration': edit_duration,
                        'responsibilities': [r.strip() for r in edit_resp.split('\n') if r.strip()]
                    }
                    auto_save()
                    st.session_state.editing_exp = None
                    st.rerun()
            with col2:
                if st.button("❌ Cancel", key=f"cancel_exp_{idx}"):
                    st.session_state.editing_exp = None
                    st.rerun()
    else:
        # View mode
        with st.expander(f"📍 {exp.get('role', 'Role')} at {exp.get('company', 'Company')}", expanded=False):
            st.write(f"**Duration:** {exp.get('duration', 'N/A')}")
            st.write("**Responsibilities:**")
            for resp in exp.get('responsibilities', []):
                st.write(f"• {resp}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Edit", key=f"edit_btn_exp_{idx}"):
                    st.session_state.editing_exp = idx
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"del_exp_{idx}"):
                    st.session_state.profile_data['experience'].pop(idx)
                    auto_save()
                    st.rerun()

# Add new experience
if st.session_state.editing_exp is None:
    with st.expander("➕ Add New Experience", expanded=False):
        with st.form("add_experience_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_company = st.text_input("Company")
                new_role = st.text_input("Role")
            with col2:
                new_duration = st.text_input("Duration", placeholder="Jan 2023 - Present")
            
            new_resp = st.text_area("Responsibilities (one per line)", height=120,
                                    placeholder="• Led team of 5 engineers\n• Increased efficiency by 40%")
            
            if st.form_submit_button("➕ Add Experience", type="primary"):
                if new_company and new_role:
                    st.session_state.profile_data['experience'].append({
                        'company': new_company,
                        'role': new_role,
                        'duration': new_duration,
                        'responsibilities': [r.strip() for r in new_resp.split('\n') if r.strip()]
                    })
                    auto_save()
                    st.success("✅ Added!")
                    st.rerun()

st.write("---")

# ==================== PROJECTS ====================
st.header("🚀 Projects")

if 'editing_proj' not in st.session_state:
    st.session_state.editing_proj = None

for idx, proj in enumerate(st.session_state.profile_data.get('projects', [])):
    if st.session_state.editing_proj == idx:
        with st.container():
            st.subheader(f"✏️ Editing Project #{idx + 1}")
            edit_pname = st.text_input("Project Name", value=proj.get('name', ''), key=f"edit_proj_name_{idx}")
            edit_pdesc = st.text_area("Description", value=proj.get('description', ''), height=100, key=f"edit_proj_desc_{idx}")
            edit_ptech = st.text_input("Tech Stack (comma-separated)", value=', '.join(proj.get('tech_stack', [])), key=f"edit_proj_tech_{idx}")
            edit_pgit = st.text_input("GitHub (optional)", value=proj.get('github', ''), key=f"edit_proj_git_{idx}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save", key=f"save_proj_{idx}", type="primary"):
                    st.session_state.profile_data['projects'][idx] = {
                        'name': edit_pname,
                        'description': edit_pdesc,
                        'tech_stack': [t.strip() for t in edit_ptech.split(',') if t.strip()],
                        'github': edit_pgit
                    }
                    auto_save()
                    st.session_state.editing_proj = None
                    st.rerun()
            with col2:
                if st.button("❌ Cancel", key=f"cancel_proj_{idx}"):
                    st.session_state.editing_proj = None
                    st.rerun()
    else:
        with st.expander(f"🔧 {proj.get('name', 'Project')}", expanded=False):
            st.write(f"**Description:** {proj.get('description', 'N/A')}")
            st.write(f"**Tech:** {', '.join(proj.get('tech_stack', []))}")
            if proj.get('github'):
                st.write(f"**GitHub:** {proj.get('github')}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Edit", key=f"edit_btn_proj_{idx}"):
                    st.session_state.editing_proj = idx
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"del_proj_{idx}"):
                    st.session_state.profile_data['projects'].pop(idx)
                    auto_save()
                    st.rerun()

if st.session_state.editing_proj is None:
    with st.expander("➕ Add New Project", expanded=False):
        with st.form("add_project_form", clear_on_submit=True):
            new_pname = st.text_input("Project Name")
            new_pdesc = st.text_area("Description", height=100)
            new_ptech = st.text_input("Tech Stack (comma-separated)", placeholder="React, Node.js, MongoDB")
            new_pgit = st.text_input("GitHub Link (optional)")
            
            if st.form_submit_button("➕ Add Project", type="primary"):
                if new_pname and new_pdesc:
                    st.session_state.profile_data['projects'].append({
                        'name': new_pname,
                        'description': new_pdesc,
                        'tech_stack': [t.strip() for t in new_ptech.split(',') if t.strip()],
                        'github': new_pgit
                    })
                    auto_save()
                    st.success("✅ Added!")
                    st.rerun()

st.write("---")

# ==================== SKILLS ====================
st.header("🎯 Skills")

col1, col2 = st.columns(2)
with col1:
    st.subheader("💻 Technical")
    tech_skills = st.text_area("Comma-separated",
                                value=', '.join(st.session_state.profile_data.get('skills', {}).get('technical', [])),
                                height=100,
                                key="tech_skills_input")

with col2:
    st.subheader("🤝 Soft")
    soft_skills = st.text_area("Comma-separated",
                               value=', '.join(st.session_state.profile_data.get('skills', {}).get('soft', [])),
                               height=100,
                               key="soft_skills_input")

st.session_state.profile_data['skills'] = {
    'technical': [s.strip() for s in tech_skills.split(',') if s.strip()],
    'soft': [s.strip() for s in soft_skills.split(',') if s.strip()]
}

st.write("---")

# ==================== EDUCATION ====================
st.header("🎓 Education")

if 'editing_edu' not in st.session_state:
    st.session_state.editing_edu = None

for idx, edu in enumerate(st.session_state.profile_data.get('education', [])):
    if st.session_state.editing_edu == idx:
        with st.container():
            st.subheader(f"✏️ Editing Education #{idx + 1}")
            col1, col2 = st.columns(2)
            with col1:
                edit_degree = st.text_input("Degree", value=edu.get('degree', ''), key=f"edit_edu_deg_{idx}")
                edit_inst = st.text_input("Institution", value=edu.get('institution', ''), key=f"edit_edu_inst_{idx}")
            with col2:
                edit_year = st.text_input("Year", value=edu.get('year', ''), key=f"edit_edu_year_{idx}")
                edit_gpa = st.text_input("GPA", value=edu.get('gpa', ''), key=f"edit_edu_gpa_{idx}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save", key=f"save_edu_{idx}", type="primary"):
                    st.session_state.profile_data['education'][idx] = {
                        'degree': edit_degree, 'institution': edit_inst,
                        'year': edit_year, 'gpa': edit_gpa
                    }
                    auto_save()
                    st.session_state.editing_edu = None
                    st.rerun()
            with col2:
                if st.button("❌ Cancel", key=f"cancel_edu_{idx}"):
                    st.session_state.editing_edu = None
                    st.rerun()
    else:
        with st.expander(f"🎓 {edu.get('degree', 'Degree')}", expanded=False):
            st.write(f"**Institution:** {edu.get('institution', 'N/A')}")
            st.write(f"**Year:** {edu.get('year', 'N/A')}")
            if edu.get('gpa'):
                st.write(f"**GPA:** {edu.get('gpa')}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Edit", key=f"edit_btn_edu_{idx}"):
                    st.session_state.editing_edu = idx
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"del_edu_{idx}"):
                    st.session_state.profile_data['education'].pop(idx)
                    auto_save()
                    st.rerun()

if st.session_state.editing_edu is None:
    with st.expander("➕ Add Education", expanded=False):
        with st.form("add_education_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_degree = st.text_input("Degree")
                new_inst = st.text_input("Institution")
            with col2:
                new_year = st.text_input("Year")
                new_gpa = st.text_input("GPA (optional)")
            
            if st.form_submit_button("➕ Add", type="primary"):
                if new_degree and new_inst:
                    st.session_state.profile_data['education'].append({
                        'degree': new_degree, 'institution': new_inst,
                        'year': new_year, 'gpa': new_gpa
                    })
                    auto_save()
                    st.success("✅ Added!")
                    st.rerun()

st.write("---")

# ==================== CERTIFICATIONS ====================
st.header("🏆 Certifications")
st.caption("Leave empty if none - this section won't appear in your resume")

if 'editing_cert' not in st.session_state:
    st.session_state.editing_cert = None

for idx, cert in enumerate(st.session_state.profile_data.get('certifications', [])):
    if st.session_state.editing_cert == idx:
        with st.container():
            st.subheader(f"✏️ Editing Certification #{idx + 1}")
            col1, col2 = st.columns(2)
            with col1:
                edit_cname = st.text_input("Name", value=cert.get('name', ''), key=f"edit_cert_name_{idx}")
                edit_cissuer = st.text_input("Issuer", value=cert.get('issuer', ''), key=f"edit_cert_issuer_{idx}")
            with col2:
                edit_cyear = st.text_input("Year", value=cert.get('year', ''), key=f"edit_cert_year_{idx}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save", key=f"save_cert_{idx}", type="primary"):
                    st.session_state.profile_data['certifications'][idx] = {
                        'name': edit_cname, 'issuer': edit_cissuer, 'year': edit_cyear
                    }
                    auto_save()
                    st.session_state.editing_cert = None
                    st.rerun()
            with col2:
                if st.button("❌ Cancel", key=f"cancel_cert_{idx}"):
                    st.session_state.editing_cert = None
                    st.rerun()
    else:
        with st.expander(f"🏆 {cert.get('name', 'Certification')}", expanded=False):
            st.write(f"**Issuer:** {cert.get('issuer', 'N/A')}")
            st.write(f"**Year:** {cert.get('year', 'N/A')}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Edit", key=f"edit_btn_cert_{idx}"):
                    st.session_state.editing_cert = idx
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"del_cert_{idx}"):
                    st.session_state.profile_data['certifications'].pop(idx)
                    auto_save()
                    st.rerun()

if st.session_state.editing_cert is None:
    with st.expander("➕ Add Certification", expanded=False):
        with st.form("add_cert_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_cname = st.text_input("Certification Name")
                new_cissuer = st.text_input("Issuer")
            with col2:
                new_cyear = st.text_input("Year")
            
            if st.form_submit_button("➕ Add", type="primary"):
                if new_cname and new_cissuer:
                    st.session_state.profile_data['certifications'].append({
                        'name': new_cname, 'issuer': new_cissuer, 'year': new_cyear
                    })
                    auto_save()
                    st.success("✅ Added!")
                    st.rerun()
# Auto-save on any change
auto_save()

st.write("---")
st.success("✅ Profile auto-saved!")
st.info("💡 Your data is automatically saved. Go to **Generate Resume** when ready!")

# Clear All Data Option
st.write("---")
st.subheader("⚠️ Danger Zone")

with st.expander("🗑️ Clear All Data", expanded=False):
    st.warning("⚠️ **Warning:** This will permanently delete ALL your profile data. This action cannot be undone!")
    
    # Confirmation checkbox
    confirm_clear = st.checkbox("I understand that all my data will be permanently deleted")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🗑️ Clear Everything", type="secondary", disabled=not confirm_clear, use_container_width=True):
            # Reset to empty profile
            st.session_state.profile_data = {
                'personal': {},
                'experience': [],
                'projects': [],
                'skills': {'technical': [], 'soft': []},
                'education': [],
                'certifications': []
            }
            
            # Delete the saved file
            try:
                if os.path.exists('data/user_profile.json'):
                    os.remove('data/user_profile.json')
            except:
                pass
            
            st.success("✅ All data cleared!")
            st.rerun()
if st.button("Add Job description", type="primary", use_container_width=True, key="generate_btn"):
    st.switch_page("pages/2_🎯_Generate_Resume.py")


# Footer
st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)