import json
import os

from ingestion.load_json import load_json_files
from embeddings.embedding_model import get_embedding

OUTPUT_FILE = "data/question_embeddings.json"


def embed_questions():

    questions = load_json_files()

    embedded_questions = []

    print("\nGenerating Embeddings...\n")

    for i, item in enumerate(questions):

        text = f"""
Category : {item.get('category','')}

Question : {item.get('question','')}

Answer : {item.get('answer','')}
"""

        vector = get_embedding(text)
        print(item["role"], "->", item["question"][:50])
        embedded_questions.append({

         "role": item.get("role"),

    "category": item.get("category"),

    "question_number": item.get("question_number"),

    "question": item.get("question"),

    "answer": item.get("answer"),

    "embedding": vector

})

        print(f"Embedded {i+1}/{len(questions)}")

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        json.dump(
            embedded_questions,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\n===================================")
    print("Embedding Completed Successfully")
    print(f"Saved to : {OUTPUT_FILE}")
    print("===================================")


if __name__ == "__main__":
    embed_questions()