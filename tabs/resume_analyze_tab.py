import streamlit as st
from services.resume_analyze import analyze_resume


def render(resume_text, jd_text):
    st.header("Resume Analyzer")
    st.write("Highlights the strong and weak points of your resume against the job description.")

    if st.button("Analyze Resume"):
        if not resume_text:
            st.warning("Please upload your resume in the sidebar.")
            return
        if not jd_text.strip():
            st.warning("Please paste the job description in the sidebar.")
            return

        with st.spinner("Analyzing your resume..."):
            result = analyze_resume(resume_text, jd_text)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Strong Points")
            for point in result.get("strong_points", []):
                st.success(f"✓ {point}")

        with col2:
            st.subheader("Weak Points")
            for point in result.get("weak_points", []):
                st.error(f"✗ {point}")
