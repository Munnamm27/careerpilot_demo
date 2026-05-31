import streamlit as st
from services.study_plan import study_plan_based_on_skill_gaps


def render(resume_text, jd_text, study_days):
    st.header("Study Plan Generator")
    st.write("Get a personalized day-by-day study plan based on the skills missing from your resume.")

    if st.button("Generate Study Plan"):
        if not resume_text:
            st.warning("Please upload your resume in the sidebar.")
            return
        if not jd_text.strip():
            st.warning("Please paste the job description in the sidebar.")
            return

        with st.spinner("Building your study plan..."):
            result = study_plan_based_on_skill_gaps(resume_text, jd_text, days_for_study=study_days)

        st.subheader(f"Your {study_days}-Day Study Plan")

        for index, day_plan in enumerate(result.get("study_plan", []), start=1):
            with st.expander(f"Day {index}: {day_plan['topic']}"):
                for subtopic in day_plan.get("subtopics", []):
                    st.write(f"• {subtopic}")
