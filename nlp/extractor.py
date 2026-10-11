
import re

SKILLS = [
    # Programming
    "python", "java", "javascript", "typescript", "c++", "c#",
    "php", "ruby",
    # Web
    "react", "node.js", "html", "css", "angular", "vue",
    # Backend
    "fastapi", "django", "flask", "spring boot", "express",
    "express.js",
    # Database
    "mongodb", "sql", "postgresql", "mysql", "firebase",
    # AI/ML
    "machine learning", "deep learning", "nlp", "tensorflow",
    "pytorch", "data analysis", "pandas", "numpy", "scikit-learn",
    # Cloud/DevOps
    "aws", "docker", "git", "linux", "azure",
]
SKILL_ALIASES = {
    "js": "javascript",
    "node": "node.js",
    "react.js": "react",
    "expressjs": "express.js",
    "postgres": "postgresql",
    "scikit learn": "scikit-learn",
    "ml": "machine learning",
}
SOFT_SKILLS = [
    "communication", "teamwork", "leadership", "problem solving",
    "time management", "project management"
]


DEGREE_SUBJECTS = [
    "computer science",
    "software engineering",
    "information technology",
    "information systems",
    "data science",
    "artificial intelligence",
    "computer engineering",
    "electrical engineering",
    "business administration",
    "mathematics",
    "statistics",
    "fine arts"
]

def contains_skill(text, skill):
    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(skill)
        + r"(?![a-z0-9])"
    )
    return re.search(pattern, text, re.IGNORECASE) is not None


def extract_text_info(text):
    text_lower = text.lower()

    # 1. Technical skills with aliases
    found_skills = []

    for skill in SKILLS:
        if contains_skill(text_lower, skill):
            found_skills.append(skill)

    for alias, canonical_skill in SKILL_ALIASES.items():
        if contains_skill(text_lower, alias):
            if canonical_skill not in found_skills:
                found_skills.append(canonical_skill)


    # 2. Soft skills alag
    found_soft_skills = []
    for skill in SOFT_SKILLS:
        if contains_skill(text_lower, skill):
            found_soft_skills.append(skill)

    # 3. Experience
    experience_pattern = (
        r"\b(\d+)\s*\+?\s*years?"
        r"(?:\s+of)?\s+experience\b"
    )
    experience = re.findall(experience_pattern, text_lower)

    # 4. Education level
    education_patterns = {
        "bachelor": [
            r"\bbachelor(?:'s)?\b",
            r"\bbs\b",
            r"\bb\.?\s*sc\b",
            r"\bb\.?\s*eng\b"
        ],
        "master": [
            r"\bmaster(?:'s)?\b",
            r"\bms\b",
            r"\bm\.?\s*sc\b",
            r"\bm\.?\s*phil\b"
        ],
        "phd": [
            r"\bph\.?\s*d\.?\b",
            r"\bdoctorate\b"
        ],
        "mba": [
            r"\bmba\b"
        ]
    }

    found_education = []
    for category, patterns in education_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                found_education.append(category)
                break

    # 5. Education subject
    found_subjects = []
    for subject in DEGREE_SUBJECTS:
        if contains_skill(text_lower, subject):
            found_subjects.append(subject)

    return {
        "skills": found_skills,
        "soft_skills": found_soft_skills,
        "experience_years": experience,
        "education": found_education,
        "education_subjects": found_subjects
    }

if __name__ == "__main__":

    test_cases = [
        (
            "CS degree",
            "Bachelor degree in Computer Science.",
            ["bachelor"],
            ["computer science"]
        ),
        (
            "Software Engineering degree",
            "BS in Software Engineering.",
            ["bachelor"],
            ["software engineering"]
        ),
        (
            "Degree without subject",
            "I have a Bachelor degree.",
            ["bachelor"],
            []
        ),
        (
            "Data Science master's",
            "Master degree in Data Science.",
            ["master"],
            ["data science"]
        )
    ]

    for name, text, expected_education, expected_subjects in test_cases:
        result = extract_text_info(text)

        print(f"\nTest: {name}")
        print("Education:", result["education"])
        print("Education subjects:", result["education_subjects"])

        assert result["education"] == expected_education, (
            f"Education test failed: {name}"
        )

        assert result["education_subjects"] == expected_subjects, (
            f"Subject test failed: {name}"
        )

        print("PASS")
