from ats.skill_gap_analyzer import analyze_skill_gap


resume_skills = [
    "Python",
    "Machine Learning",
    "SQL"
]

required_skills = [
    "Python",
    "Machine Learning",
    "SQL",
    "Pandas",
    "TensorFlow"
]


result = analyze_skill_gap(
    resume_skills,
    required_skills
)


print("Skill Gap Analysis")
print("-------------------")

print("Matched Skills:", result["matched_skills"])
print("Missing Skills:", result["missing_skills"])
print("Match Percentage:", result["match_percentage"])
print("Gap Percentage:", result["gap_percentage"])