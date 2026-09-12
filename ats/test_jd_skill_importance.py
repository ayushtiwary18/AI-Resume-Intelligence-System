from ats.jd_analyzer import extract_jd_skills
from ats.jd_skill_importance import analyze_skill_importance


job_description = """
We are looking for a Data Scientist with strong Python experience.

The candidate should have excellent Python programming skills.
Python development experience is highly desirable.

Experience with SQL and Pandas is also required.
Knowledge of Power BI is preferred.
"""


detected_skills = extract_jd_skills(job_description)

result = analyze_skill_importance(
    job_description,
    detected_skills
)


print("JD Skill Importance")
print("-------------------")

for skill, data in result.items():
    print(
        f"{skill}: "
        f"{data['count']} occurrence(s) - "
        f"{data['importance']}"
    )