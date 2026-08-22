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
    conn.close()

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