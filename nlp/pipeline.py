import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from file_reader import read_folder
from match import rank_candidates


def load_candidates_from_folder(folder_path):
    candidates = []

    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return candidates

    # read_folder dict return karta hai {filename: text}
    cv_data = read_folder(folder_path)

    for filename, text in cv_data.items():
        if text and text.strip():
            name = os.path.splitext(filename)[0].replace("_", " ")
            candidates.append({
                "name": name,
                "cv": text,
                "file": filename
            })
            print(f"  Loaded: {filename}")

    return candidates

    
def run_pipeline(jd_text, cv_folder):
    print("\n" + "=" * 60)
    print("APEX SOURCING PIPELINE")
    print("=" * 60)

    print(f"\nLoading CVs from: {cv_folder}")
    candidates = load_candidates_from_folder(cv_folder)

    if not candidates:
        print("No CVs found. Exiting.")
        return []

    print(f"Total CVs loaded: {len(candidates)}")
    print("\nRunning matching and ranking...")

    ranked = rank_candidates(jd_text, candidates)

    print("\n" + "=" * 60)
    print("RANKED RESULTS")
    print("=" * 60)

    for i, c in enumerate(ranked, 1):
        icon = "✓" if c["candidate_status"] == "scored" else "?"
        print(f"\nRank {i} {icon} | {c['name']}")
        print(f"  File            : {c.get('file', 'N/A')}")
        print(f"  Final Score     : {c['final_score']}%")
        print(f"  Status          : {c['candidate_status']}")
        print(f"  Skills Score    : {c['skills_score']}%")
        print(f"  Experience Score: {c['experience_score']}%")
        print(f"  Education Status: {c['education_status']}")
        print(f"  Matched Skills  : {c['matched_skills']}")
        print(f"  Missing Skills  : {c['missing_skills']}")

    return ranked


if __name__ == "__main__":

    jd = """
    We are looking for a Senior Python Developer with 4 years of experience.
    Skills required: Python, FastAPI, Machine Learning, SQL, Docker, Git.
    Bachelor degree in Computer Science or Software Engineering required.
    Strong problem solving and communication skills needed.
    """

    cv_folder = os.path.join(
        os.path.dirname(__file__), "..", "data", "cvs"
    )

    results = run_pipeline(jd, cv_folder)
    print(f"\nTotal candidates ranked: {len(results)}")