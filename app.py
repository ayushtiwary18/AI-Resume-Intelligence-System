import streamlit as st
import os
import uuid

from database.operations import save_resume
from resume_parser.extractor import extract_text
from preprocessing.cleaner import clean_text
from resume_parser.info_extractor import (
    extract_email,
    extract_phone,
    extract_name
)

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

    unique_filename = f"{uuid.uuid4()}.pdf"

    file_path = os.path.join(
        upload_folder,
        unique_filename
    )

    # Save PDF first
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Save metadata
    save_resume(
        uploaded_file.name,
        unique_filename,
        file_path
    )

    # Extract text
    resume_text = extract_text(file_path)

    st.success("Resume uploaded and saved successfully!")

    st.write("Original Filename:", uploaded_file.name)
    st.write("Stored Filename:", unique_filename)
    st.code(file_path)

    resume_text = extract_text(file_path)
    cleaned_text = clean_text(resume_text)

    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    name = extract_name(resume_text)

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

    else:
        st.error("No readable text found. The PDF may be scanned.")