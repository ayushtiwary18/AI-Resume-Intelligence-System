from ats.job_matcher import extract_required_skills


job_description = """
We are looking for a Data Scientist with strong Python,
SQL, Pandas, Machine Learning and TensorFlow skills.
Experience with Power BI is also preferred.
"""

required_skills = extract_required_skills(job_description)

print("Required Skills:", required_skills)