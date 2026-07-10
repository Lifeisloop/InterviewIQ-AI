from ai.prompt_builder import build_interview_prompt
from ai.llm import ask_llm
import json

def generate_interview_questions(data):

    prompt = build_interview_prompt(
        name = data.candidate_name,
        skills = data.skills,
        ats_score = data.ats_score,
        job_description = data.job_description
    )

    response = ask_llm(prompt)

    try:
        return json.loads(response)
    except Exception:
        return { "raw_response": response}
    