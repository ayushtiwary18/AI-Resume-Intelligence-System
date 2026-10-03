SKILL_ALIASES = {
    "ml": "machine learning",
    "machine-learning": "machine learning",
    "machinelearning": "machine learning",

    "nlp": "natural language processing",
    "natural-language-processing": "natural language processing",

    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "scikit_learn": "scikit-learn",

    "postgres": "postgresql",
    "postgres sql": "postgresql",

    "powerbi": "power bi",
    "power-bi": "power bi",

    "tf": "tensorflow",
    "pytorch": "pytorch",

    "js": "javascript",
    "javascript": "javascript",

    "reactjs": "react",
    "react.js": "react",
}


def normalize_skill(skill):
    """
    Convert a skill or skill alias into a canonical skill name.
    """

    normalized = skill.lower().strip()

    return SKILL_ALIASES.get(
        normalized,
        normalized
    )


def normalize_skills(skills):
    """
    Normalize a list of skills and remove duplicates.
    """

    normalized_skills = {
        normalize_skill(skill)
        for skill in skills
        if skill and skill.strip()
    }

    return sorted(normalized_skills)