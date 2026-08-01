from database.connection import get_connection


def save_resume(original_filename, stored_filename, file_path):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resumes
        (original_filename, stored_filename, file_path)
        VALUES (?, ?, ?)
    """, (
        original_filename,
        stored_filename,
        file_path
    ))

    conn.commit()
    conn.close()