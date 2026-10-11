from match import rank_candidates, match_candidate, sort_by_score
from extractor import extract_text_info

alias_tests = [
    ("I use JS for frontend development", "javascript", True),
    ("I use JavaScript for frontend development", "javascript", True),
    ("I use Node for backend development", "node.js", True),
    ("I use React.js for UI development", "react", True),
    ("I use PostgreSQL for databases", "postgresql", True),
    ("I use scikit learn for machine learning", "scikit-learn", True),
    ("I use ML for prediction", "machine learning", True),
    ("I know Java programming", "javascript", False),
]
# ── Issue 6: End-to-End Alias Matching Tests ──────────────────────────

print("\n=== ISSUE 6: END-TO-END MATCHING TESTS ===")

matching_tests = [
    {
        "name": "JS matches JavaScript",
        "jd": "Required skill: JavaScript.",
        "cv": "I have experience using JS.",
        "expected_score": 100.0,
    },
    {
        "name": "Java does not match JavaScript",
        "jd": "Required skill: JavaScript.",
        "cv": "I have experience using Java.",
        "expected_score": 0.0,
    },
]

for test in matching_tests:
    result = match_candidate(test["jd"], test["cv"])

    actual_score = result["skills_score"]

    assert actual_score == test["expected_score"], (
        f"FAIL: {test['name']} | "
        f"Expected {test['expected_score']}%, got {actual_score}%"
    )

    print(f"PASS: {test['name']}")
    print("  Matched skills:", result["matched_skills"])
    print("  Missing skills:", result["missing_skills"])
    print("  Skills score:", actual_score)
print("\n=== ISSUE 6: SKILL ALIAS TESTS ===")

for text, expected_skill, should_match in alias_tests:
    result = extract_text_info(text)
    found = expected_skill in result["skills"]

    assert found == should_match, (
        f"FAIL: '{text}' | expected {expected_skill} "
        f"match={should_match}, got {found}"
    )

    print(f"PASS: {text} -> {expected_skill}: {found}")

education_tests = [
    "Bachelor of Science in Computer Science",
    "BS Computer Science",
    "Bachelor of Software Engineering",
    "Master of Data Science",
    "Bachelor of Fine Arts",
    "Bachelor of Information Technology",
    "Bachelor of Statistics",
]

print("\n=== EDUCATION SUBJECT EXTRACTION TEST ===")

for education_text in education_tests:
    result = extract_text_info(education_text)

    print("\nInput:", education_text)
    print("Education:", result["education"])
    print("Subjects:", result["education_subjects"])

# ── Job Description ───────────────────────────────────────────────────────────
jd = """
We are looking for a Senior Python Developer with 4 years of experience.
Skills required: Python, FastAPI, Machine Learning, SQL, Docker, Git.
Bachelor degree in Computer Science or Software Engineering required.
Strong problem solving and communication skills needed.
"""

# ── Candidates ────────────────────────────────────────────────────────────────
candidates = [
    {
        "name": "Ali Hassan",
        "cv": """
        Senior Python Developer with 5 years of experience.
        Skills: Python, FastAPI, Machine Learning, SQL, Docker, Git, AWS.
        BS Computer Science from FAST University.
        Strong problem solving and communication skills.
        Led backend team of 4 engineers.
        """
    },
    {
        "name": "Sana Malik",
        "cv": """
        Data Scientist with 3 years of experience.
        Skills: Python, Machine Learning, Deep Learning, Pandas, NumPy, SQL.
        MS Data Science from LUMS.
        Good communication and teamwork skills.
        """
    },
    {
        "name": "Usman Tariq",
        "cv": """
        Full Stack Developer with 4 years of experience.
        Skills: React, Node.js, MongoDB, JavaScript, Git, Docker.
        BS Software Engineering from UET.
        Strong problem solving skills.
        """
    },
    {
        "name": "Ayesha Noor",
        "cv": """
        Backend Developer with 2 years of experience.
        Skills: Python, FastAPI, SQL, Git.
        BS Computer Science from UCP.
        Good communication skills.
        """
    },
    {
        "name": "Bilal Chaudhry",
        "cv": """
        ML Engineer with 6 years of experience.
        Skills: Python, Machine Learning, Deep Learning, TensorFlow,
        PyTorch, Docker, Git, SQL, FastAPI.
        PhD Computer Science from NUST.
        Excellent problem solving and leadership skills.
        """
    },
    {
        "name": "Zara Ahmed",
        "cv": """
        Graphic Designer with 3 years of experience.
        Skills: Photoshop, Illustrator, Figma, CorelDraw.
        Bachelor degree in Fine Arts.
        Good communication and teamwork skills.
        """
    },
    {
        "name": "Hassan Raza",
        "cv": """
        Junior Python Developer with 1 year of experience.
        Skills: Python, SQL, Git, Flask.
        BS Computer Science from Punjab University.
        Eager to learn and good problem solving skills.
        """
    },
    {
        "name": "Maham Iqbal",
        "cv": """
        DevOps Engineer with 4 years of experience.
        Skills: Docker, Git, Linux, AWS, Azure, Python, SQL.
        BS Software Engineering from COMSATS.
        Strong problem solving and project management skills.
        """
    },
    {
        "name": "Farhan Shah",
        "cv": """
        Accountant with 5 years of experience.
        Skills: Excel, QuickBooks, Financial Reporting, Taxation.
        MBA from IBA Karachi.
        Good communication and time management skills.
        """
    },
    {
        "name": "Nimra Butt",
        "cv": """
        Python Developer with 4 years of experience.
        Skills: Python, FastAPI, Machine Learning, SQL, Git, Docker.
        BS Computer Science from GIKI.
        Strong communication and problem solving skills.
        """
    },
    {
        "name": "Omer Khalid",
        "cv": """
        Data Analyst with 2 years of experience.
        Skills: Python, SQL, Pandas, Data Analysis, Excel, Git.
        BS Statistics from Karachi University.
        Good communication skills.
        """
    },
    {
        "name": "Hina Javed",
        "cv": """
        HR Manager with 7 years of experience.
        Skills: Recruitment, HR Management, Communication,
        Leadership, Time Management.
        MBA Human Resources from UMT.
        Excellent teamwork and project management skills.
        """
    }
]

# ── Run Test ──────────────────────────────────────────────────────────────────
print("=" * 60)
print("APEX SOURCING MODULE — FULL PIPELINE TEST")
print("=" * 60)
print(f"\nTotal candidates: {len(candidates)}")
print(f"JD: Senior Python Developer | 4 years | CS degree\n")
print("=" * 60)


# ── Issue 5: Sorting Consistency Tests ────────────────────────────────

print("\n=== ISSUE 5: SORTING CONSISTENCY TESTS ===")

test_scores = [
    {"name": "Candidate A", "final_score": 70.0},
    {"name": "Candidate B", "final_score": None},
    {"name": "Candidate C", "final_score": 90.0},
    {"name": "Candidate D", "final_score": 70.0},
    {"name": "Candidate E", "final_score": None},
]

sort_by_score(test_scores)

sorted_names = [c["name"] for c in test_scores]

expected_names = [
    "Candidate C",
    "Candidate A",
    "Candidate D",
    "Candidate B",
    "Candidate E",
]

assert sorted_names == expected_names, (
    f"Sorting failed. Actual order: {sorted_names}"
)

print("PASS: Scores are sorted in descending order.")
print("PASS: None scores appear after numeric scores.")
print("PASS: Equal scores preserve their original order.")
print("Sorted order:", sorted_names)

ranked = rank_candidates(jd, candidates)


# ISSUE 7: Candidate count, uniqueness, and status validation

print("\n=== ISSUE 7: RANKING AND STATUS TESTS ===")

# 1. Every input candidate must be returned.
assert len(ranked) == len(candidates), (
    f"Expected {len(candidates)} candidates, got {len(ranked)}"
)
print("PASS: Every candidate is returned.")

# 2. No candidate should appear more than once.
input_names = [c["name"] for c in candidates]
ranked_names = [c["name"] for c in ranked]

assert len(ranked_names) == len(set(ranked_names)), (
    "Duplicate candidates found in ranked results."
)
assert sorted(ranked_names) == sorted(input_names), (
    "Input and ranked candidate names do not match."
)
print("PASS: No candidates are missing or duplicated.")

# 3. Verify group ordering.
status_order = {
    "scored": 0,
    "manual_review": 1,
    "education_mismatch": 2,
}

positions = [
    status_order.get(c["candidate_status"], 3)
    for c in ranked
]

assert positions == sorted(positions), (
    "Candidate status groups are not in the expected order."
)
print("PASS: Candidate groups appear in the expected order.")

# 4. Verify that each candidate's status is recognized.
allowed_statuses = {
    "scored",
    "manual_review",
    "education_mismatch",
    "insufficient_data",
}

for candidate in ranked:
    assert candidate["candidate_status"] in allowed_statuses, (
        f"Unexpected status for {candidate['name']}: "
        f"{candidate['candidate_status']}"
    )

print("PASS: Every candidate has a recognized status.")
print("Total candidates verified:", len(ranked))


# Issue 5: End-to-end group sorting verification

print("\n=== ISSUE 5: GROUP SORTING VERIFICATION ===")

groups = {
    "scored": [],
    "manual_review": [],
    "education_mismatch": [],
    "other": [],
}

for candidate in ranked:
    status = candidate["candidate_status"]

    if status == "scored":
        groups["scored"].append(candidate)
    elif status == "manual_review":
        groups["manual_review"].append(candidate)
    elif status == "education_mismatch":
        groups["education_mismatch"].append(candidate)
    else:
        groups["other"].append(candidate)

for group_name, group_candidates in groups.items():
    scores = [
        c["final_score"]
        for c in group_candidates
        if c["final_score"] is not None
    ]

    assert scores == sorted(scores, reverse=True), (
        f"FAIL: {group_name} group is not sorted descending: {scores}"
    )

    print(f"PASS: {group_name} group scores are descending")

    none_seen = False

    for candidate in group_candidates:
        if candidate["final_score"] is None:
            none_seen = True
        elif none_seen:
            raise AssertionError(
                f"FAIL: Numeric score appears after None in {group_name}"
            )

    print(f"PASS: {group_name} handles missing scores correctly")

print("Total ranked candidates:", len(ranked))


# Verify education mismatch for ALL candidates
print("\n=== EDUCATION MISMATCH CHECK ===")

for candidate in candidates:
    result = match_candidate(jd, candidate["cv"])

    print("\nCandidate:", candidate["name"])
    print("Required education:", result["required_education"])
    print("Candidate education:", result["candidate_education"])
    print("Required subjects:", result["required_subjects"])
    print("Candidate subjects:", result["candidate_subjects"])
    print("Education status:", result["education_status"])
    print("Candidate status:", result["candidate_status"])


# ── Candidate Results by Status ─────────────────────────────────────────

scored_candidates = []
manual_review_candidates = []
mismatch_candidates = []
other_candidates = []

for c in ranked:
    if c["candidate_status"] == "scored":
        scored_candidates.append(c)
    elif c["candidate_status"] == "manual_review":
        manual_review_candidates.append(c)
    elif c["candidate_status"] == "education_mismatch":
        mismatch_candidates.append(c)
    else:
        other_candidates.append(c)


def print_candidates(title, candidate_list):
    print(f"\n=== {title} ({len(candidate_list)}) ===\n")

    if not candidate_list:
        print("No candidates in this category.\n")
        return

    for i, c in enumerate(candidate_list, 1):
        print(f"{i}. {c['name']}")
        print(f"   Final Score      : {c['final_score']}%")
        print(f"   Status           : {c['candidate_status']}")
        print(f"   Skills Score     : {c['skills_score']}%")
        print(f"   Experience Score : {c['experience_score']}%")
        print(f"   Education Status : {c['education_status']}")
        print(f"   Matched Skills   : {c['matched_skills']}")
        print(f"   Missing Skills   : {c['missing_skills']}")
        print()


print_candidates("SCORED CANDIDATES", scored_candidates)
print_candidates("MANUAL REVIEW REQUIRED", manual_review_candidates)
print_candidates("EDUCATION MISMATCH", mismatch_candidates)
print_candidates("OTHER CANDIDATES", other_candidates)

# ── Sanity Checks ─────────────────────────────────────────────────────────────
print("=" * 60)
print("SANITY CHECKS")
print("=" * 60)

top_names = [c["name"] for c in ranked]

# Graphic designer aur accountant neeche hone chahiye
irrelevant = ["Zara Ahmed", "Farhan Shah", "Hina Javed"]
relevant_top3 = ["Ali Hassan", "Bilal Chaudhry", "Nimra Butt"]

print("\nIrrelevant candidates (should rank low):")
for name in irrelevant:
    if name in top_names:
        pos = top_names.index(name) + 1
        icon = "✓ LOW" if pos >= 7 else "✗ TOO HIGH"
        print(f"  {icon} | {name} at Rank {pos}")

print("\nRelevant candidates (should rank high):")
for name in relevant_top3:
    if name in top_names:
        pos = top_names.index(name) + 1
        icon = "✓ HIGH" if pos <= 4 else "✗ TOO LOW"
        print(f"  {icon} | {name} at Rank {pos}")