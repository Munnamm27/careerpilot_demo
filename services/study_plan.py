### Promt --> LLM --> Structured Output Response
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage,SystemMessage
from pydantic import BaseModel, Field
from typing import List
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    temperature=0
)


def get_skill_gap(resume_text, jd_text):
    class SkillGapAnalysis(BaseModel):
        skill: List[str] = Field(description="List of skills that are required for the job but are missing in the resume")

    skill_gap_llm = llm.with_structured_output(SkillGapAnalysis)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an expert AI assistant specializing in Skill Gap Analysis.

                Responsibilities:
                - You will be provided with a resume and a job description.
                - Analyze the resume in the context of the job description.
                - You will provide a structured output listing the technical skills that are required for the job but are missing in the resume.
                - Only list the technical skills(theory and hands-on) that are relevant to the job description and are missing in the resume. Do not list any other elements.

                """
            ),
            (
                "human",
                """
                Resume:
                {resume}

                JD:
                {jd}
                """
            ),
        ]
    )
    skill_gap_chain = prompt | skill_gap_llm
    result = skill_gap_chain.invoke(
        {
            "resume": resume_text,
            "jd": jd_text,
        }
    )
    return dict(result)


def study_plan_based_on_skill_gaps(
    resume_text: str,
    jd_text: str,
    days_for_study: int = 30
):
    """
    Generate a personalized day-by-day study plan based on skill gaps.
    """

    # -----------------------------
    # Structured Output Models
    # -----------------------------
    class DayPlan(BaseModel):
        topic: str = Field(
            description="Main topic to study on this day"
        )
        subtopics: List[str] = Field(
            description="Detailed subtopics to cover"
        )

    class StudyPlan(BaseModel):
        study_plan: List[DayPlan] = Field(
            description="""
            List of day plans.
            """
        )

    # -----------------------------
    # Get Skill Gaps
    # -----------------------------
    skills = get_skill_gap(
        resume_text,
        jd_text
    )["skill"]

    # -----------------------------
    # Structured Output LLM
    # -----------------------------
    study_plan_llm = llm.with_structured_output(StudyPlan)

    # -----------------------------
    # Prompt
    # -----------------------------
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert AI career coach and technical mentor.

Your task is to create a detailed study plan for a candidate.

Rules:

1. Analyze the missing skills carefully.
2. Create a study plan spanning EXACTLY the number of days provided.
3. The output keys MUST be:
   day_1, day_2, day_3 ... day_N
4. N must equal the study days provided.
5. Each day must contain:
   - topic
   - subtopics
6. Progress from beginner to advanced.
7. Prioritize high-impact skills first.
8. Ensure all missing skills are covered.
9. If days are more than required, distribute learning, revision,
   hands-on projects, interview preparation, and mock assessments.
10. Keep topics practical and job-focused.
11. Each day should contain 3-6 subtopics.
12. Return ONLY the structured output.
                """
            ),
            (
                "human",
                """
Resume:
{resume}

Job Description:
{jd}

Missing Skills:
{skills}

Study Days:
{days}

Create a day-by-day study plan.
                """
            ),
        ]
    )

    # -----------------------------
    # Chain
    # -----------------------------
    chain = prompt | study_plan_llm

    result = chain.invoke(
        {
            "resume": resume_text,
            "jd": jd_text,
            "skills": skills,
            "days": days_for_study,
        }
    )

    return result.model_dump()


if __name__ == "__main__":
    from utils.doc_loader import resume_loader, text_loader
    resume_text = resume_loader("docs/Mahmud_Hasan_Munna_BL.pdf")
    jd_text = text_loader("docs/jd.txt")

    study_plan = study_plan_based_on_skill_gaps(
        resume_text,
        jd_text,
        days_for_study=7
    )

    print(study_plan)