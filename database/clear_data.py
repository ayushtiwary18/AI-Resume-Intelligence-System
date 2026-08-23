from database.connection import get_connection


def clear_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Delete extracted data first because it depends on resumes
    cursor.execute("DELETE FROM extracted_resume_data")

    # Delete resume records
    cursor.execute("DELETE FROM resumes")

    conn.commit()
    conn.close()

    print("All resume data deleted successfully!")


if __name__ == "__main__":
    clear_data()