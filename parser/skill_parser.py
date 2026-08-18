import re

# Master Skill Database
SKILL_DATABASE = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Power BI",
    "Tableau",
    "Excel",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Analysis",
    "Data Analytics",
    "FastAPI",
    "Flask",
    "React",
    "Next.js",
    "Node.js",
    "HTML",
    "CSS",
    "JavaScript",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Azure",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Generative AI",
    "GenAI",
    "LangChain",
    "LangGraph",
    "RAG",
    "LLM",
    "OpenAI",
    "Prompt Engineering",
    "Transformers",
    "HuggingFace",
    "Vector Database",
    "FAISS",
    "ChromaDB",
    "Ollama",
    "Fine-Tuning",
    "LoRA",
    "PEFT"
]


def extract_skills(resume_text):
    """
    Extract only the skills that actually appear
    in the resume.
    """

    extracted_skills = []

    for skill in SKILL_DATABASE:

        # Whole word match (case-insensitive)
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, resume_text, re.IGNORECASE):
            extracted_skills.append(skill)

    return extracted_skills