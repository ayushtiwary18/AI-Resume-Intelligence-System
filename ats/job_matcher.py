from resume_parser.skill_extractor import SKILLS


def extract_required_skills(job_description):

    job_description = job_description.lower()

    required_skills = []

    for skill in SKILLS:
        if skill.lower() in job_description:
            required_skills.append(skill)

    return required_skills