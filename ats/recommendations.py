def generate_recommendations(
    score,
    matched_skills,
    missing_skills
):
    recommendations = []

    # Overall score recommendation
    if score < 50:
        recommendations.append(
            "The resume has a low skill match with the job description."
        )

    elif score < 75:
        recommendations.append(
            "The resume has a moderate skill match with the job description."
        )

    else:
        recommendations.append(
            "The resume has a strong skill match with the job description."
        )

    # Missing skills recommendation
    if missing_skills:
        recommendations.append(
            "Consider adding the following skills if you genuinely have them: "
            + ", ".join(
                skill.title()
                for skill in missing_skills
            )
        )

    # Matched skills
    if matched_skills:
        recommendations.append(
            "Your resume already contains some skills relevant to this job."
        )

    return recommendations