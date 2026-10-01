from ats.hybrid_matcher import calculate_hybrid_match_score


ats_score = 92.86
semantic_similarity = 52.53

hybrid_score = calculate_hybrid_match_score(
    ats_score,
    semantic_similarity
)

print("ATS Score:", ats_score)
print("Semantic Similarity:", semantic_similarity)
print("Hybrid Match Score:", hybrid_score)