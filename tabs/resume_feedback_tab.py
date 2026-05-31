import streamlit as st
from services.resume_feedback import get_resume_feedback


def render(resume_text, jd_text):
    st.header("Resume Feedback")
    st.write("See what to add and what to remove from your resume based on the job description.")

    if st.button("Get Feedback"):
        if not resume_text:
            st.warning("Please upload your resume in the sidebar.")
            return
        if not jd_text.strip():
            st.warning("Please paste the job description in the sidebar.")
            return

        with st.spinner("Generating feedback..."):
            result = get_resume_feedback(resume_text, jd_text)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Add to Resume")
            for item in result.get("to_be_added", []):
                st.success(f"+ {item}")

        with col2:
            st.subheader("Remove from Resume")
            for item in result.get("to_be_deleted", []):
                st.error(f"− {item}")
