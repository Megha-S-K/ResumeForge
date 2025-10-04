"""
ResumeForge AI - Style Loader
Loads custom CSS for premium UI experience
"""

import streamlit as st


def local_css(file_name):
    """Load local CSS file and inject into Streamlit app"""
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"⚠️ CSS file '{file_name}' not found. Please ensure style.css is in the same directory.")
    except Exception as e:
        st.error(f"⚠️ Error loading CSS: {e}")


def inject_custom_components():
    """Inject custom HTML components for enhanced UI"""
    
    # Add custom meta tags for better appearance
    st.markdown("""
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="theme-color" content="#667eea">
    """, unsafe_allow_html=True)
    
    # Add custom font imports (backup in case CSS import fails)
    st.markdown("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Sora:wght@400;600;700;800&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)


def create_hero_section(title, subtitle, emoji="🚀"):
    """Create a beautiful hero section"""
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{emoji}</div>
            <h1 style="
                color: white;
                font-size: 3rem;
                font-weight: 900;
                margin: 0;
                text-shadow: 0 2px 10px rgba(0,0,0,0.2);
            ">{title}</h1>
            <p style="
                color: rgba(255, 255, 255, 0.9);
                font-size: 1.25rem;
                margin-top: 1rem;
                font-weight: 400;
            ">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


def create_feature_card(icon, title, description):
    """Create a feature card with icon"""
    st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 16px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            height: 100%;
        " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 24px rgba(102, 126, 234, 0.2)';" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
            <h3 style="
                color: #f8fafc;
                font-weight: 700;
                margin-bottom: 0.5rem;
            ">{title}</h3>
            <p style="
                color: #cbd5e1;
                line-height: 1.6;
            ">{description}</p>
        </div>
    """, unsafe_allow_html=True)


def create_stat_card(value, label, color="gradient"):
    """Create a statistic card"""
    if color == "gradient":
        bg = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    elif color == "green":
        bg = "linear-gradient(135deg, #10b981 0%, #059669 100%)"
    elif color == "blue":
        bg = "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)"
    else:
        bg = "rgba(255, 255, 255, 0.05)"
    
    st.markdown(f"""
        <div style="
            background: {bg};
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        ">
            <div style="
                font-size: 3rem;
                font-weight: 800;
                color: white;
                margin-bottom: 0.5rem;
            ">{value}</div>
            <div style="
                color: rgba(255, 255, 255, 0.9);
                font-weight: 600;
                text-transform: uppercase;
                font-size: 0.875rem;
                letter-spacing: 0.05em;
            ">{label}</div>
        </div>
    """, unsafe_allow_html=True)


def create_badge(text, color="purple"):
    """Create a colored badge"""
    colors = {
        "purple": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "green": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
        "blue": "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
        "orange": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
        "red": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
    }
    
    bg = colors.get(color, colors["purple"])
    
    st.markdown(f"""
        <span style="
            display: inline-block;
            background: {bg};
            color: white;
            padding: 0.375rem 1rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 600;
            margin: 0.25rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        ">{text}</span>
    """, unsafe_allow_html=True)


def create_progress_bar(percentage, label="", color="purple"):
    """Create a custom progress bar"""
    colors = {
        "purple": "linear-gradient(90deg, #667eea 0%, #764ba2 100%)",
        "green": "linear-gradient(90deg, #10b981 0%, #059669 100%)",
        "blue": "linear-gradient(90deg, #3b82f6 0%, #2563eb 100%)",
    }
    
    bg = colors.get(color, colors["purple"])
    
    st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="
                display: flex;
                justify-content: space-between;
                margin-bottom: 0.5rem;
                color: #f8fafc;
                font-weight: 600;
            ">
                <span>{label}</span>
                <span>{percentage}%</span>
            </div>
            <div style="
                background: rgba(255, 255, 255, 0.1);
                border-radius: 9999px;
                height: 8px;
                overflow: hidden;
            ">
                <div style="
                    width: {percentage}%;
                    height: 100%;
                    background: {bg};
                    border-radius: 9999px;
                    transition: width 0.5s ease;
                "></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def add_separator(style="gradient"):
    """Add a decorative separator"""
    if style == "gradient":
        st.markdown("""
            <div style="
                height: 2px;
                background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
                margin: 2rem 0;
                border-radius: 9999px;
            "></div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="
                height: 1px;
                background: rgba(148, 163, 184, 0.2);
                margin: 2rem 0;
            "></div>
        """, unsafe_allow_html=True)


def create_info_box(title, content, icon="ℹ️", color="blue"):
    """Create an information box"""
    colors = {
        "blue": ("rgba(59, 130, 246, 0.1)", "#3b82f6"),
        "green": ("rgba(16, 185, 129, 0.1)", "#10b981"),
        "yellow": ("rgba(245, 158, 11, 0.1)", "#f59e0b"),
        "red": ("rgba(239, 68, 68, 0.1)", "#ef4444"),
        "purple": ("rgba(139, 92, 246, 0.1)", "#8b5cf6"),
    }
    
    bg_color, border_color = colors.get(color, colors["blue"])
    
    st.markdown(f"""
        <div style="
            background: {bg_color};
            border-left: 4px solid {border_color};
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
        ">
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 1rem;
            ">
                <div style="font-size: 2rem;">{icon}</div>
                <div>
                    <h4 style="
                        color: #f8fafc;
                        font-weight: 700;
                        margin-bottom: 0.5rem;
                    ">{title}</h4>
                    <p style="
                        color: #cbd5e1;
                        line-height: 1.6;
                        margin: 0;
                    ">{content}</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def create_loading_animation():
    """Create a custom loading animation"""
    st.markdown("""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2rem;
        ">
            <div style="
                width: 50px;
                height: 50px;
                border: 4px solid rgba(102, 126, 234, 0.3);
                border-top-color: #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            "></div>
        </div>
        <style>
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
    """, unsafe_allow_html=True)


# Export all functions for easy import
__all__ = [
    'local_css',
    'inject_custom_components',
    'create_hero_section',
    'create_feature_card',
    'create_stat_card',
    'create_badge',
    'create_progress_bar',
    'add_separator',
    'create_info_box',
    'create_loading_animation',
]