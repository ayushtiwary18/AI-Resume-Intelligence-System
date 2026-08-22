import streamlit as st
import os
import uuid
import hashlib

from database.operations import (
    save_resume,
    get_resume_by_hash
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
#from resume_parser.experience_extractor import extract_experience

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
        save_resume(
            uploaded_file.name,
            unique_filename,
            file_path,
            file_hash
        )

        st.success("Resume uploaded and saved successfully!")

    # Extract text
    resume_text = extract_text(file_path)
    cleaned_text = clean_text(resume_text)

    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    name = extract_name(resume_text)

    skills = extract_skills(cleaned_text)
    education = extract_education(cleaned_text)
    #experience = extract_experience(cleaned_text)

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

        # st.subheader("Experience")
        # if experience:
        #     for item in experience:
        #         st.write("•", item)
        # else:
        #     st.warning("No experience duration found.")

    else:
        st.error("No readable text found. The PDF may be scanned.")