from pydantic import BaseModel, Field

class AnswerItem(BaseModel):
    question: str

    answer: str = Field(
        min_length=1
    )

class FinalReportRequest(BaseModel):
    interview_id: int

    answers: list[AnswerItem] = Field(
        min_length=1
    )