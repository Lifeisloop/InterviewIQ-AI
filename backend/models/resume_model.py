from datetime import datetime
from pydantic import BaseModel

class ResumeResponse(BaseModel):
    id: int
    user_id: int
    file_name: str
    candidate_name: str
    candidate_email: str
    candidate_phone: str
    skills: list[str]
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }