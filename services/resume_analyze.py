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

# response = llm.invoke("Hi")
# print(response.content)

def analyze_resume(resume_text, jd_text):
    class ResumeAnalysis(BaseModel):
        strong_points: List[str] = Field(description="List of strong points in the resume")
        weak_points: List[str] = Field(description="List of weak points in the resume")

    analyze_llm = llm.with_structured_output(ResumeAnalysis)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an expert AI assistant specializing in Resume Strong and Weakness Analysis.

                Responsibilities:
                - You will be provided with a resume and a job description.
                - Analyze the resume in the context of the job description.
                - You will provide a structured analysis highlighting the strong points and weak points of the resume with respect to the job description.
                - Max allowed strong points: 5
                - Max allowed weak points: 5

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
    analyze_chain = prompt | analyze_llm
    result = analyze_chain.invoke(
        {
            "resume": resume_text,
            "jd": jd_text,
        }
    )
    return dict(result)


if __name__ == "__main__":
    from utils.doc_loader import resume_loader, text_loader
    resume_text = resume_loader("docs/Mahmud_Hasan_Munna_BL.pdf")
    jd_text = text_loader("docs/jd.txt")

    analysis = analyze_resume(resume_text, jd_text)
    print(analysis)