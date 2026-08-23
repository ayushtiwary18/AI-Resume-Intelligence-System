# Skill importance weights
SKILL_WEIGHTS = {
    "python": 3,
    "machine learning": 3,
    "sql": 2,
    "pandas": 2,
    "tensorflow": 2,
}


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

    total_weight = sum(
        SKILL_WEIGHTS.get(skill, 1)
        for skill in required_skills
    )

    matched_weight = sum(
        SKILL_WEIGHTS.get(skill, 1)
        for skill in matched_skills
    )

    score = (
        matched_weight / total_weight
    ) * 100

    return (
        round(score, 2),
        sorted(matched_skills),
        sorted(missing_skills)
    )