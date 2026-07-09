from pydantic import BaseModel

class ATSRequest(BaseModel):
    resume_skills: list[str]
    job_description: str