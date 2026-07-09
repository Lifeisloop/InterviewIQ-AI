import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from database.models.resume import Resume
from database.models.interview import Interview

from models.interview_model import InterviewRequest

from services.interview_service import (
    generate_interview_questions
)


def start_interview_session(
    db: Session,
    user_id: int,
    resume_id: int,
    job_description: str
):

    # Find only a resume owned by current user
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == user_id
        )
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    # Convert stored JSON text back to Python list
    skills = json.loads(
        resume.skills or "[]"
    )

    # Build input for existing AI service
    interview_data = InterviewRequest(
        candidate_name=(
            resume.candidate_name
            or "Candidate"
        ),
        skills=skills,
        ats_score=0,
        job_description=job_description
    )

    # Generate questions using Ollama
    questions = generate_interview_questions(
        interview_data
    )

    # Save session in MySQL
    new_interview = Interview(
        user_id=user_id,
        resume_id=resume_id,
        job_description=job_description,
        questions=json.dumps(questions),
        status="active"
    )

    db.add(new_interview)

    try:
        db.commit()
        db.refresh(new_interview)

    except Exception:
        db.rollback()
        raise

    return {
        "interview_id": new_interview.id,
        "resume_id": new_interview.resume_id,
        "status": new_interview.status,
        "questions": questions,
        "created_at": new_interview.created_at
    }