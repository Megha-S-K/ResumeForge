# 🧠 ResumeForge AI

> Transform your job search from hours of manual work to seconds of **AI-powered automation.**

**ResumeForge AI** generates perfectly tailored, ATS-optimized resumes using cutting-edge AI technology.

Every one of us has faced the frustration of manually tweaking resumes for each company instead of focusing on interview prep.  
This project was built to **help graduates and job seekers** instantly generate **personalized, job-specific resumes** using AI.

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [AI Integration](#-ai-integration)
- [Design Philosophy](#-design-philosophy)

---

## 🎯 Overview

### ❌ The Problem
- Job seekers spend **2–3 hours** customizing resumes for each job.
- **75% of resumes** are rejected by ATS (Applicant Tracking Systems) due to poor keyword matching.
- Many candidates don’t know **which skills or experiences** to emphasize.

### ✅ The Solution
**ResumeForge AI** uses **Cerebras Cloud** and **Meta’s Llama 3** models to:
- Analyze job descriptions in seconds  
- Generate tailored professional summaries  
- Recommend missing critical skills  
- Select the most relevant projects and experiences  
- Produce ATS-optimized, visually appealing resumes  

### ⚡ The Result
- **30 seconds** instead of 2–3 hours per resume  
- **75–90% ATS match score** (vs 40–50% for generic resumes)  
- **Beautiful, one-page** professional resumes ready for top MNCs  

---

## ✨ Key Features

### 🤖 AI-Powered Intelligence
- **Smart Job Analysis** – Extracts skills and keywords from job postings.  
- **Skill Recommendations** – Suggests missing skills to improve your ATS score.  
- **Context-Aware Generation** – Customizes each section based on job context.  
- **Relevance Scoring** – Picks the most impactful projects and experiences.

### 📝 Professional Resume Builder
- **One-Time Profile Setup** – Enter once, reuse forever.  
- **Auto-Save** – All inputs saved automatically.  
- **CRUD Operations** – Edit or delete any section easily.  
- **Dynamic Sections** – Hides empty fields (e.g., no “Work Experience” for freshers).

### 🎨 Beautiful Output
- **Modern Design** – Professional sidebar layout with gradient styling.  
- **ATS-Friendly Format** – Passes screening bots effortlessly.  
- **Live Preview** – View your resume before downloading.  
- **Multiple Formats** – Export as **PDF** or **DOCX**.  
- **One-Page Optimization** – AI intelligently shortens and formats content.

### ⚡ Lightning Fast
- **5–7 seconds** per generation using **Cerebras Cloud** (1000× faster than GPUs).  
- **Real-Time Updates** – Immediate skill edits and regeneration.  
- **Smooth UX** – No lag, no load screens.

---

## 🛠️ Tech Stack

### 🎨 Frontend
- **Streamlit** – Modern Python web framework  
- **Custom CSS** – Glassmorphic dark theme with responsive design  
- **HTML/CSS** – Professionally formatted resume templates  

### ⚙️ Backend
- **Python 3.10+** – Core logic and orchestration  
- **Cerebras Cloud SDK** – Ultra-fast AI inference  
- **Meta Llama 3.1 (8B & 70B)** – Natural language understanding and generation  

### 🧠 AI & Processing
- **Trafilatura** – Extracts job text from URLs  
- **BeautifulSoup4** – HTML parsing  
- **pdfkit / WeasyPrint** – PDF generation  
- **python-docx** – DOCX creation  

### 💾 Data & Storage
- **JSON** – Local user profile storage  
- **python-dotenv** – Environment management  

---

## 📖 Usage

### 1️⃣ Build Your Profile
Go to **📝 Profile Builder**  
- Enter personal info (name, email, phone, LinkedIn)  
- Add work experience and projects  
- List technical and soft skills  
- Add education and certifications  

🪄 *All data saves automatically as you type!*

---

### 2️⃣ Generate a Tailored Resume
Go to **🎯 Generate Resume**  
- Paste a job posting **URL** or **job description text**  
- Click **Generate Resume**

---

### 3️⃣ Review AI Analysis
View AI-powered insights:
- ✅ Match Score (0–100%)  
- 🧩 Matching Skills  
- ⚠️ Missing Skills  
- 💡 AI-Recommended Additions  

---

### 4️⃣ Improve Your Resume
- Add recommended skills you actually have  
- Click **Update Profile & Regenerate**  
- Watch your **ATS score** increase!

---

### 5️⃣ Download
- Preview in browser  
- Download as **PDF (professional)** or **DOCX (ATS-ready)**  
- Apply confidently to your dream jobs!

---

## 📁 Project Structure

```bash
resume-forge-ai/
│
├── app.py                     # Main Streamlit app
│
├── pages/
│   ├── 1_📝_Profile_Builder.py   # Profile creation page
│   └── 2_🎯_Generate_Resume.py    # Resume generation interface
│
├── utils/
│   ├── __init__.py
│   ├── profile_manager.py      # Save/load profiles
│   ├── url_extractor.py        # Extract JD from URLs
│   ├── ai_analyzer.py          # Cerebras + Llama logic
│   ├── html_resume_builder.py  # HTML resume template
│   └── docx_builder.py         # DOCX generation
│
├── data/
│   └── user_profile.json       # Local storage
│
├── .streamlit/
│   ├── config.toml             # Theme configuration
│   └── style.css               # Custom CSS
│
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container config
├── .env.example                # Environment template
├── .gitignore
└── README.md                   # Documentation
```

---

## 🧩 How It Works

### 1️⃣ Job Analysis
- User pastes job URL or text.
- Trafilatura cleans and extracts text.
- Llama 3.1 (8B) identifies:
  - Required & optional skills
  -Role type & seniority
  -Key responsibilities
  -ATS keywords

### 2️⃣ Profile Matching
- Compares user data with job requirements
- Calculates Match Score (0–100%)
- Highlights skill gaps and recommends improvements

### 3️⃣ Content Selection
- AI ranks projects by relevance
- Picks top 3 projects
- Optimizes bullet points with job keywords
- Reorders skills and experience intelligently

### 4️⃣ Resume Generation
- AI drafts a tailored summary
- html_resume_builder.py renders modern layout
- pdfkit → PDF
- python-docx → ATS-friendly DOCX

### 5️⃣ Output
- Live preview in Streamlit
- Download options: PDF / DOCX
- Quick iteration supported

---

## 🤖 AI Integration
⚡ Cerebras Cloud + Meta Llama 3.1

### Why Cerebras?
🚀 1000× faster inference
⚡ 5–7 sec processing (vs 30+ sec standard)
🔒 Stable performance under heavy load
💸 Free tier for dev & MVP testing

#### Llama 3.1 Used For:

- Job description analysis
- Summary & keyword generation
- Skill recommendation
- Project relevance scoring

---

## 🎨 Design Philosophy

### 🧭 User Experience Principles

Speed First: Instant interactions
Smart Defaults: Minimal typing, maximum AI help
Visual Feedback: Clear process visibility
Progressive Disclosure: Simplicity first, depth later
Error Recovery: Smooth fallback for failed API calls

### 🧾 Resume Design Principles

ATS-Friendly: Clean, parseable structure
One Page: Prioritized content
Professional: Modern, balanced visuals
Scannable: Recruiter-friendly layout
Dynamic: Hide unused sections automatically

---

##### Demo video : https://youtu.be/0rACAOkFXTQ?si=SRI_YMM9ZI_iTdrI
