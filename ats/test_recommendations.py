from ats.recommendations import generate_recommendations


score = 60

matched_skills = [
    "python",
    "sql"
]

missing_skills = [
    "tensorflow",
    "pandas"
]

recommendations = generate_recommendations(
    score,
    matched_skills,
    missing_skills
)

print("Recommendations:")

for recommendation in recommendations:
    print("•", recommendation)