from ats.semantic_matcher import calculate_semantic_similarity


resume_text = """
Python developer with experience in machine learning,
data analysis, pandas, SQL and TensorFlow.
Worked on data science projects and predictive models.
"""


job_description = """
We are looking for a Data Scientist with strong Python,
machine learning, SQL and data analysis skills.
Experience with Pandas and TensorFlow is preferred.
"""


score = calculate_semantic_similarity(
    resume_text,
    job_description
)

print("Semantic Similarity:", score, "%")
