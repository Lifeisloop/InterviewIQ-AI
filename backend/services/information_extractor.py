import re
def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)

    return match.group() if match else None

def extract_phone(text):
    pattern = r"\+?\d[\d\s-]{8,}\d"
    match = re.search(pattern, text)

    return match.group() if match else None

SKILLS = [
    "Python",
    "FastAPI",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "Machine Learning",
    "Deep Learning",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Docker",
    "Git",
    "React",
    "JavaScript",
    "HTML",
    "CSS",
    "Power BI"
]

def extract_skills(text):
    found = []
    text = text.lower()
    for skill in SKILLS:
        if skill.lower() in text:
            found.append(skill)

    return found

def extract_name(text):
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if len(line.split()) <= 4:
            if "@" not in line:
                return line
    return None