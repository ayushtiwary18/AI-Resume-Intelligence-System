def calculate_hybrid_match_score(
    ats_score,
    semantic_similarity,
    skill_weight=0.7,
    semantic_weight=0.3
):
    """
    Calculate a hybrid resume-JD matching score
    using ATS skill matching and semantic similarity.
    """

    if ats_score < 0 or semantic_similarity < 0:
        return 0.0

    if ats_score > 100 or semantic_similarity > 100:
        return 0.0

    total_weight = skill_weight + semantic_weight

    if total_weight == 0:
        return 0.0

    hybrid_score = (
        ats_score * skill_weight
        + semantic_similarity * semantic_weight
    ) / total_weight

    return round(hybrid_score, 2)