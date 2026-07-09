import json
from sqlalchemy.orm import Session
from database.models.resume import Resume

def save_resume(
        db: Session,
        user_id: int,
        file_name: str,
        file_path: str,
        candidate_name: str | None,
        candidate_email: str | None,
        candidate_phone: str | None,
        skills: list[str],
        parsed_text: str
):
    
    resume = Resume(
         user_id=user_id,
        file_name=file_name,
        file_path=file_path,
        candidate_name=candidate_name,
        candidate_email=candidate_email,
        candidate_phone=candidate_phone,
        skills=json.dumps(skills),
        parsed_text=parsed_text
    )

    db.add(resume)

    try: 
        db.commit()
        db.refresh(resume)

    except Exception:
        db.rollback()
        raise

    return resume