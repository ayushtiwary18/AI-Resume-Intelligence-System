from ats.relevant_resume_text import build_relevant_resume_text


resume_text = """
Worked on machine learning projects using Python and SQL.
Built predictive models and performed data analysis.
"""

skills = [
    "Python",
    "Machine Learning",
    "SQL",
    "Pandas"
]

education = [
    "B.Tech Computer Science"
]

experience = [
    "Data Science Internship"
]


result = build_relevant_resume_text(
    resume_text,
    skills,
    education,
    experience
)

print("Relevant Resume Text:")
print(result)