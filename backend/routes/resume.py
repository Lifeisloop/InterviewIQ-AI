import os
import shutil
import json
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from database.connection import get_db
from database.models.user import User

from services.resume_parser import extract_text

from services.information_extractor import (
    extract_name,
    extract_email,
    extract_phone,
    extract_skills
)

from services.resume_service import save_resume

from utils.dependencies import get_current_user


router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 1. Check filename
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is missing"
        )

    # 2. Validate PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )

    # 3. Create unique filename
    unique_filename = (
        f"{uuid.uuid4()}_{file.filename}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    try:
        # 4. Save PDF
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        # 5. Extract raw text
        text = extract_text(file_path)

        # 6. Extract structured information
        name = extract_name(text)
        email = extract_email(text)
        phone = extract_phone(text)
        skills = extract_skills(text)

        # 7. Save resume in MySQL
        saved_resume = save_resume(
            db=db,
            user_id=current_user.id,
            file_name=file.filename,
            file_path=file_path,
            candidate_name=name,
            candidate_email=email,
            candidate_phone=phone,
            skills=skills,
            parsed_text=text
        )

        # 8. Return response
        return {
            "success": True,
            "resume_id": saved_resume.id,
            "user_id": saved_resume.user_id,
            "file_name": saved_resume.file_name,
            "candidate_name": saved_resume.candidate_name,
            "candidate_email": saved_resume.candidate_email,
            "candidate_phone": saved_resume.candidate_phone,
            "skills": json.loads(
                saved_resume.skills or "[]"
            ),
            "uploaded_at": saved_resume.uploaded_at
        }

    except HTTPException:
        raise

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resume upload failed: {str(e)}"
        )

    finally:
        await file.close()