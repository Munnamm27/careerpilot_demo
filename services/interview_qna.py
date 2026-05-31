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


class InterviewQnA(BaseModel):
    question: str = Field(
        description="Interview question"
    )

    options: List[str] = Field(
        description="Exactly 4 answer options"
    )

    answer: str = Field(
        description="Correct answer"
    )

    explanation: str = Field(
        description="Explanation of why the answer is correct"
    )


class InterviewPreparation(BaseModel):
    qna: List[InterviewQnA] = Field(
        description="List of interview questions and answers"
    )


def generate_interview_qna(
    resume_text: str,
    jd_text: str,
    num_questions: int = 10
):

    interview_llm = llm.with_structured_output(
        InterviewPreparation
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert technical interviewer.

Responsibilities:

1. Analyze the candidate's resume.
2. Analyze the job description.
3. Generate interview questions relevant to:
   - Required skills
   - Candidate experience
   - Missing skills
   - Real-world job responsibilities

Rules:

1. Generate EXACTLY the requested number of questions.
2. Each question must have EXACTLY 4 options.
3. Only ONE option should be correct.
4. Include the correct answer.
5. Include a short explanation.
6. Mix difficulty levels:
   - 30% Easy
   - 50% Medium
   - 20% Hard
7. Focus on practical interview questions.
8. Avoid duplicate questions.
                """
            ),
            (
                "human",
                """
Resume:
{resume}

Job Description:
{jd}

Generate exactly {num_questions} interview questions.
                """
            )
        ]
    )

    chain = prompt | interview_llm

    result = chain.invoke(
        {
            "resume": resume_text,
            "jd": jd_text,
            "num_questions": num_questions
        }
    )

    return result.model_dump()


if __name__ == "__main__":
    from utils.doc_loader import resume_loader, text_loader
    resume_text = resume_loader("docs/Mahmud_Hasan_Munna_BL.pdf")
    jd_text = text_loader("docs/jd.txt")

    interview_qna = generate_interview_qna(resume_text, jd_text, num_questions=10)
    print(interview_qna)