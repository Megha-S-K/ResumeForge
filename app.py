"""
ResumeForge AI - Professional Homepage
AI-Powered Resume Builder with Smart Tailoring
"""

import streamlit as st
from style import local_css, inject_custom_components

# Page configuration
st.set_page_config(
    page_title="ResumeForge AI - Smart Resume Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
local_css("style.css")
inject_custom_components()

# Sidebar Navigation
with st.sidebar:
    # Logo and title
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <div style="
                width: 70px;
                height: 70px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1rem auto;
                font-size: 2.5rem;
                box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
            ">📄</div>
            <h2 style="
                font-size: 1.5rem; 
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 800;
            ">ResumeForge AI</h2>
            <p style="
                color: #94a3b8;
                font-size: 0.75rem;
                margin-top: 0.5rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
            ">AI Resume Builder</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation Menu
    st.markdown("""
        <div style="padding: 0.5rem 0 1rem 0;">
            <h3 style="
                font-size: 0.75rem; 
                color: #94a3b8; 
                text-transform: uppercase; 
                letter-spacing: 0.1em; 
                margin-bottom: 1rem;
                font-weight: 600;
            ">📍 NAVIGATION</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1 = st.columns(1)[0]
    
    if st.button("🏠 Home", use_container_width=True, key="nav_home"):
        st.switch_page("app.py")
    
    if st.button("📝 Build Profile", use_container_width=True, key="nav_profile"):
        st.switch_page("pages/1_📝_Profile_Builder.py")
    
    if st.button("🎯 Generate Resume", use_container_width=True, key="nav_generate"):
        st.switch_page("pages/2_🎯_Generate_Resume.py")
    
    st.markdown("---")
    
    # Quick info
    st.markdown("""
        <div style="
            background: rgba(102, 126, 234, 0.1);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
        ">
            <h4 style="
                color: #f8fafc;
                font-size: 0.875rem;
                margin-bottom: 0.5rem;
                font-weight: 600;
            ">💡 Quick Tip</h4>
            <p style="
                color: #cbd5e1;
                font-size: 0.8rem;
                line-height: 1.5;
                margin: 0;
            ">
                Build your profile once, then generate unlimited tailored resumes for different jobs!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Stats
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="margin-bottom: 1rem;">
                <div style="
                    font-size: 1.5rem;
                    font-weight: 800;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                ">Fast & Smart</div>
                <div style="
                    color: #94a3b8;
                    font-size: 0.75rem;
                    
                ">Powered by Cerebras AI</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 5rem; margin-bottom: 1rem; animation: float 3s ease-in-out infinite;">
            📄
        </div>
    </div>
""", unsafe_allow_html=True)

# Main title with gradient
st.markdown("""
    <h1 style="
        text-align: center;
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        line-height: 1.1;
    ">
        ResumeForge AI
    </h1>
""", unsafe_allow_html=True)

# Subtitle/Tagline
st.markdown("""
    <p style="
        text-align: center;
        font-size: 1.5rem;
        color: #cbd5e1;
        margin-bottom: 2rem;
        font-weight: 400;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    ">
        One Profile. Infinite Tailored Resumes. ⚡ Powered by Cerebras AI
    </p>
""", unsafe_allow_html=True)

# Description paragraph
st.markdown("""
    <div style="
        max-width: 900px;
        margin: 0 auto 0rem auto;
        text-align: center;
    ">
        <p style="
            font-size: 1.125rem;
            line-height: 1.8;
            color: #94a3b8;
            margin-bottom: 0.5rem;
        ">
            ResumeForge AI is your intelligent career companion that transforms the way you apply for jobs. 
            Build your comprehensive profile once, then let our advanced AI engine craft perfectly tailored 
            resumes for every opportunity in seconds. Say goodbye to manual customization and hello to 
            interview-winning applications.
        </p>
    </div>
""", unsafe_allow_html=True)

# Call-to-action buttons
st.markdown("""
    <div style="
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    ">
""", unsafe_allow_html=True)


if st.button("🚀 Get Started Now", type="primary", use_container_width=True, key="footer_cta"):
    st.switch_page("pages/1_📝_Profile_Builder.py")
# Create two columns for buttons
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    subcol1, subcol2 = st.columns(2)
    
    with subcol1:
        if st.button("📝 Build Your Profile", type="primary", use_container_width=True, key="build_btn"):
            st.switch_page("pages/1_📝_Profile_Builder.py")
    
    with subcol2:
        if st.button("🎯 Generate Resume", type="primary", use_container_width=True, key="generate_btn"):
            st.switch_page("pages/2_🎯_Generate_Resume.py")
        

st.markdown("</div>", unsafe_allow_html=True)

# Features section
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
    <h2 style="
        text-align: center;
        font-size: 2.5rem;
        color: #f8fafc;
        margin: 4rem 0 3rem 0;
        font-weight: 700;
    ">
        Why Choose ResumeForge AI?
    </h2>
""", unsafe_allow_html=True)

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 16px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            text-align: center;
            transition: all 0.3s ease;
            height: 100%;
        ">
            <div style="
                width: 80px;
                height: 80px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1.5rem auto;
                font-size: 2.5rem;
                box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
            ">⚡</div>
            <h3 style="color: #f8fafc; font-weight: 700; margin-bottom: 1rem; font-size: 1.5rem;">
                Lightning Fast
            </h3>
            <p style="color: #cbd5e1; line-height: 1.7; font-size: 1rem;">
                Generate tailored resumes in seconds, not hours. Our AI processes job descriptions 
                instantly and optimizes your profile automatically.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 16px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            text-align: center;
            transition: all 0.3s ease;
            height: 100%;
        ">
            <div style="
                width: 80px;
                height: 80px;
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1.5rem auto;
                font-size: 2.5rem;
                box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
            ">🎯</div>
            <h3 style="color: #f8fafc; font-weight: 700; margin-bottom: 1rem; font-size: 1.5rem;">
                Smart Tailoring
            </h3>
            <p style="color: #cbd5e1; line-height: 1.7; font-size: 1rem;">
                AI-powered matching that highlights your most relevant skills and experiences 
                for each job application. Beat the ATS every time.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 16px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            text-align: center;
            transition: all 0.3s ease;
            height: 100%;
        ">
            <div style="
                width: 80px;
                height: 80px;
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1.5rem auto;
                font-size: 2.5rem;
                box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
            ">🤖</div>
            <h3 style="color: #f8fafc; font-weight: 700; margin-bottom: 1rem; font-size: 1.5rem;">
                AI-Powered
            </h3>
            <p style="color: #cbd5e1; line-height: 1.7; font-size: 1rem;">
                Leveraging Cerebras AI for intelligent skill recommendations, gap analysis, 
                and professional summary generation. Your personal career advisor.
            </p>
        </div>
    """, unsafe_allow_html=True)

# How it works section
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
    <h2 style="
        text-align: center;
        font-size: 2.5rem;
        color: #f8fafc;
        margin: 4rem 0 3rem 0;
        font-weight: 700;
    ">
        How It Works
    </h2>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem;">
            <div style="
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1rem auto;
                font-size: 1.5rem;
                font-weight: 800;
                color: white;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            ">1</div>
            <h4 style="color: #f8fafc; margin-bottom: 0.75rem; font-size: 1.25rem;">Build Profile</h4>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6;">
                Enter your information once: experience, projects, skills, and education
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem;">
            <div style="
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1rem auto;
                font-size: 1.5rem;
                font-weight: 800;
                color: white;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            ">2</div>
            <h4 style="color: #f8fafc; margin-bottom: 0.75rem; font-size: 1.25rem;">Paste Job</h4>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6;">
                Copy any job description URL or text - our AI extracts key requirements
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem;">
            <div style="
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1rem auto;
                font-size: 1.5rem;
                font-weight: 800;
                color: white;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            ">3</div>
            <h4 style="color: #f8fafc; margin-bottom: 0.75rem; font-size: 1.25rem;">Download</h4>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6;">
                Get your perfectly tailored, ATS-optimized resume in seconds
            </p>
        </div>
    """, unsafe_allow_html=True)

# Stats section
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 3rem 0;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    ">
        <h2 style="
            color: white;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 2rem;
        ">
            Ready to Transform Your Job Search?
        </h2>
        <p style="
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.125rem;
            margin-bottom: 2rem;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        ">
            Join thousands of job seekers who have supercharged their applications 
            with AI-powered resume tailoring. Your dream job is just one click away.
        </p>
    </div>
""", unsafe_allow_html=True)


# Footer
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
    <div style="
        text-align: center;
        padding: 2rem 0;
        border-top: 1px solid rgba(148, 163, 184, 0.2);
        margin-top: 4rem;
    ">
        <p style="color: #64748b; font-size: 0.875rem;">
            Made with ❤️ using Streamlit & Cerebras AI
        </p>
        <p style="color: #64748b; font-size: 0.875rem; margin-top: 0.5rem;">
            © 2025 ResumeForge AI. All rights reserved.
        </p>
    </div>
""", unsafe_allow_html=True)

# Add floating animation keyframes
st.markdown("""
    <style>
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
    </style>
""", unsafe_allow_html=True)