from extractor import extract_text_info
from semantic_matcher import find_semantic_evidence


def match_candidate(jd_text, cv_text):
    """
    JD aur CV ko match karta hai aur score deta hai
    """
    
    semantic_evidence = find_semantic_evidence(jd_text, cv_text)

    jd_info = extract_text_info(jd_text)
    cv_info = extract_text_info(cv_text)
    
    # 1. Skills matching
    jd_skills = set(jd_info["skills"])
    cv_skills = set(cv_info["skills"])
    
    matched_skills = jd_skills.intersection(cv_skills)
    missing_skills = jd_skills - cv_skills
    
    # Skills score — kitne % skills match hue
    if len(jd_skills) > 0:
        skills_score = len(matched_skills) / len(jd_skills) * 100
    else:
        skills_score = 0
    
    # 2. Experience matching
    jd_exp = int(jd_info["experience_years"][0]) if jd_info["experience_years"] else 0
    cv_exp = int(cv_info["experience_years"][0]) if cv_info["experience_years"] else 0
    
    if cv_exp >= jd_exp:
        experience_score = 100
    elif jd_exp > 0:
        experience_score = (cv_exp / jd_exp) * 100
    else:
        experience_score = 0
    
    # 3. Education matching
    jd_edu = set(jd_info["education"])
    cv_edu = set(cv_info["education"])
    matched_edu = jd_edu.intersection(cv_edu)
    education_score = 100 if matched_edu else 0
    
    # 4. Final score — weighted
    final_score = (
        skills_score * 0.6 +      # Skills 60% weight
        experience_score * 0.3 +   # Experience 30% weight
        education_score * 0.1      # Education 10% weight
    )
    
    return {
        "final_score": round(final_score, 2),
        "skills_score": round(skills_score, 2),
        "experience_score": round(experience_score, 2),
        "education_score": round(education_score, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "semantic_evidence": semantic_evidence
    }


def rank_candidates(jd_text, candidates):
    """
    Multiple candidates ko rank karta hai
    candidates = list of dicts: [{"name": "Ali", "cv": "..."}]
    """
    results = []
    
    for candidate in candidates:
        score = match_candidate(jd_text, candidate["cv"])
        results.append({
            "name": candidate["name"],
            **score
        })
    
    # Score ke hisaab se sort karo — highest first
    ranked = sorted(results, key=lambda x: x["final_score"], reverse=True)
    
    # Top 10 return karo
    return ranked[:10]


# Test karo
if __name__ == "__main__":
    
    jd = """
    We need a Python Developer with 3 years of experience.
    Skills required: Python, Machine Learning, NLP, FastAPI, SQL.
    Bachelor degree in Computer Science required.
    """
    
    candidates = [
        {
            "name": "Ahmed Ali",
            "cv": "Python developer, 4 years experience. Skills: Python, Machine Learning, NLP, SQL, Docker. BS Computer Science."
        },
        {
            "name": "Sara Khan", 
            "cv": "Frontend developer, 2 years experience. Skills: React, JavaScript, MongoDB. Bachelor degree."
        },
        {
            "name": "Usman Malik",
            "cv": "Data scientist, 3 years experience. Skills: Python, Machine Learning, NLP, FastAPI, SQL, TensorFlow. BS degree."
        },
        {
            "name": "Ayesha Raza",
            "cv": "Backend developer, 1 year experience. Skills: Python, FastAPI, SQL. BS Computer Science."
        },
        {
            "name": "Bilal Ahmed",
            "cv": "ML Engineer, 5 years experience. Skills: Python, Machine Learning, Deep Learning, NLP, FastAPI, SQL, AWS. Master degree."
        }
    ]
    
    
    print("=== Ranked Candidates ===\n")
    ranked = rank_candidates(jd, candidates)

    for i, candidate in enumerate(ranked, 1):
        print(f"Rank {i}: {candidate['name']}")
        print(f"  Final Score: {candidate['final_score']}%")
        print(f"  Skills Match: {candidate['skills_score']}%")
        print(f"  Experience: {candidate['experience_score']}%")
        print(f"  Matched Skills: {candidate['matched_skills']}")
        print(f"  Missing Skills: {candidate['missing_skills']}")

        print("\n  Semantic Evidence:")

        for item in candidate["semantic_evidence"]:
            print("    Requirement:", item["requirement"])
            print("    CV Evidence:", item["cv_evidence"])
            print("    Similarity:", item["similarity"])

        print()
