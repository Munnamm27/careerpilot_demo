import streamlit as st
import tempfile
import os
from utils.doc_loader import resume_loader
from tabs import resume_analyze_tab, resume_feedback_tab, study_plan_tab, interview_qna_tab

st.set_page_config(
    page_title="CareerPilot",
    page_icon="🚀",
    layout="wide"
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🚀 CareerPilot")
    st.write("Fill in the details below, then pick a tab.")

    st.divider()

    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Paste Job Description", height=250)

    st.divider()

    st.subheader("Study Plan Settings")
    study_days = st.number_input("Study Days", min_value=1, max_value=90, value=30)

    st.subheader("Interview Q&A Settings")
    num_questions = st.number_input("Number of Questions", min_value=1, max_value=30, value=10)

# ── Load resume text once (shared across all tabs) ───────────────────────────
resume_text = None
if resume_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(resume_file.read())
        tmp_path = tmp.name
    try:
        resume_text = resume_loader(tmp_path)
    finally:
        os.unlink(tmp_path)

# ── Main content ──────────────────────────────────────────────────────────────
st.title("🚀 CareerPilot")
st.write("Your AI-powered career assistant.")
st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "Resume Analyzer",
    "Resume Feedback",
    "Study Plan",
    "Interview Q&A"
])

with tab1:
    resume_analyze_tab.render(resume_text, jd_text)

with tab2:
    resume_feedback_tab.render(resume_text, jd_text)

with tab3:
    study_plan_tab.render(resume_text, jd_text, study_days)

with tab4:
    interview_qna_tab.render(resume_text, jd_text, num_questions)
