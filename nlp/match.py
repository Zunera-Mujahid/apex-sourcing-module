from extractor import extract_text_info
from semantic_matcher import find_semantic_evidence


EDUCATION_LEVELS = {
    "bachelor": 1,
    "master": 2,
    "phd": 3
}


def check_education(required_education, candidate_education,
                    required_subjects, candidate_subjects):
    if not required_education:
        return "not_required", None

    if not candidate_education:
        return "manual_review", None

    for required in required_education:
        if required in EDUCATION_LEVELS:
            required_level = EDUCATION_LEVELS[required]
            candidate_meets_level = False

            for candidate_degree in candidate_education:
                if candidate_degree in EDUCATION_LEVELS:
                    if EDUCATION_LEVELS[candidate_degree] >= required_level:
                        candidate_meets_level = True
                        break

            if not candidate_meets_level:
                return "mismatch", 0
        else:
            if required not in candidate_education:
                return "mismatch", 0

    if not required_subjects:
        return "verified_match", 100

    if not candidate_subjects:
        return "manual_review", None

    if set(required_subjects).intersection(candidate_subjects):
        return "verified_match", 100

    return "mismatch", 0


def match_candidate(jd_text, cv_text):

    # 1. Extract info
    jd_info = extract_text_info(jd_text)
    cv_info = extract_text_info(cv_text)

    # 2. Technical skills matching
    jd_skills = set(jd_info["skills"])
    cv_skills = set(cv_info["skills"])

    matched_skills = jd_skills.intersection(cv_skills)
    missing_skills = jd_skills - cv_skills

    if jd_skills:
        skills_score = (len(matched_skills) / len(jd_skills)) * 100
    else:
        skills_score = None

    # 3. Soft skills matching
    jd_soft = set(jd_info["soft_skills"])
    cv_soft = set(cv_info["soft_skills"])

    matched_soft = jd_soft.intersection(cv_soft)

    if jd_soft:
        soft_score = (len(matched_soft) / len(jd_soft)) * 100
    else:
        soft_score = None

    # 4. Experience matching
    jd_exp = (
        int(jd_info["experience_years"][0])
        if jd_info["experience_years"]
        else None
    )
    cv_exp = (
        int(cv_info["experience_years"][0])
        if cv_info["experience_years"]
        else None
    )

    if jd_exp is None:
        experience_score = None
    elif cv_exp is None:
        experience_score = 0
    elif cv_exp >= jd_exp:
        experience_score = 100
    elif jd_exp > 0:
        experience_score = (cv_exp / jd_exp) * 100
    else:
        experience_score = None

    # 5. Education matching
    jd_education = set(jd_info["education"])
    cv_education = set(cv_info["education"])
    jd_subjects = set(jd_info["education_subjects"])
    cv_subjects = set(cv_info["education_subjects"])

    education_status, education_score = check_education(
        jd_education, cv_education,
        jd_subjects, cv_subjects
    )

    if education_status == "verified_match":
        matched_education = sorted(jd_education)
        missing_education = []
    elif education_status == "mismatch":
        matched_education = []
        missing_education = sorted(jd_education)
    else:
        matched_education = []
        missing_education = sorted(jd_education)

    # 6. Semantic evidence
    semantic_evidence = find_semantic_evidence(jd_text, cv_text)

    potential_matches = [
        item for item in semantic_evidence
        if item["status"] == "potential_match"
    ]

    if semantic_evidence:
        semantic_score = (
            len(potential_matches) / len(semantic_evidence)
        ) * 100
    else:
        semantic_score = None

    # 7. Final score — soft skills 10%, technical 55%
    criteria = [
        (skills_score, 0.55),
        (experience_score, 0.25),
        (education_score, 0.10),
        (soft_score, 0.10),
    ]

    available_criteria = [
        (score, weight)
        for score, weight in criteria
        if score is not None
    ]

    if available_criteria:
        total_weight = sum(
            weight for score, weight in available_criteria
        )
        final_score = sum(
            score * weight
            for score, weight in available_criteria
        ) / total_weight
    else:
        final_score = None

    
    if education_status == "mismatch":
        candidate_status = "education_mismatch"
    elif education_status == "manual_review":
        candidate_status = "manual_review"
    elif final_score is None:
        candidate_status = "insufficient_data"
    else:
        candidate_status = "scored"

    return {
        "final_score": (
            round(final_score, 2) if final_score is not None else None
        ),
        "candidate_status": candidate_status,
        "skills_score": (
            round(skills_score, 2) if skills_score is not None else None
        ),
        "soft_skills_score": (
            round(soft_score, 2) if soft_score is not None else None
        ),
        "experience_score": (
            round(experience_score, 2)
            if experience_score is not None else None
        ),
        "education_score": education_score,
        "education_status": education_status,
        "required_education": sorted(jd_education),
        "candidate_education": sorted(cv_education),
        "required_subjects": sorted(jd_subjects),
        "candidate_subjects": sorted(cv_subjects),
        "matched_education": matched_education,
        "missing_education": missing_education,
        "semantic_score": (
            round(semantic_score, 2)
            if semantic_score is not None else None
        ),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "matched_soft_skills": sorted(matched_soft),
        "missing_soft_skills": sorted(jd_soft - cv_soft),
        "semantic_evidence": semantic_evidence
    }
def sort_by_score(candidates):
    candidates.sort(
        key=lambda c: (
            c["final_score"] is not None,
            c["final_score"] if c["final_score"] is not None else 0
        ),
        reverse=True
    )

def rank_candidates(jd_text, candidates):

    results = []

    for candidate in candidates:
        score = match_candidate(jd_text, candidate["cv"])
        results.append({
            "name": candidate["name"],
            **score
        })

    verified_candidates = []
    review_candidates = []
    other_candidates = []

    for candidate in results:
        if candidate["candidate_status"] == "manual_review":
            review_candidates.append(candidate)
        elif candidate["candidate_status"] == "scored":
            verified_candidates.append(candidate)
        else:
            other_candidates.append(candidate)


    sort_by_score(verified_candidates)
    sort_by_score(review_candidates)
    sort_by_score(other_candidates)

    ranked = verified_candidates + review_candidates + other_candidates

    return ranked

    
# SEMANTIC SCORE POLICY:
# semantic_score is report-only and is not included in final_score.
# final_score is calculated using skills, experience, education,
# and soft skills according to the configured weights.
# Semantic similarity alone does not verify a candidate's
# actual skills or educational qualifications.

