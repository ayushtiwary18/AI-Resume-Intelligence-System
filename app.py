import streamlit as st
import os
import uuid

from database.operations import (
    save_resume,
    get_resume_by_hash,
    save_extracted_data,
    get_extracted_data_by_resume_id,
    save_ats_analysis,
    get_existing_ats_analysis,
    get_ats_analyses_by_resume_id,
    get_all_resumes,
    delete_resume
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
from resume_parser.file_hash import calculate_file_hash

st.set_page_config(
    page_title="AI Resume Intelligence System",
    page_icon="📄",
    layout="wide"
)

st.title("AI Resume Intelligence System")

if "active_resume_id" not in st.session_state:
    st.session_state.active_resume_id = None

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file:

    upload_folder = "uploads/resumes"
    os.makedirs(upload_folder, exist_ok=True)

    # Get uploaded file bytes
    file_bytes = uploaded_file.getvalue()

    # Calculate hash
    file_hash = calculate_file_hash(file_bytes)

    # Check for duplicate resume
    existing_resume = get_resume_by_hash(file_hash)

    if existing_resume:

        st.info("This resume already exists in the system.")

        resume_id = existing_resume["resume_id"]
        file_path = existing_resume["file_path"]

        # Make existing resume active
        st.session_state.active_resume_id = resume_id
    else:
        # Create unique filename
        unique_filename = f"{uuid.uuid4()}.pdf"

        file_path = os.path.join(
            upload_folder,
            unique_filename
        )

        # Save PDF
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        # Save resume metadata
        resume_id = save_resume(
            uploaded_file.name,
            unique_filename,
            file_path,
            file_hash
        )

        # Make newly uploaded resume active
        st.session_state.active_resume_id = resume_id

        st.success(
            "New resume uploaded and saved successfully!"
        )

    resume_text = extract_text(file_path)

    cleaned_text = clean_text(resume_text)

    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    name = extract_name(resume_text)

    skills = extract_skills(cleaned_text)
    education = extract_education(cleaned_text)
    experience = extract_experience(cleaned_text)

    # Check whether extracted data already exists
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

        st.success(
            "Extracted data saved to database."
        )
    else:

        st.info(
            "Extracted data already exists."
        )

st.subheader("Select Resume")

stored_resumes = get_all_resumes()


if stored_resumes:

    resume_options = {
        f"{resume['original_filename']} | "
        f"Uploaded: {resume['upload_time']}": resume
        for resume in stored_resumes
    }

    selected_resume_label = st.selectbox(
        "Choose a resume",
        list(resume_options.keys())
    )

    selected_resume = resume_options[
        selected_resume_label
    ]

    selected_resume_id = selected_resume[
        "resume_id"
    ]

    selected_file_path = selected_resume[
        "file_path"
    ]

    st.write(
        "Resume ID:",
        selected_resume_id
    )

    st.write(
        "File:",
        selected_resume["original_filename"]
    )

    if st.button("Use Selected Resume"):

        if os.path.exists(selected_file_path):

            st.session_state.active_resume_id = (
                selected_resume_id
            )

            st.success(
                "Selected resume is now active."
            )

            st.rerun()
        else:

            st.error(
                "Resume file not found."
            )

    if st.button("Delete Selected Resume"):

        result = delete_resume(
            selected_resume_id
        )

        if result:

            # Clear active resume if it was deleted
            if (
                st.session_state.active_resume_id
                == selected_resume_id
            ):
                st.session_state.active_resume_id = None

            st.success(
                "Resume deleted successfully."
            )

            st.rerun()
        else:

            st.error(
                "Resume could not be deleted."
            )
else:

    st.info(
        "No resumes stored yet."
    )

active_resume_id = (
    st.session_state.active_resume_id
)

if active_resume_id is not None:

    # Get active resume information
    active_resume = None

    for resume in stored_resumes:

        if resume["resume_id"] == active_resume_id:

            active_resume = resume
            break

    if active_resume:

        active_file_path = active_resume[
            "file_path"
        ]

        active_resume_text = extract_text(
            active_file_path
        )

        active_cleaned_text = clean_text(
            active_resume_text
        )

        active_email = extract_email(
            active_resume_text
        )

        active_phone = extract_phone(
            active_resume_text
        )

        active_name = extract_name(
            active_resume_text
        )

        active_skills = extract_skills(
            active_cleaned_text
        )

        active_education = extract_education(
            active_cleaned_text
        )

        active_experience = extract_experience(
            active_cleaned_text
        )

        st.subheader("Resume Summary")

        extracted_data = (
            get_extracted_data_by_resume_id(
                active_resume_id
            )
        )
    
        skill_count = 0
        education_count = 0

        st.subheader("ATS Score History")

        analysis_history = get_ats_analyses_by_resume_id(
            active_resume_id
        )

        if analysis_history:

            for analysis in analysis_history:

                with st.container(border=True):

                    st.write(
                        f"### Analysis {analysis['analysis_id']}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "ATS Score",
                            f"{analysis['ats_score']}%"
                        )

                    with col2:
                        st.write("**Analyzed On:**")
                        st.write(
                            analysis["analysis_time"]
                        )

                    st.write("**Matched Skills:**")

                    if analysis["matched_skills"]:
                        st.write(
                            analysis["matched_skills"]
                        )
                    else:
                        st.write("None")

                    st.write("**Missing Skills:**")

                    if analysis["missing_skills"]:
                        st.write(
                            analysis["missing_skills"]
                        )
                    else:
                        st.write("None")
        else:

            st.info(
                "No ATS analyses found for this resume."
            )


        if extracted_data:

            if extracted_data["skills"]:

                skill_count = len(
                    extracted_data["skills"].split(", ")
                )

            if extracted_data["education"]:

                education_count = len(
                    extracted_data["education"].split(", ")
                )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Resume ID",
            active_resume_id
        )

        col2.metric(
            "Skills",
            skill_count
        )

        col3.metric(
            "Education",
            education_count
        )

        col4.metric(
            "ATS Analyses",
            len(analysis_history)
        )

        if active_resume_text.strip():

            st.subheader(
                "Extracted Resume Text"
            )

            st.text_area(
                "Resume Content",
                active_resume_text,
                height=350
            )

            st.subheader(
                "Cleaned Resume Text"
            )

            st.text_area(
                "Cleaned Content",
                active_cleaned_text,
                height=350
            )

            st.subheader(
                "Extracted Information"
            )

            st.write(
                "Name:",
                active_name
                if active_name
                else "Not Found"
            )

            st.write(
                "Email:",
                active_email
                if active_email
                else "Not Found"
            )

            st.write(
                "Phone:",
                active_phone
                if active_phone
                else "Not Found"
            )

            st.subheader(
                "Extracted Skills"
            )

            if active_skills:

                for skill in active_skills:

                    st.write(
                        "•",
                        skill.title()
                    )
            else:
                st.warning(
                    "No skills found."
                )

            st.subheader(
                "Education"
            )

            if active_education:

                for degree in active_education:

                    st.write(
                        "•",
                        degree.upper()
                    )
            else:

                st.warning(
                    "No education details found."
                )

            st.subheader(
                "Experience"
            )

            if active_experience:

                for item in active_experience:

                    st.write(
                        "•",
                        item
                    )
            else:

                st.warning(
                    "No experience duration found."
                )

            st.subheader(
                "Job Description"
            )

            job_description = st.text_area(
                "Paste the job description here",
                height=250,
                placeholder=(
                    "Example: We are looking for a "
                    "Data Scientist with Python, SQL, "
                    "Pandas and Machine Learning skills..."
                )
            )

            if job_description.strip():

                if st.button(
                    "Analyze Resume Against Job Description"
                ):

                    existing_analysis = (
                        get_existing_ats_analysis(
                            active_resume_id,
                            job_description
                        )
                    )

                    if existing_analysis:

                        st.info(
                            "This resume has already been "
                            "analyzed against this Job Description."
                        )

                        score = existing_analysis[
                            "ats_score"
                        ]

                        matched_skills = (
                            existing_analysis[
                                "matched_skills"
                            ].split(", ")
                            if existing_analysis[
                                "matched_skills"
                            ]
                            else []
                        )

                        missing_skills = (
                            existing_analysis[
                                "missing_skills"
                            ].split(", ")
                            if existing_analysis[
                                "missing_skills"
                            ]
                            else []
                        )
                    else:
                        required_skills = (
                            extract_required_skills(
                                job_description
                            )
                        )

                        (
                            score,
                            matched_skills,
                            missing_skills
                        ) = calculate_ats_score(
                            active_skills,
                            required_skills
                        )


                        save_ats_analysis(
                            active_resume_id,
                            job_description,
                            score,
                            matched_skills,
                            missing_skills
                        )

                        st.success(
                            "New ATS analysis saved to database."
                        )

                    st.subheader(
                        "ATS Analysis"
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "ATS Match Score",
                        f"{score}%"
                    )

                    col2.metric(
                        "Matched Skills",
                        len(matched_skills)
                    )

                    col3.metric(
                        "Missing Skills",
                        len(missing_skills)
                    )

                    st.progress(
                        int(score) / 100,
                        text=f"ATS Match Score: {score}%"
                    )

                    matched_col, missing_col = (
                        st.columns(2)
                    )

                    with matched_col:

                        st.subheader(
                            "Matched Skills"
                        )

                        if matched_skills:

                            for skill in matched_skills:

                                st.write(
                                    "✓",
                                    skill.title()
                                )
                        else:
                            st.info(
                                "No matching skills found."
                            )

                    with missing_col:
                        st.subheader(
                            "Missing Skills"
                        )

                        if missing_skills:

                            for skill in missing_skills:

                                st.write(
                                    "✗",
                                    skill.title()
                                )
                        else:

                            st.info(
                                "No missing skills."
                            )

                    recommendations = (
                        generate_recommendations(
                            score,
                            matched_skills,
                            missing_skills
                        )
                    )

                    st.subheader(
                        "Recommendations"
                    )

                    for recommendation in recommendations:

                        st.write(
                            "•",
                            recommendation
                        )

                    st.subheader(
                        "ATS Analysis History"
                    )

                    analysis_history = (
                        get_ats_analyses_by_resume_id(
                            active_resume_id
                        )
                    )

                    if analysis_history:

                        for analysis in analysis_history:

                            st.write(
                                f"**Analysis "
                                f"{analysis['analysis_id']}**"
                            )

                            st.write(
                                f"ATS Score: "
                                f"{analysis['ats_score']}%"
                            )

                            st.write(
                                f"Analyzed On: "
                                f"{analysis['analysis_time']}"
                            )

                            st.write(
                                "Matched Skills:",
                                analysis[
                                    "matched_skills"
                                ]
                                if analysis[
                                    "matched_skills"
                                ]
                                else "None"
                            )

                            st.write(
                                "Missing Skills:",
                                analysis[
                                    "missing_skills"
                                ]
                                if analysis[
                                    "missing_skills"
                                ]
                                else "None"
                            )

                            st.divider()
                    else:
                        st.info(
                            "No previous ATS analyses found."
                        )
        else:
            st.error(
                "No readable text found. "
                "The PDF may be scanned."
            )