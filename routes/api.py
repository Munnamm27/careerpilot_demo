import os
import tempfile
from fastapi import APIRouter, UploadFile, File, Form

from utils.doc_loader import resume_loader
from services.resume_feedback import get_resume_feedback
from services.resume_analyze import analyze_resume
from services.interview_qna import generate_interview_qna
from services.study_plan import study_plan_based_on_skill_gaps

router = APIRouter(
    prefix="/api",
    tags=["CareerPilot API"],
)


def _load_resume(upload: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(upload.file.read())
        tmp_path = tmp.name
    try:
        return resume_loader(tmp_path)
    finally:
        os.unlink(tmp_path)


@router.post("/resume/feedback")
def resume_feedback(
    resume: UploadFile = File(...),
    jd_text: str = Form(...),
):
    resume_text = _load_resume(resume)
    return get_resume_feedback(resume_text, jd_text)


@router.post("/resume/analyze")
def resume_analyze(
    resume: UploadFile = File(...),
    jd_text: str = Form(...),
):
    resume_text = _load_resume(resume)
    return analyze_resume(resume_text, jd_text)


@router.post("/interview/qna")
def interview_qna(
    resume: UploadFile = File(...),
    jd_text: str = Form(...),
    num_questions: int = Form(10),
):
    resume_text = _load_resume(resume)
    return generate_interview_qna(resume_text, jd_text, num_questions)


@router.post("/study-plan")
def study_plan(
    resume: UploadFile = File(...),
    jd_text: str = Form(...),
    days_for_study: int = Form(30),
):
    resume_text = _load_resume(resume)
    return study_plan_based_on_skill_gaps(resume_text, jd_text, days_for_study)
