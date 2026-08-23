def calculate_ats_score(resume_skills, required_skills):

    resume_skills = {
        skill.lower().strip()
        for skill in resume_skills
    }

    required_skills = {
        skill.lower().strip()
        for skill in required_skills
    }

    if not required_skills:
        return 0, [], []

    matched_skills = resume_skills.intersection(required_skills)
    missing_skills = required_skills - resume_skills

    score = (
        len(matched_skills) / len(required_skills)
    ) * 100

    return (
        round(score, 2),
        sorted(matched_skills),
        sorted(missing_skills)
    )