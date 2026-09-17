def build_relevant_resume_text(
    resume_text,
    skills,
    education,
    experience
):
    """
    Build a relevant text representation of a resume
    for job-description matching.
    """

    sections = []

    if skills:
        sections.append(
            "Skills: " + ", ".join(skills)
        )

    if education:
        sections.append(
            "Education: " + ", ".join(education)
        )

    if experience:
        sections.append(
            "Experience: " + ", ".join(experience)
        )

    if resume_text:
        sections.append(
            "Resume Content: " + resume_text
        )

    return "\n".join(sections)