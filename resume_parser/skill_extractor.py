SKILLS = [
    "python",
    "java",
    "c++",
    "c#",
    "sql",
    "mysql",
    "sqlite",
    "mongodb",
    "html",
    "css",
    "javascript",
    "django",
    "react.js",
    "veu.js",
    "machine learning",
    "deep learning",
    "data science",
    "data analysis",
    "natural language processing",
    "nlp",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "keras",
    "power bi",
    "tableau",
    "excel",
    "streamlit",
    "git",
    "github",
    "docker"
]


def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in SKILLS:

        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills