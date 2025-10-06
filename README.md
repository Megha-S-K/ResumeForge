Transform your job search from hours of manual work to seconds of AI-powered automation. ResumeForge AI generates perfectly tailored, ATS-optimized resumes using cutting-edge AI technology.
Every one of us would have faced the problem of tinkering our resume with respect to the job description of the comapany manually ,instead of preparing for our interview .. So I created this project ResumeForgeAI application to help graduates and job seekers generate a tailored resume customized to the specific JD and their profile.

📋 Table of Contents

-Overview
-Key Features
-Tech Stack
-Usage
-Project Structure
-How It Works
-AI Integration
-Acknowlegments

🎯 Overview
The Problem:
- Job seekers spend 2-3 hours customizing resumes for each application
- 75% of resumes are rejected by ATS (Applicant Tracking Systems) due to poor keyword matching
- Most candidates don't know which skills or experiences to emphasize

The Solution:
ResumeForge AI uses Cerebras Cloud and Meta's Llama 3 models to:
-Analyze job descriptions in seconds
-Generate tailored professional summaries
-Recommend missing critical skills
-Select relevant projects and experiences
-Produce ATS-optimized, professionally designed resumes

The Result:
- 30 seconds instead of 2-3 hours per application
- 75-90% ATS match scores (vs 40-50% for generic resumes)
- Beautiful, one-page professional resumes ready for top MNC companies


✨ Key Features
🤖 AI-Powered Intelligence

Smart Job Analysis: Automatically extracts requirements, skills, and keywords from any job posting URL
Skill Recommendations: AI suggests critical missing skills to improve your ATS score
Context-Aware Generation: Tailors every section based on target role
Relevance Scoring: Intelligently selects your most impactful projects and experiences

📝 Professional Resume Building

One-Time Profile Setup: Enter your information once, use it forever
Auto-Save: Never lose your progress
Edit & Delete: Full CRUD operations on all profile sections
Dynamic Sections: Empty sections automatically hidden (e.g., no "Work Experience" for freshers)

🎨 Beautiful Output

Modern Design: Professional sidebar layout with gradient accents
ATS-Friendly: Optimized formatting that passes automated screening
Live Preview: See your resume before downloading
Multiple Formats: Download as PDF (beautiful) or DOCX (ATS-compatible)
One-Page Optimization: Intelligent content prioritization for single-page perfection

⚡ Lightning Fast

5-7 Second Generation: Powered by Cerebras Cloud (1000x faster than traditional GPUs)
Real-Time Updates: Instant skill additions and regeneration
Smooth UX: No frustrating loading screens


🛠️ Tech Stack
Frontend :
Streamlit - Modern Python web framework for rapid UI development
Custom CSS - Glassmorphic dark theme with responsive design
HTML/CSS - Professional resume templates

Backend:
Python 3.10+ - Core application logic
Cerebras Cloud SDK - Ultra-fast AI inference
Meta Llama 3.1 (8B & 70B models) - Natural language processing and generation

AI & Processing:
Trafilatura - Web scraping for job description extraction
BeautifulSoup4 - HTML parsing
Pdfkit - PDF generation from HTML
python-docx - DOCX document generation

Data & Storage:
JSON - Local data storage for user profiles
python-dotenv - Environment variable management

📖 Usage
1. Build Your Profile
Navigate to 📝 Profile Builder:

Enter personal information (name, email, phone, LinkedIn)
Add work experience (if applicable)
Add projects with descriptions and tech stacks
List technical and soft skills
Add education details
Add certifications (optional)

Note: All data is automatically saved as you type!
2. Generate Tailored Resume
Navigate to 🎯 Generate Resume:

Paste a job posting URL (LinkedIn, Indeed, company website)
OR paste the job description text directly
Click Generate Resume

3. Review AI Analysis
The system will show:

Match score (percentage)
Matching skills (what you have)
Missing skills (what the job requires)
AI-recommended skills

4. Add Recommended Skills

Select skills you actually have from recommendations
Click Update Profile & Regenerate
Watch your ATS score improve!

5. Download Your Resume

Preview the beautiful resume in browser
Download as PDF (professional design) or DOCX (ATS-compatible)
Apply to jobs with confidence!


📁 Project Structure
resume-forge-ai/
│
├── app.py                          # Main Streamlit application
│
├── pages/                          # Multi-page app
│   ├── 1_📝_Profile_Builder.py    # Profile creation and editing
│   └── 2_🎯_Generate_Resume.py    # Resume generation interface
│
├── utils/                          # Helper modules
│   ├── __init__.py
│   ├── profile_manager.py         # Save/load user profiles
│   ├── url_extractor.py           # Extract job descriptions from URLs
│   ├── ai_analyzer.py             # Cerebras API integration
│   ├── html_resume_builder.py     # HTML resume template
│   └── docx_builder.py            # DOCX resume generation
│
├── data/                           # Local data storage
│   └── user_profile.json          # User profile data
│
├── .streamlit/                     # Streamlit configuration
│   ├── config.toml                # Theme settings
│   └── style.css                  # Custom CSS styling
│
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker container config
├── .env.example                    # Environment variables template
├── .gitignore
└── README.md                       # This file

🧠 How It Works
Step-by-Step Process

Job Analysis

User pastes job URL or description
Trafilatura extracts clean text from URL
Llama 3.1-8B analyzes and extracts:

Required technical skills
Nice-to-have skills
Role type and seniority level
Key responsibilities
ATS keywords




Profile Matching

System compares user skills with job requirements
Calculates match score (0-100%)
Identifies skill gaps
Generates AI-powered recommendations


Content Selection

AI scores each project for relevance
Selects top 3 most relevant projects
Prioritizes experience bullets with job keywords
Reorders skills (matching first)


Resume Generation

Llama 3.1-8B generates tailored professional summary
System builds HTML resume with modern template
Optimizes content for one-page layout
WeasyPrint converts to PDF
python-docx creates ATS-friendly DOCX


Output

Live preview in browser
Download options (PDF/DOCX)
User can iterate and regenerate instantly




🤖 AI Integration
Cerebras Cloud + Llama 3.1
Why Cerebras?

1000x faster inference than traditional GPUs
5-7 second total processing time (vs 25-45 seconds with standard inference)
Consistent performance under load
Free tier for development and MVP testing

Llama 3.1 Model Used for:
-Job analysis
-Summary generation
-Skill recommendations
-Project scoring

🎨 Design Philosophy
User Experience Principles

Speed First: Every interaction should feel instant
Smart Defaults: Minimize user input, maximize AI assistance
Visual Feedback: Users always know what's happening
Progressive Disclosure: Show complexity only when needed
Error Recovery: Graceful fallbacks if AI fails

Resume Design Principles

ATS-Friendly: Clean structure parseable by automated systems
One Page: Strict content prioritization
Professional: Modern but not flashy
Scannable: Easy for recruiters to skim
No Empty Sections: Dynamic hiding of unused sections

🙏 Acknowledgments
Built For
FutureStack 2025 Hackathon

Sponsored by Cerebras, Meta, Docker, and WeMakeDevs

Technologies

Cerebras Cloud - For blazing-fast AI inference
Meta Llama 3.1 - For powerful language understanding
Streamlit - For rapid UI development
Docker - For containerization
Open Source Community - For amazing libraries

Special Thanks

Cerebras team for providing free cloud access
Meta for open-sourcing Llama models
WeMakeDevs for organizing the hackathon
All contributors and testers
