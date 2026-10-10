import spacy
import re

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Common skills list - baad mein expand karein ge
SKILLS = [
    "python", "java", "javascript", "react", "node.js", "mongodb",
    "sql", "machine learning", "deep learning", "nlp", "fastapi",
    "docker", "git", "aws", "tensorflow", "pytorch", "data analysis",
    "communication", "teamwork", "leadership", "problem solving"
]

def extract_text_info(text):
    """
    import info from JD or CV text. Extract skills, experience, and education.
    """
    text_lower = text.lower()
    doc = nlp(text)
    
    # 1. Skills extract karo
    found_skills = []
    for skill in SKILLS:
        if skill in text_lower:
            found_skills.append(skill)
    
    # 2. Experience extract karo (e.g. "3 years", "2+ years")
    experience_pattern = r'(\d+)\+?\s*years?\s*(?:of\s*)?experience'
    experience = re.findall(experience_pattern, text_lower)
    
    # 3. Education extract karo
    education_keywords = ["bachelor", "master", "phd", "bs", "ms", "mba", "degree"]
    found_education = []
    for edu in education_keywords:
        if edu in text_lower:
            found_education.append(edu)
    
    return {
        "skills": found_skills,
        "experience_years": experience,
        "education": found_education
    }


# Test karo
if __name__ == "__main__":
    
    # Sample JD
    sample_jd = """
    We are looking for a Python Developer with 3 years of experience.
    Must know Machine Learning, NLP, and FastAPI.
    Bachelor's degree in Computer Science required.
    Good communication and teamwork skills needed.
    """
    
    # Sample CV
    sample_cv = """
    I am a software engineer with 2 years of experience.
    Skills: Python, React, MongoDB, SQL, Machine Learning.
    BS in Computer Science from UCP.
    Strong problem solving and leadership skills.
    """
    
    print("=== JD Info ===")
    jd_info = extract_text_info(sample_jd)
    print(jd_info)
    
    print("\n=== CV Info ===")
    cv_info = extract_text_info(sample_cv)
    print(cv_info)