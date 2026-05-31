import streamlit as st
from services.interview_qna import generate_interview_qna

LABELS = ["A", "B", "C", "D"]


def render(resume_text, jd_text, num_questions):
    st.header("Interview Q&A Practice")
    st.write("Generate multiple-choice interview questions tailored to your resume and the job description.")

    if st.button("Generate Questions"):
        if not resume_text:
            st.warning("Please upload your resume in the sidebar.")
            return
        if not jd_text.strip():
            st.warning("Please paste the job description in the sidebar.")
            return

        with st.spinner("Generating interview questions..."):
            result = generate_interview_qna(resume_text, jd_text, num_questions=num_questions)

        # Store in session state so results persist after clicking "Reveal Answer"
        st.session_state["qna_result"] = result.get("qna", [])

    # Render questions if they exist in session state
    if "qna_result" in st.session_state:
        qna_list = st.session_state["qna_result"]
        st.subheader(f"{len(qna_list)} Interview Questions")

        for index, qna in enumerate(qna_list):
            st.markdown(f"### Q{index + 1}. {qna['question']}")

            # Show A / B / C / D options
            for label, option in zip(LABELS, qna.get("options", [])):
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;**{label}.** {option}")

            # Reveal answer button — unique key per question
            if st.button("Reveal Answer", key=f"reveal_{index}"):
                st.session_state[f"show_answer_{index}"] = True

            if st.session_state.get(f"show_answer_{index}"):
                st.success(f"Correct Answer: {qna['answer']}")
                st.info(f"Explanation: {qna['explanation']}")

            st.divider()
