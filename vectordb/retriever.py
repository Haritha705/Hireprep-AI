from typing import Dict, List

from vectordb.vector_store import VectorStore
from embeddings.embedding_model import embed_query


# Create MongoDB vector store
vector_store = VectorStore()


def _extract_question_text(doc: dict) -> str:
    # 1. Try root-level fields
    q = doc.get("question")
    a = doc.get("answer")

    # 2. Try metadata fields
    meta = doc.get("metadata") or {}
    if not q:
        q = meta.get("question")
    if not a:
        a = meta.get("answer")

    if q:
        q = q.strip()
        if a:
            return f"{q}\n\nAnswer:\n{a.strip()}"
        return q

    # 3. Fallback to text field
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
    top_k: int = 200
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
                category = _determine_category(doc)
                
                # Technical questions must match the candidate's detected role
                if category == "technical" and resume_role:
                    doc_role = doc.get("role") or ""
                    # Allow partial, case‑insensitive match between detected role and document role
                    if resume_role.lower().strip() not in doc_role.lower():
                        continue
                    if len(questions["technical"]) >= 20:
                        continue
                        
                seen.add(q_text)
                questions[category].append(q_text)

    except Exception as e:
        print(f"❌ Main MongoDB vector search failed: {e}")

    # --------------------------------------------------
    # 3. Fallback targeted retrieval
    # --------------------------------------------------
    # Repeatedly attempt to fetch technical questions if under limit
    attempts = 0
    while len(questions["technical"]) < 20 and attempts < 5:
        try:
            t_query = f"{resume_role or ''} technical interview questions"
            t_embed = await embed_query(t_query)
            # Increase top_k each attempt to broaden search
            t_results = await vector_store.similarity_search(query_embedding=t_embed, top_k=top_k + (attempts * 200))
            for doc in t_results:
                if _determine_category(doc) == "technical":
                    q_text = _extract_question_text(doc)
                    if q_text and q_text not in questions["technical"]:
                        questions["technical"].append(q_text)
                    if len(questions["technical"]) >= 20:
                        break
        except Exception as e:
            print(f"❌ Technical question fallback error: {e}")
        attempts += 1

    if len(questions["project"]) < 5:
        try:
            p_query = f"{resume_role or ''} project architecture challenges implementation"
            p_embed = await embed_query(p_query)
            p_results = await vector_store.similarity_search(query_embedding=p_embed, top_k=50)
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