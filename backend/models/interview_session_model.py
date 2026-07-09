from pydantic import BaseModel, Field

class StartInterviewRequest(BaseModel):
    resume_id: int

    job_description: str = Field(
        min_length = 20
    )