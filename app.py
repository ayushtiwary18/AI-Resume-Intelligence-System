import streamlit as st
import os
import uuid

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

    from database.operations import save_resume
    save_resume(
        uploaded_file.name,
        unique_filename,
        file_path
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Resume uploaded and saved successfully!")

    st.write("Original Filename:", uploaded_file.name)
    st.write("Stored Filename:", unique_filename)
    st.code(file_path)