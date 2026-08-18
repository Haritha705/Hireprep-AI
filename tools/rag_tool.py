import json
from typing import Any

from langchain_core.tools import tool

from ai.llm_adapter import generate_text_with_langchain
from db.Mongodb import get_vector_collection
from embeddings.embedding_model import EmbeddingModel


@tool
async def rag_tool(query: str) -> dict[str, Any]:
    """Retrieve relevant interview context and answer the query using the existing RAG pipeline components."""
    try:
        embedding_model = EmbeddingModel()
        query_embedding = await embedding_model.embed_query(query)
        collection = get_vector_collection()
        docs = await collection.find({}).to_list(length=1000)

        scored_docs = []
        for doc in docs:
            doc_embedding = doc.get("embedding", [])
            if not doc_embedding:
                continue
            dot_product = sum(a * b for a, b in zip(query_embedding, doc_embedding))
            magnitude1 = (sum(a * a for a in query_embedding)) ** 0.5
            magnitude2 = (sum(b * b for b in doc_embedding)) ** 0.5
            score = 0.0 if magnitude1 == 0 or magnitude2 == 0 else dot_product / (magnitude1 * magnitude2)
            scored_docs.append((score, doc))

        scored_docs.sort(key=lambda item: item[0], reverse=True)
        context_items = []
        for _, doc in scored_docs[:5]:
            context_items.append(
                f"- {doc.get('question', doc.get('text', ''))} | {doc.get('answer', '')}"
            )

        context = "\n".join(context_items) if context_items else "No relevant context found."
        prompt = (
            "You are an interview prep assistant. Answer the user's question using the retrieved context.\n"
            f"Question: {query}\n\nRetrieved Context:\n{context}"
        )
        answer = generate_text_with_langchain(prompt, system_prompt="You are a helpful interview preparation assistant.")
        return {
            "status": "success",
            "data": {
                "answer": answer,
                "context": context_items,
            },
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": f"RAG retrieval failed: {exc}",
        }
