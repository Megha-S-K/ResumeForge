import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="ResumeForge AI",
    page_icon="📄",
    layout="wide"
)

# Main title
st.title("📄 ResumeForge AI")
st.subheader("One Profile. Infinite Tailored Resumes. ⚡ Powered by Cerebras")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    st.write("Welcome to ResumeForge AI!")
    st.write("---")
    st.write("👈 Use the sidebar to navigate between pages")

# Main content
st.write("## 👋 Welcome!")
st.write("This AI-powered platform helps you create perfectly tailored resumes in seconds.")

st.info("🚧 Setup in progress... More features coming soon!")

# Test if everything works
if st.button("Test Button - Click Me! 🎉"):
    st.balloons()
    st.success("✅ Everything is working perfectly!")