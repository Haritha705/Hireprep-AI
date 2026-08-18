import re


DATA_ANALYST = {
    "sql",
    "power bi",
    "tableau",
    "excel",
    "pandas",
    "numpy",
    "python",
    "statistics",
    "data analysis",
    "data analytics",
    "visualization",
    "machine learning"
}

FULL_STACK = {
    "html",
    "css",
    "javascript",
    "react",
    "node",
    "node.js",
    "express",
    "mongodb",
    "mysql",
    "api",
    "rest",
    "next.js",
    "bootstrap"
}

GENERATIVE_AI = {
    "generative ai",
    "genai",
    "llm",
    "langchain",
    "langgraph",
    "rag",
    "openai",
    "prompt engineering",
    "transformers",
    "huggingface",
    "gpt",
    "bert",
    "vector database",
    "embeddings",
    "fine-tuning",
    "peft",
    "lora",
    "faiss",
    "chromadb",
    "ollama",
    "agentic ai",
    "deep learning",
    "artificial intelligence"
}


def detect_role(skills):

    skills = [skill.lower().strip() for skill in skills]

    data_score = 0
    fullstack_score = 0
    genai_score = 0

    for skill in skills:

        if skill in DATA_ANALYST:
            data_score += 1

        if skill in FULL_STACK:
            fullstack_score += 1

        if skill in GENERATIVE_AI:
            genai_score += 1

    scores = {
        "Generative AI": genai_score,
        "Data Analyst": data_score,
        "Full Stack Developer": fullstack_score
    }

    max_role = max(scores, key=scores.get)

    if scores[max_role] > 0:
        return max_role

    return "General"


if __name__ == "__main__":

    sample = [
        "Python",
        "SQL",
        "Power BI",
        "Excel"
    ]

    role = detect_role(sample)

    print("\nDetected Role :", role)