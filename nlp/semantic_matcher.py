
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading semantic model...")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("Semantic model loaded!\n")


def split_sentences(text):
    """Text ko chotay sentences ya lines mein divide karta hai."""
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)

    sentences = []

    for part in parts:
        part = part.strip()

        if part:
            sentences.append(part)

    return sentences



def find_semantic_evidence(jd_text, cv_text):
    """Har JD sentence ke liye closest CV sentence aur similarity status return karta hai."""

    jd_sentences = split_sentences(jd_text)
    cv_sentences = split_sentences(cv_text)

    if not jd_sentences or not cv_sentences:
        return []

    jd_embeddings = model.encode(jd_sentences)
    cv_embeddings = model.encode(cv_sentences)

    similarity_matrix = cosine_similarity(
        jd_embeddings,
        cv_embeddings
    )

    results = []

    # Initial threshold: testing ke liye
    threshold = 0.60

    for i, jd_sentence in enumerate(jd_sentences):
        best_index = similarity_matrix[i].argmax()
        best_score = float(similarity_matrix[i][best_index])

        if best_score >= threshold:
            status = "potential_match"
        else:
            status = "low_confidence"

        results.append({
            "requirement": jd_sentence,
            "cv_evidence": cv_sentences[best_index],
            "similarity": round(best_score, 4),
            "status": status
        })

    return results


if __name__ == "__main__":
    jd = "Experience developing REST APIs and backend services."

    cv = """
    Built server-side applications and integrated API endpoints.
    Designed social media posts and managed marketing campaigns.
    """

   
    evidence = find_semantic_evidence(jd, cv)

    for item in evidence:
        print("Requirement:", item["requirement"])
        print("CV Evidence:", item["cv_evidence"])
        print("Similarity:", item["similarity"])
        print("Status:", item["status"])
        print()

