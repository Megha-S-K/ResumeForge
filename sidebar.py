# sidebar.py
import streamlit as st

def render_sidebar():
    """Renders the consistent sidebar navigation on any page."""
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
        
        # Navigation buttons (use unique keys to avoid conflicts across pages)
        if st.button("🏠 Home", use_container_width=True, key="nav_home"):
            st.switch_page("app.py")
        
        if st.button("📝 Build Profile", use_container_width=True, key="nav_profile"):
            st.switch_page("pages/profile_builder.py")
        
        if st.button("🎯 Generate Resume", use_container_width=True, key="nav_generate"):
            st.switch_page("pages/generate_resume.py")
        
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
                        margin-top: 0.25rem;
                    ">Powered by Cerebras AI</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
