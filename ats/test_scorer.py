from ats.scorer import calculate_ats_score


resume_skills = [
    "Python",
    "SQL",
    "Pandas",
    "Machine Learning"
]

required_skills = [
    "Python",
    "SQL",
    "Pandas",
    "Machine Learning",
    "TensorFlow"
]

score, matched, missing = calculate_ats_score(
    resume_skills,
    required_skills
)

print("ATS Score:", score)
print("Matched Skills:", matched)
print("Missing Skills:", missing)