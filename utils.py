import pdfplumber
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Lightweight stopword list
STOPWORDS = set([
    "the", "is", "and", "in", "to", "of", "a", "with", "that", "for", "on",
    "as", "an", "are", "by", "at", "be", "this", "or", "from", "it", "your"
])

# Clean and tokenize text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = [word for word in text.split() if word not in STOPWORDS]
    return " ".join(tokens)

# Cosine similarity for resume-job match
def rate_resume(resume_text, job_text):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity_score * 100, 2)

# Common words
def get_common_words(resume_text, job_text):
    resume_words = set(resume_text.split())
    job_words = set(job_text.split())
    return sorted(list(resume_words.intersection(job_words)))[:20]

# Missing keywords
def find_missing_keywords(resume_text, job_text):
    resume_words = set(resume_text.split())
    job_words = set(job_text.split())
    missing = job_words - resume_words
    keywords = [word for word in missing if len(word) > 4]
    return sorted(keywords)[:15]

# Format suggestions
def check_format_quality(raw_text):
    suggestions = []
    if len(raw_text) < 800:
        suggestions.append("Your resume appears too short. Add more relevant experience or skills.")
    if "-" not in raw_text and "•" not in raw_text:
        suggestions.append("Consider using bullet points to structure your experience clearly.")
    if "objective" not in raw_text.lower() and "summary" not in raw_text.lower():
        suggestions.append("You may add a short summary or objective at the top.")
    return suggestions
