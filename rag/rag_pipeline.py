import hashlib
import logging

from pymongo import UpdateOne

from langchain_core.documents import Document

from db.Mongodb import get_vector_collection
from embeddings.embedding_model import EmbeddingModel
from ingestion.load_json import load_json_files
from vectordb.vector_store import VectorStore


logger = logging.getLogger("uvicorn")


async def ingest_questions():

    logger.info(
        "Starting LangChain RAG ingestion..."
    )

    # =========================================================
    # 1. Load JSON knowledge base
    # =========================================================

    questions = load_json_files()

    if not questions:

        logger.warning(
            "No interview questions found."
        )

        return

    logger.info(
        f"Loaded {len(questions)} questions."
    )


    # =========================================================
    # 2. Convert JSON → LangChain Documents
    # =========================================================

    documents = []

    for index, question in enumerate(questions):

        question_text = question.get(
            "question",
            ""
        ).strip()

        if not question_text:
            continue

        role = question.get(
            "role",
            "General"
        )

        category = question.get(
            "category",
            "General"
        )

        difficulty = question.get(
            "difficulty",
            "Medium"
        )

        answer = question.get(
            "answer",
            ""
        )

        question_number = question.get(
            "question_number",
            index + 1
        )

        source = question.get(
            "source",
            "knowledge_base"
        )


        # -----------------------------------------------------
        # Content that will be embedded
        # -----------------------------------------------------

        page_content = f"""
Role: {role}

Category: {category}

Difficulty: {difficulty}

Question:
{question_text}
""".strip()


        # -----------------------------------------------------
        # LangChain Document
        # -----------------------------------------------------

        document = Document(

            page_content=page_content,

            metadata={
                "role": role,
                "category": category,
                "difficulty": difficulty,
                "question_number": question_number,
                "answer": answer,
                "source": source,
            }
        )

        documents.append(document)


    logger.info(
        f"Created {len(documents)} LangChain Documents."
    )


    if not documents:
        logger.warning(
            "No valid LangChain Documents created."
        )
        return


    # =========================================================
    # 3. Check existing MongoDB documents
    # =========================================================

    vector_store = VectorStore()

    existing_ids = await vector_store.get_existing_ids()

    logger.info(
        f"Existing MongoDB documents: {len(existing_ids)}"
    )


    # =========================================================
    # 4. Generate stable IDs
    # =========================================================

    documents_to_ingest = []
    document_ids = []


    for document in documents:

        question_text = document.metadata.get(
            "answer",
            ""
        )

        # Use question itself for unique ID
        actual_question = document.page_content

        document_id = hashlib.md5(
            actual_question.encode("utf-8")
        ).hexdigest()


        if document_id in existing_ids:

            continue


        document_ids.append(
            document_id
        )

        documents_to_ingest.append(
            document
        )


    logger.info(
        f"New documents to ingest: "
        f"{len(documents_to_ingest)}"
    )


    if not documents_to_ingest:

        logger.info(
            "All questions are already in MongoDB."
        )

        await vector_store.ensure_vector_index()

        return


    # =========================================================
    # 5. Extract text from LangChain Documents
    # =========================================================

    texts = [
        document.page_content
        for document in documents_to_ingest
    ]


    # =========================================================
    # 6. LangChain Embeddings
    # =========================================================

    logger.info(
        "Generating embeddings using "
        "LangChain GoogleGenerativeAIEmbeddings..."
    )


    embedding_model = EmbeddingModel()


    try:

        embeddings = await embedding_model.embed_texts(
            texts
        )

    except Exception as e:

        logger.error(
            f"Embedding generation failed: {e}"
        )

        return


    logger.info(
        f"Generated {len(embeddings)} embeddings."
    )


    # =========================================================
    # 7. Validate embedding dimension
    # =========================================================

    if embeddings:

        dimension = len(
            embeddings[0]
        )

        logger.info(
            f"Embedding dimension: {dimension}"
        )


        if dimension != 768:

            raise ValueError(
                f"Expected 768-dimensional embeddings "
                f"but received {dimension}."
            )


    # =========================================================
    # 8. Store in MongoDB Atlas
    # =========================================================

    collection = get_vector_collection()

    operations = []


    for document_id, document, embedding in zip(
        document_ids,
        documents_to_ingest,
        embeddings
    ):

        metadata = document.metadata


        mongo_document = {

            "_id": document_id,

            "id": document_id,

            # LangChain document text
            "text": document.page_content,

            # Original interview question
            "question": (
                document.page_content
            ),

            "answer": metadata.get(
                "answer",
                ""
            ),

            "role": metadata.get(
                "role",
                "General"
            ),

            "category": metadata.get(
                "category",
                "General"
            ),

            "difficulty": metadata.get(
                "difficulty",
                "Medium"
            ),

            "question_number": metadata.get(
                "question_number"
            ),

            "source": metadata.get(
                "source",
                "knowledge_base"
            ),

            # 768-dimensional vector
            "embedding": embedding,

            # Keep LangChain-style metadata
            "metadata": metadata,
        }


        operations.append(
            UpdateOne(
                {
                    "_id": document_id
                },

                {
                    "$set": mongo_document
                },

                upsert=True
            )
        )


    # =========================================================
    # 9. Bulk insert
    # =========================================================

    if operations:

        result = await collection.bulk_write(
            operations
        )

        logger.info(
            "======================================"
        )

        logger.info(
            "LangChain RAG Ingestion Completed"
        )

        logger.info(
            f"Inserted: {result.upserted_count}"
        )

        logger.info(
            f"Updated: {result.modified_count}"
        )

        logger.info(
            "Embedding dimension: 768"
        )

        logger.info(
            "======================================"
        )


    # =========================================================
    # 10. Ensure MongoDB Vector Index
    # =========================================================

    await vector_store.ensure_vector_index()

    logger.info(
        "MongoDB Atlas Vector Search index ready."
    )