from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.interview_model import InterviewRequest
from models.interview_session_model import StartInterviewRequest

from services.interview_service import generate_interview_questions
from services.interview_session_service import start_interview_session

from database.connection import get_db
from database.models.user import User

from utils.dependencies import get_current_user


router = APIRouter()


# Existing endpoint
@router.post("/generate")
def generate(request: InterviewRequest):

    return generate_interview_questions(request)


# New interview session endpoint
@router.post("/start")
def start_interview(
    request: StartInterviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return start_interview_session(
        db=db,
        user_id=current_user.id,
        resume_id=request.resume_id,
        job_description=request.job_description
    )