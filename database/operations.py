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

def save_ats_analysis(
    resume_id,
    job_description,
    ats_score,
    matched_skills,
    missing_skills
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ats_analysis
        (
            resume_id,
            job_description,
            ats_score,
            matched_skills,
            missing_skills
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        resume_id,
        job_description,
        ats_score,
        ", ".join(matched_skills),
        ", ".join(missing_skills)
    ))

    conn.commit()
    conn.close()

def get_existing_ats_analysis(resume_id, job_description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM ats_analysis
        WHERE resume_id = ?
        AND job_description = ?
        ORDER BY analysis_id DESC
        LIMIT 1
    """, (
        resume_id,
        job_description
    ))

    analysis = cursor.fetchone()

    conn.close()

    return analysis

def get_ats_analyses_by_resume_id(resume_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            analysis_id,
            job_description,
            ats_score,
            matched_skills,
            missing_skills,
            analysis_time
        FROM ats_analysis
        WHERE resume_id = ?
        ORDER BY analysis_time DESC
    """, (resume_id,))

    analyses = cursor.fetchall()

    conn.close()

    return analyses

def get_all_resumes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            resume_id,
            original_filename,
            stored_filename,
            file_path,
            upload_time
        FROM resumes
        ORDER BY upload_time DESC
    """)

    resumes = cursor.fetchall()

    conn.close()

    return resumes