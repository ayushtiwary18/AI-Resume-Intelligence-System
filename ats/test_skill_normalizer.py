from ats.skill_normalizer import (
    normalize_skill,
    normalize_skills
)


test_skills = [
    "Python",
    "ML",
    "NLP",
    "Scikit Learn",
    "Postgres",
    "PowerBI",
    "TensorFlow"
]


print("Individual tests:")

for skill in test_skills:
    print(
        f"{skill} -> {normalize_skill(skill)}"
    )


print("\nNormalized skill list:")

print(
    normalize_skills(test_skills)
)