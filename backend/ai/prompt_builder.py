def build_interview_prompt(name, skills, ats_score, job_description):
    prompt = f"""
You are an experienced technical interviewer.

Candidate Name:
{name}

Candidate Skills:
{', '.join(skills)}

ATS Score:
{ats_score}

Job Description:
{job_description}

Generate the following:

1. Five Easy Technical Questions

2. Five Medium Technical Questions

3. Five Hard Technical Questions

4. Three Coding Questions

5. Five HR Questions

Return ONLY valid JSON.

Do not write:
Here are the questions.

Do not use markdown.

Do not use ```json

Return exactly this format:

{{
  "easy": [],
  "medium": [],
  "hard": [],
  "coding": [],
  "hr": []
}}
"""
    return prompt