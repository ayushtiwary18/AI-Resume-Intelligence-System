from ats.jd_analyzer import extract_jd_skills


job_description = """
We are looking for a Data Scientist with experience in
Python, Pandas, NumPy, SQL and Machine Learning.

Experience with TensorFlow and Power BI is preferred.
"""


skills = extract_jd_skills(job_description)

print("Extracted JD Skills:")
for skill in skills:
    print("-", skill)