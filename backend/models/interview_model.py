from pydantic import BaseModel
from typing import List

class InterviewRequest(BaseModel):
    candidate_name: str
    skills: List[str]
    ats_score: int
    job_description: str
