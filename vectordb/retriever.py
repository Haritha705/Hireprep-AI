from typing import Dict, List

from vectordb.vector_store import VectorStore
from embeddings.embedding_model import embed_query


# Create MongoDB vector store
vector_store = VectorStore()


def _extract_question_text(doc: dict) -> str:
    meta = doc.get("metadata") or {}
    if meta.get("question"):
        return meta.get("question").strip()
    text = doc.get("text") or ""
    if "Question:" in text:
        return text.split("Question:", 1)[1].strip()
    return text.strip()


def _determine_category(doc: dict) -> str:
    meta = doc.get("metadata") or {}
    source = str(meta.get("source") or doc.get("source") or "").lower().strip()
    cat = str(doc.get("category") or meta.get("category") or "").lower().strip()
    role = str(doc.get("role") or meta.get("role") or "").lower().strip()

    if "hr_questions" in source or role == "hr" or cat in ["hr", "human resources", "behavioral", "behavioural"]:
        return "hr"
    if "project_questions" in source or role == "project" or cat in ["project", "projects"]:
        return "project"
    return "technical"


async def get_interview_questions(
    query: str,
    resume_role: str = None,
    top_k: int = 30
) -> Dict[str, List[str]]:

    # --------------------------------------------------
    # 1. Validate query
    # --------------------------------------------------
    query = (query or "").strip()
    if not query:
        query = resume_role or "interview questions"

    search_query = f"{resume_role} {query}" if resume_role else query

    # --------------------------------------------------
    # 2. Main Vector Search
    # --------------------------------------------------
    questions: Dict[str, List[str]] = {
        "technical": [],
        "hr": [],
        "project": []
    }

    try:
        query_embedding = await embed_query(search_query)
        if len(query_embedding) == 768:
            results = await vector_store.similarity_search(
                query_embedding=query_embedding,
                top_k=top_k
            )

            seen = set()
            for doc in results:
                q_text = _extract_question_text(doc)
                if not q_text or q_text in seen:
                    continue
                seen.add(q_text)
                category = _determine_category(doc)
                questions[category].append(q_text)

    except Exception as e:
        print(f"❌ Main MongoDB vector search failed: {e}")

    # --------------------------------------------------
    # 3. Fallback targeted retrieval for any thin category
    # --------------------------------------------------
    if len(questions["technical"]) < 3:
        try:
            t_query = f"{resume_role or ''} technical architecture algorithms coding system design interview questions"
            t_embed = await embed_query(t_query)
            t_results = await vector_store.similarity_search(query_embedding=t_embed, top_k=15)
            for doc in t_results:
                if _determine_category(doc) == "technical":
                    q_text = _extract_question_text(doc)
                    if q_text and q_text not in questions["technical"]:
                        questions["technical"].append(q_text)
                    if len(questions["technical"]) >= 5:
                        break
        except Exception as e:
            print(f"❌ Technical question fallback error: {e}")

    if len(questions["project"]) < 3:
        try:
            p_query = f"{resume_role or ''} project architecture challenges final year project implementation"
            p_embed = await embed_query(p_query)
            p_results = await vector_store.similarity_search(query_embedding=p_embed, top_k=15)
            for doc in p_results:
                q_text = _extract_question_text(doc)
                if q_text and q_text not in questions["project"]:
                    questions["project"].append(q_text)
                if len(questions["project"]) >= 5:
                    break
        except Exception as e:
            print(f"❌ Project question fallback error: {e}")

    if len(questions["hr"]) < 3:
        try:
            hr_query = f"{resume_role or ''} HR behavioral teamwork challenges strength weakness conflict resolution"
            hr_embed = await embed_query(hr_query)
            hr_results = await vector_store.similarity_search(query_embedding=hr_embed, top_k=15)
            for doc in hr_results:
                q_text = _extract_question_text(doc)
                if q_text and q_text not in questions["hr"]:
                    questions["hr"].append(q_text)
                if len(questions["hr"]) >= 5:
                    break
        except Exception as e:
            print(f"❌ HR question fallback error: {e}")

    return questions