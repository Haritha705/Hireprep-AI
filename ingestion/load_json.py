import os
import json

from langchain_core.documents import Document


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

KNOWLEDGE_BASE = os.path.join(
    BASE_DIR,
    "data",
    "knowledge_base"
)


def detect_role(filename: str) -> str:

    filename = filename.lower()

    if "data_analyst" in filename:
        return "Data Analyst"

    if "full_stack" in filename:
        return "Full Stack Developer"

    if "genai" in filename:
        return "Generative AI"

    if "generative" in filename:
        return "Generative AI"

    if "hr" in filename:
        return "HR"

    if "project" in filename:
        return "Project"

    return "General"


def load_json_files() -> list[dict]:
    all_questions = []
    if not os.path.exists(KNOWLEDGE_BASE):
        print("Knowledge base folder not found.")
        return all_questions

    for filename in os.listdir(KNOWLEDGE_BASE):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(KNOWLEDGE_BASE, filename)
        role = detect_role(filename)
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                questions = json.load(file)
            for index, q in enumerate(questions):
                q_copy = q.copy()
                q_copy["role"] = role
                q_copy["source"] = filename
                if "question_number" not in q_copy:
                    q_copy["question_number"] = index + 1
                all_questions.append(q_copy)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    return all_questions


def load_interview_documents() -> list[Document]:

    documents = []

    if not os.path.exists(KNOWLEDGE_BASE):
        print("Knowledge base folder not found.")
        return documents

    for filename in os.listdir(KNOWLEDGE_BASE):

        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(
            KNOWLEDGE_BASE,
            filename
        )

        role = detect_role(filename)

        try:

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                questions = json.load(file)

            for index, q in enumerate(questions):

                question = q.get(
                    "question",
                    ""
                )

                answer = q.get(
                    "answer",
                    ""
                )

                category = q.get(
                    "category",
                    "General"
                )

                difficulty = q.get(
                    "difficulty",
                    "Medium"
                )

                question_number = q.get(
                    "question_number",
                    index + 1
                )

                if not question:
                    continue

                # Text used for embedding
                page_content = f"""
Role: {role}

Category: {category}

Difficulty: {difficulty}

Question:
{question}
""".strip()

                document = Document(

                    page_content=page_content,

                    metadata={
                        "role": role,
                        "category": category,
                        "difficulty": difficulty,
                        "question_number": question_number,
                        "answer": answer,
                        "source": filename,
                    }
                )

                documents.append(document)

        except Exception as e:

            print(
                f"Error reading {filename}: {e}"
            )

    print(
        f"Loaded {len(documents)} LangChain documents."
    )

    return documents