from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_semantic_similarity(resume_text, job_description):
    """
    Calculate semantic similarity between resume text
    and job description using TF-IDF and cosine similarity.
    """

    if not resume_text or not job_description:
        return 0.0

    resume_text = resume_text.strip()
    job_description = job_description.strip()

    if not resume_text or not job_description:
        return 0.0

    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)