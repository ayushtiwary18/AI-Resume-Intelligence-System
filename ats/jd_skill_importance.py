from collections import Counter


def analyze_skill_importance(job_description, detected_skills):
    """
    Analyze how frequently each detected skill appears
    in a job description.
    """

    if not job_description or not detected_skills:
        return {}

    text = job_description.lower()

    skill_counts = Counter()

    for skill in detected_skills:
        skill_lower = skill.lower().strip()

        count = text.count(skill_lower)

        skill_counts[skill_lower] = count

    max_count = max(skill_counts.values(), default=0)

    importance = {}

    for skill, count in skill_counts.items():

        if count == 0:
            level = "Normal"

        elif count == max_count and count > 1:
            level = "High"

        elif count > 1:
            level = "Medium"

        else:
            level = "Normal"

        importance[skill] = {
            "count": count,
            "importance": level
        }

    return importance