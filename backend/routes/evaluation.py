from fastapi import APIRouter
from models.evaluation import EvaluationRequest
from services.evaluation_service import evaluate_answer

router = APIRouter()


@router.post("/evaluate")
def evaluate(request: EvaluationRequest):
    return evaluate_answer(request)