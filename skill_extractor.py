import re

# Sample skill list (replace/extend with real database or API)
SKILLS_DB = [
    "python", "java", "c++", "react", "node", "aws", "docker",
    "sql", "mongodb", "flask", "tensorflow", "pytorch", "ml", "nlp"
]

def extract_skills(text):
    text = text.lower()
    found = [skill for skill in SKILLS_DB if skill in text]
    return list(set(found))

def skill_coverage(resume_text, jd_text):
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))
    common = resume_skills.intersection(jd_skills)
    total_required = len(jd_skills)
    return {
        "resume_skills": list(resume_skills),
        "jd_skills": list(jd_skills),
        "common_skills": list(common),
        "coverage_score": round(len(common) / total_required * 100, 2) if total_required else 0
    }
