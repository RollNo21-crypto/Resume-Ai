def generate_feedback(score, coverage_score, missing_skills):
    suggestions = []

    if score < 50:
        suggestions.append("Overall match is low. Consider restructuring your resume for better alignment.")
    if coverage_score < 50:
        suggestions.append("Many required skills are missing. Add relevant projects or experiences.")

    if missing_skills:
        suggestions.append("Missing key skills: " + ", ".join(missing_skills[:5]))

    if score >= 80:
        suggestions.append("Great job! Your resume is highly aligned with the job description.")

    return suggestions
