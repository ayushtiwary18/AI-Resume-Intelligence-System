from database.connection import get_connection


def save_resume(
    original_filename,
    stored_filename,
    file_path, 
    file_hash
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resumes
        (original_filename, stored_filename, file_path, file_hash)
        VALUES (?, ?, ?, ?)
    """, (
        original_filename,
        stored_filename,
        file_path,
        file_hash
    ))

    conn.commit()

    resume_id = cursor.lastrowid

    conn.close()

    return resume_id

def get_resume_by_hash(file_hash):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
            "SELECT * FROM resumes WHERE file_hash = ?",
            (file_hash,)
        )

    resume = cursor.fetchone()

    conn.close()

    return resume

def save_extracted_data(
    resume_id,
    name,
    email,
    phone,
    skills,
    education,
    experience
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO extracted_resume_data
        (
            resume_id,
            name,
            email,
            phone,
            skills,
            education,
            experience
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        resume_id,
        name,
        email,
        phone,
        ", ".join(skills),
        ", ".join(education),
        ", ".join(experience)
    ))

    conn.commit()
    conn.close()

def get_extracted_data_by_resume_id(resume_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM extracted_resume_data WHERE resume_id = ?",
        (resume_id,)
    )

    data = cursor.fetchone()

    conn.close()

    return data