from database.operations import get_ats_analyses_by_resume_id


resume_id = 3

analyses = get_ats_analyses_by_resume_id(resume_id)

print("ATS Analysis History")
print("--------------------")

for analysis in analyses:

    print(
        "Analysis ID:", analysis["analysis_id"],
        "| Score:", analysis["ats_score"],
        "| Date:", analysis["analysis_time"]
    )