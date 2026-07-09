from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models.user import User

from models.report_model import FinalReportRequest

from services.report_service import generate_final_report

from utils.dependencies import get_current_user


router = APIRouter()


@router.post("/final")
def create_final_report(
    request: FinalReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return generate_final_report(
        db=db,
        user_id=current_user.id,
        interview_id=request.interview_id,
        answers=request.answers
    )