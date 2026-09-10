import re


KNOWN_SKILLS = {
    "python",
    "java",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "html",
    "css",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "pandas",
    "numpy",
    "scikit-learn",
    "sklearn",
    "tensorflow",
    "pytorch",
    "keras",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "natural language processing",
    "computer vision",
    "data science",
    "data analysis",
    "power bi",
    "tableau",
    "excel",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
}


def extract_jd_skills(job_description):
    """
    Extract known technical skills from a job description.
    """

    if not job_description or not job_description.strip():
        return []

    text = job_description.lower()

    found_skills = []

    for skill in KNOWN_SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(found_skills)