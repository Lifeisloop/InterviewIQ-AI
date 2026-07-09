def calculate_ats_score(resume_skills, jd_skills):
    resume_set = {skill.lower() for skill in resume_skills}
    jd_set = {skill.lower() for skill in jd_skills}

    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)

    if not jd_set:
        score = 0
    else:
        score = round((len(matched) / len(jd_set)) * 100)

    return{
        "ats_score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }