
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

def get_resume_feedback(resume_text, jd_text):
    class ResumeFeedback(BaseModel):
        to_be_added: List[str] = Field(description="Elements that are missing in the resume but are relevant to the job description")
        to_be_deleted: List[str] = Field(description="Elements that are present in the resume but are not relevant to the job description")

    feedback_llm = llm.with_structured_output(ResumeFeedback)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an expert AI assistant specializing in Resume Providing Resume Feedback.

                Responsibilities:
                - You will be provided with a resume and a job description.
                - Analyze the resume in the context of the job description.
                - You will provide a structured feedback highlighting the elements that are missing in the resume but are relevant to the job description (to_be_added) and the elements that are present in the resume but are not relevant to the job description (to_be_deleted).


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
    feedback_chain = prompt | feedback_llm
    result = feedback_chain.invoke(
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

    feedback = get_resume_feedback(resume_text, jd_text)
    print(feedback)