import os
from dotenv import load_dotenv
import json

load_dotenv()

try:
    from cerebras.cloud.sdk import Cerebras
    CEREBRAS_AVAILABLE = True
except ImportError:
    CEREBRAS_AVAILABLE = False

def get_cerebras_client():
    api_key = os.getenv('CEREBRAS_API_KEY')
    if not api_key:
        raise ValueError("CEREBRAS_API_KEY not found!")
    if not CEREBRAS_AVAILABLE:
        raise ImportError("Cerebras SDK not installed")
    return Cerebras(api_key=api_key)

def analyze_job_description(jd_text):
    """Analyze job description using Cerebras AI"""
    try:
        client = get_cerebras_client()
        
        prompt = f"""Analyze this job description and extract the following in JSON format:

1. required_skills: List of required technical skills (max 15)
2. nice_to_have_skills: List of nice-to-have skills (max 10)
3. role_type: The job title/role
4. seniority_level: Experience level (Senior/Mid-Level/Junior/Entry Level)
5. key_responsibilities: Main responsibilities (max 5)
6. keywords: Important ATS keywords (max 20)

Job Description:
{jd_text}

Return ONLY valid JSON."""

        response = client.chat.completions.create(
            model="llama3.1-8b",
            messages=[
                {"role": "system", "content": "You are an expert job description analyzer. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        result_text = response.choices[0].message.content
        
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0]
        
        analysis = json.loads(result_text.strip())
        
        return {'success': True, 'data': analysis, 'error': None}
        
    except Exception as e:
        return {'success': False, 'data': None, 'error': str(e)}

def generate_skill_recommendations(user_profile, jd_analysis):
    """
    Recommend skills user should add to improve match score
    Returns: dict with recommendations
    """
    user_skills = set()
    user_skills.update([s.lower() for s in user_profile.get('skills', {}).get('technical', [])])
    user_skills.update([s.lower() for s in user_profile.get('skills', {}).get('soft', [])])
    
    required_skills = set([s.lower() for s in jd_analysis.get('required_skills', [])])
    nice_skills = set([s.lower() for s in jd_analysis.get('nice_to_have_skills', [])])
    
    # Find missing critical skills
    critical_missing = list(required_skills - user_skills)[:5]
    
    # Find missing nice-to-have skills
    nice_missing = list(nice_skills - user_skills)[:5]
    
    # AI-powered recommendations
    try:
        client = get_cerebras_client()
        
        prompt = f"""Based on this job role and the candidate's profile, suggest 3-5 skills they should consider adding to their resume to improve their chances.

Role: {jd_analysis.get('role_type', 'Software Engineer')}
Required Skills: {', '.join(jd_analysis.get('required_skills', [])[:10])}
Candidate's Current Skills: {', '.join(list(user_skills)[:15])}

Consider:
1. Skills commonly expected but not listed
2. Complementary skills to what they already have
3. Industry-standard tools/frameworks

Return as a JSON array of strings (skill names only)."""

        response = client.chat.completions.create(
            model="llama3.1-8b",
            messages=[
                {"role": "system", "content": "You are a career advisor helping candidates improve their resumes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        result = response.choices[0].message.content.strip()
        
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0]
        elif "```" in result:
            result = result.split("```")[1].split("```")[0]
        
        ai_suggestions = json.loads(result)
        
    except:
        ai_suggestions = []
    
    return {
        'critical_missing': critical_missing,
        'nice_to_have_missing': nice_missing,
        'ai_suggestions': ai_suggestions[:5],
        'has_recommendations': len(critical_missing) > 0 or len(nice_missing) > 0
    }
def generate_tailored_summary(user_profile, jd_analysis):
    """Generate professional summary tailored to the job, returning only the summary text."""
    try:
        client = get_cerebras_client()
        
        user_summary = user_profile.get('personal', {}).get('summary', '')
        user_skills = user_profile.get('skills', {})
        role_type = jd_analysis.get('role_type', 'this position')
        required_skills = ', '.join(jd_analysis.get('required_skills', [])[:5])
        
        # Check if fresher (no experience)
        is_fresher = len(user_profile.get('experience', [])) == 0
        
        if is_fresher:
            prompt = f"""Write a professional summary for a FRESHER/RECENT GRADUATE resume (2-3 sentences, max 80 words).
Education: {user_profile.get('education', [{}])[0].get('degree', 'Computer Science') if user_profile.get('education') else 'Computer Science'}
Skills: {', '.join(user_skills.get('technical', [])[:10])}
Target Role: {role_type}
Key Required Skills: {required_skills}

Focus on:
- Academic projects and achievements
- Eagerness to learn and contribute
- Relevant technical skills
- Career aspirations aligned with the role

Respond ONLY with the professional summary text. Do NOT include any explanations or quotes."""
        else:
            prompt = f"""Write a professional summary for an EXPERIENCED PROFESSIONAL resume (2-3 sentences, max 80 words).
Current Summary: {user_summary}
Skills: {', '.join(user_skills.get('technical', [])[:10])}
Target Role: {role_type}
Key Required Skills: {required_skills}

Make it compelling and highlight relevant experience. Focus on achievements and impact.

Respond ONLY with the professional summary text. Do NOT include any explanations or quotes."""
        
        response = client.chat.completions.create(
            model="llama3.1-8b",
            messages=[
                {"role": "system", "content": "You are a professional resume writer. Provide ONLY the professional summary text, no extra commentary."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=150
        )
        
        summary_text = response.choices[0].message.content.strip()
        
        # Optional: Remove surrounding quotes if model adds them
        if summary_text.startswith('"') and summary_text.endswith('"'):
            summary_text = summary_text[1:-1].strip()
        
        return summary_text
        
    except Exception as e:
        # Fallback to existing summary if error occurs
        return user_profile.get('personal', {}).get('summary', '')

def calculate_match_score(user_profile, jd_analysis):
    """Calculate match score and provide details"""
    user_skills = set()
    user_skills.update([s.lower() for s in user_profile.get('skills', {}).get('technical', [])])
    user_skills.update([s.lower() for s in user_profile.get('skills', {}).get('soft', [])])
    
    required_skills = set([s.lower() for s in jd_analysis.get('required_skills', [])])
    nice_skills = set([s.lower() for s in jd_analysis.get('nice_to_have_skills', [])])
    
    matched_required = user_skills & required_skills
    matched_nice = user_skills & nice_skills
    missing_skills = required_skills - user_skills
    
    if required_skills:
        required_score = (len(matched_required) / len(required_skills)) * 70
    else:
        required_score = 70
    
    if nice_skills:
        nice_score = (len(matched_nice) / len(nice_skills)) * 30
    else:
        nice_score = 30
    
    total_score = required_score + nice_score
    
    return {
        'score': round(total_score, 1),
        'matched_skills': list(matched_required | matched_nice),
        'missing_skills': list(missing_skills),
        'match_percentage': f"{round(total_score)}%"
    }

def select_best_projects(user_profile, jd_analysis, max_projects=3):
    """
    Intelligently select most relevant projects for the resume
    """
    projects = user_profile.get('projects', [])
    if not projects:
        return []
    
    required_skills = set([s.lower() for s in jd_analysis.get('required_skills', [])])
    nice_skills = set([s.lower() for s in jd_analysis.get('nice_to_have_skills', [])])
    all_jd_skills = required_skills | nice_skills
    
    # Score each project
    scored_projects = []
    for proj in projects:
        tech_stack = set([t.lower() for t in proj.get('tech_stack', [])])
        
        # Count matching skills
        matches = len(tech_stack & all_jd_skills)
        required_matches = len(tech_stack & required_skills)
        
        # Score: required matches worth more
        score = (required_matches * 3) + matches
        
        scored_projects.append((proj, score))
    
    # Sort by score and return top N
    scored_projects.sort(key=lambda x: x[1], reverse=True)
    return [p[0] for p in scored_projects[:max_projects]]

def optimize_experience_bullets(experiences, jd_keywords, max_bullets=3):
    """
    Select and optimize experience bullets for relevance
    """
    optimized_experiences = []
    
    for exp in experiences:
        responsibilities = exp.get('responsibilities', [])
        
        # Score each responsibility by keyword matches
        scored_resp = []
        for resp in responsibilities:
            resp_lower = resp.lower()
            score = sum(1 for keyword in jd_keywords if keyword.lower() in resp_lower)
            scored_resp.append((resp, score))
        
        # Sort by score and take top N
        scored_resp.sort(key=lambda x: x[1], reverse=True)
        top_resp = [r[0] for r in scored_resp[:max_bullets]]
        
        optimized_exp = exp.copy()
        optimized_exp['responsibilities'] = top_resp
        optimized_experiences.append(optimized_exp)
    
    return optimized_experiences