def analyze_skill_gap(resume_skills, required_skills):
    """
    Compare resume skills with job-required skills
    and calculate the skill gap.
    """

    resume_skills = {
        skill.lower().strip()
        for skill in resume_skills
    }

    required_skills = {
        skill.lower().strip()
        for skill in required_skills
    }

    if not required_skills:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "match_percentage": 0,
            "gap_percentage": 0
        }

    matched_skills = resume_skills.intersection(required_skills)
    missing_skills = required_skills - resume_skills

    match_percentage = (
        len(matched_skills) / len(required_skills)
    ) * 100

    gap_percentage = (
        len(missing_skills) / len(required_skills)
    ) * 100

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "match_percentage": round(match_percentage, 2),
        "gap_percentage": round(gap_percentage, 2)
    }