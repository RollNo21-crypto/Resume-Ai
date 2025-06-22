def compute_final_score(semantic_score, skill_score, length_score, section_score):
    # Weight config (adjust as needed)
    weights = {
        "semantic": 0.4,
        "skills": 0.3,
        "length": 0.15,
        "sections": 0.15
    }
    final = (
        semantic_score * weights["semantic"]
        + skill_score * weights["skills"]
        + length_score * weights["length"]
        + section_score * weights["sections"]
    )
    return round(final, 2)

def get_length_score(text):
    word_count = len(text.split())
    if word_count < 250:
        return 40
    elif word_count < 500:
        return 70
    else:
        return 90

def check_sections(text):
    sections = ["experience", "education", "projects", "skills", "summary", "certification"]
    found = sum([1 for section in sections if section in text.lower()])
    return round((found / len(sections)) * 100, 2)
