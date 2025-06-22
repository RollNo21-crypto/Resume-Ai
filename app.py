import streamlit as st
from semantic_matcher import get_semantic_score
from skill_extractor import skill_coverage
from score_engine import compute_final_score, get_length_score, check_sections
from feedback_generator import generate_feedback

st.set_page_config(page_title="📄 Resume Critic Pro", layout="centered")

st.title("🧐 Resume Critic Pro – Industry-Ready AI Resume Analyzer")
st.write("Upload your resume and paste the job description to receive an AI-driven analysis.")

resume_file = st.file_uploader("📄 Upload Resume (PDF or TXT)", type=["pdf", "txt"])
jd_text = st.text_area("📑 Paste Job Description Here", height=250)

analyze = st.button("🔍 Analyze Resume")

if analyze:
    if resume_file and jd_text:
        if resume_file.name.endswith(".txt"):
            resume_text = resume_file.read().decode("utf-8")
        elif resume_file.name.endswith(".pdf"):
            import pdfplumber
            text = ""
            with pdfplumber.open(resume_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
            resume_text = text
        else:
            st.error("Unsupported file format.")
            st.stop()

        # Compute scores
        semantic_score = get_semantic_score(resume_text, jd_text)
        skill_result = skill_coverage(resume_text, jd_text)
        length_score = get_length_score(resume_text)
        section_score = check_sections(resume_text)
        final_score = compute_final_score(semantic_score, skill_result["coverage_score"], length_score, section_score)
        feedback = generate_feedback(final_score, skill_result["coverage_score"], list(set(skill_result["jd_skills"]) - set(skill_result["common_skills"])))

        # Results UI
        st.subheader("📊 Resume Evaluation Summary")
        st.metric("🔍 Semantic Match", f"{semantic_score} %")
        st.metric("🛠️ Skill Match", f"{skill_result['coverage_score']} %")
        st.metric("🧾 Resume Length Score", f"{length_score} %")
        st.metric("📄 Section Coverage", f"{section_score} %")
        st.metric("🎯 Final Resume Score", f"{final_score} / 100")

        with st.expander("✅ Matching Skills"):
            st.write(", ".join(skill_result["common_skills"]))

        with st.expander("❌ Missing Skills"):
            st.write(", ".join(set(skill_result["jd_skills"]) - set(skill_result["common_skills"])))

        with st.expander("💡 AI Suggestions"):
            for tip in feedback:
                st.write("- " + tip)
    else:
        st.warning("Please upload a resume and paste a job description.")
