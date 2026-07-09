from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from database.models.interview import Interview
from models.evaluation import EvaluationRequest
from services.evaluation_service import evaluate_answer


def generate_final_report(
    db: Session,
    user_id: int,
    interview_id: int,
    answers: list
):

    # Find interview owned by current user
    interview = (
        db.query(Interview)
        .filter(
            Interview.id == interview_id,
            Interview.user_id == user_id
        )
        .first()
    )

    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    evaluations = []

    total_score = 0.0

    all_strengths = []
    all_weaknesses = []

    for item in answers:

        evaluation_data = EvaluationRequest(
            question=item.question,
            candidate_answer=item.answer
        )

        result = evaluate_answer(
            evaluation_data
        )

        score = float(
            result.get("score", 0)
        )

        total_score += score

        all_strengths.extend(
            result.get("strengths", [])
        )

        all_weaknesses.extend(
            result.get("weaknesses", [])
        )

        evaluations.append({
            "question": item.question,
            "answer": item.answer,
            "score": score,
            "strengths": result.get(
                "strengths",
                []
            ),
            "weaknesses": result.get(
                "weaknesses",
                []
            ),
            "ideal_answer": result.get(
                "ideal_answer",
                ""
            )
        })

    average_score = round(
        total_score / len(answers),
        2
    )

    # Remove duplicate feedback
    unique_strengths = list(
        dict.fromkeys(all_strengths)
    )

    unique_weaknesses = list(
        dict.fromkeys(all_weaknesses)
    )

    # Mark interview completed
    interview.status = "completed"

    try:
        db.commit()
        db.refresh(interview)

    except Exception:
        db.rollback()
        raise

    return {
        "interview_id": interview.id,
        "status": interview.status,
        "total_questions": len(answers),
        "average_score": average_score,
        "strengths": unique_strengths,
        "weaknesses": unique_weaknesses,
        "evaluations": evaluations
    }