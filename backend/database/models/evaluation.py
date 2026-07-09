from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    question: str
    candidate_answer: str