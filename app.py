import streamlit as st
import os
import uuid
import hashlib

from database.operations import (
    save_resume,
    get_resume_by_hash,
    save_extracted_data,
    get_extracted_data_by_resume_id,
    save_ats_analysis,
    get_existing_ats_analysis
)
from resume_parser.extractor import extract_text
from preprocessing.cleaner import clean_text
from resume_parser.info_extractor import (
    extract_email,
    extract_phone,
    extract_name
)
from resume_parser.skill_extractor import extract_skills
from resume_parser.education_extractor import extract_education
from resume_parser.experience_extractor import extract_experience
from ats.job_matcher import extract_required_skills
from ats.scorer import calculate_ats_score
from ats.recommendations import generate_recommendations

st.set_page_config(
    page_title="AI Resume Intelligence System",
    page_icon="📄",
    layout="wide"
)

st.title("AI Resume Intelligence System")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file:

    upload_folder = "uploads/resumes"
    os.makedirs(upload_folder, exist_ok=True)

    # Get file bytes
    file_bytes = uploaded_file.getvalue()

    # Create unique hash for the uploaded file
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    # Check whether this exact resume already exists
    existing_resume = get_resume_by_hash(file_hash)

    if existing_resume:

        st.info("This resume already exists in the system.")
        resume_id = existing_resume[0]
        file_path = existing_resume[3]

    else:

        unique_filename = f"{uuid.uuid4()}.pdf"

        file_path = os.path.join(
            upload_folder,
            unique_filename
        )

        # Save PDF
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        # Save metadata
        resume_id = save_resume(
            uploaded_file.name,
            unique_filename,
            file_path,
            file_hash
        )

        st.success("Resume uploaded successfully!")

    resume_text = extract_text(file_path)
    cleaned_text = clean_text(resume_text)

    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    name = extract_name(resume_text)

    skills = extract_skills(cleaned_text)
    education = extract_education(cleaned_text)
    experience = extract_experience(cleaned_text)

    existing_extracted_data = (
        get_extracted_data_by_resume_id(resume_id)
    )

    if not existing_extracted_data:

        save_extracted_data(
            resume_id,
            name,
            email,
            phone,
            skills,
            education,
            experience
        )

        st.success("Extracted data saved to database.")

    else:

        st.info("Extracted data already exists.")

    if resume_text.strip():

        st.subheader("Extracted Resume Text")

        st.text_area(
            "Resume Content",
            resume_text,
            height=350
        )
        st.subheader("Cleaned Resume Text")

        st.text_area(
            "Cleaned Content",
            cleaned_text,
            height=350
        )

        st.subheader("Extracted Information")

        st.write("Name:", name if name else "Not Found")
        st.write("Email:", email if email else "Not Found")
        st.write("Phone:", phone if phone else "Not Found")  

        st.subheader("Extracted Skills")

        if skills:
            for skill in skills:
                st.write("•", skill.title())
        else:
            st.warning("No skills found.") 

        st.subheader("Education")

        if education:
            for degree in education:
                st.write("•", degree.upper())
        else:
            st.warning("No education details found.")  

        st.subheader("Experience")
        if experience:
            for item in experience:
                st.write("•", item)
        else:
            st.warning("No experience duration found.")

        st.subheader("Job Description")

        job_description = st.text_area(
            "Paste the job description here",
            height=250,
            placeholder="Example: We are looking for a Data Scientist with Python, SQL, Pandas and Machine Learning skills..."
        )

        if job_description.strip():

            if st.button("Analyze Resume Against Job Description"):

                existing_analysis = get_existing_ats_analysis(
                    resume_id,
                    job_description
                )

                if existing_analysis:

                    st.info("This resume has already been analyzed against this Job Description.")

                    score = existing_analysis["ats_score"]

                    matched_skills = (
                        existing_analysis["matched_skills"].split(", ")
                        if existing_analysis["matched_skills"]
                        else []
                    )

                    missing_skills = (
                        existing_analysis["missing_skills"].split(", ")
                        if existing_analysis["missing_skills"]
                        else []
                    )

                else:

                    required_skills = extract_required_skills(
                        job_description
                    )

                    score, matched_skills, missing_skills = calculate_ats_score(
                        skills,
                        required_skills
                    )

                    save_ats_analysis(
                        resume_id,
                        job_description,
                        score,
                        matched_skills,
                        missing_skills
                    )

                    st.success("New ATS analysis saved to database.")

                st.subheader("ATS Analysis")

                st.metric(
                    "ATS Skill Match Score",
                    f"{score}%"
                )

                st.write("### Matched Skills")

                if matched_skills:
                    for skill in matched_skills:
                        st.write("✓", skill.title())
                else:
                    st.write("No matching skills found.")

                st.write("### Missing Skills")

                if missing_skills:
                    for skill in missing_skills:
                        st.write("✗", skill.title())
                else:
                    st.write("No missing skills.")

                recommendations = generate_recommendations(
                    score,
                    matched_skills,
                    missing_skills
                )

                st.subheader("Recommendations")

                for recommendation in recommendations:
                    st.write("•", recommendation)

    else:
        st.error("No readable text found. The PDF may be scanned.")