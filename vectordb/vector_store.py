import logging

from db.Mongodb import get_vector_collection

logger = logging.getLogger("uvicorn")


class VectorStore:

    INDEX_NAME = "vector_index"

    def _get_collection(self):
        return get_vector_collection()

    async def get_existing_ids(self) -> set[str]:

        collection = self._get_collection()

        try:

            cursor = collection.find(
                {},
                {
                    "_id": 1,
                    "id": 1
                }
            )

            docs = await cursor.to_list(
                length=50000
            )

            existing_ids = set()

            for doc in docs:

                if "_id" in doc:
                    existing_ids.add(
                        str(doc["_id"])
                    )

                if "id" in doc:
                    existing_ids.add(
                        str(doc["id"])
                    )

            return existing_ids

        except Exception as e:

            logger.error(
                f"Failed to get existing IDs: {e}"
            )

            return set()

    async def ensure_vector_index(self):

        collection = self._get_collection()

        try:

            cursor = collection.list_search_indexes()

            indexes = await cursor.to_list(
                length=100
            )

            existing_names = [
                index.get("name")
                for index in indexes
            ]

            if self.INDEX_NAME in existing_names:

                logger.info(
                    f"Vector index '{self.INDEX_NAME}' already exists."
                )

                return

            from pymongo.operations import SearchIndexModel

            index_model = SearchIndexModel(

                definition={
                    "fields": [
                        {
                            "type": "vector",
                            "path": "embedding",

                            # Your chosen dimension
                            "numDimensions": 768,

                            "similarity": "cosine"
                        }
                    ]
                },

                name=self.INDEX_NAME,

                type="vectorSearch"
            )

            await collection.create_search_index(
                model=index_model
            )

            logger.info(
                f"Created MongoDB vector index: "
                f"{self.INDEX_NAME}"
            )

        except Exception as e:

            logger.warning(
                f"Vector index check failed: {e}"
            )

    async def add_documents(
        self,
        documents,
        embeddings,
        ids
    ):

        collection = self._get_collection()

        from pymongo import UpdateOne

        operations = []

        for document, embedding, doc_id in zip(
            documents,
            embeddings,
            ids
        ):

            mongo_doc = {

                "_id": doc_id,

                "id": doc_id,

                "text": document.page_content,

                "embedding": embedding,

                "metadata": document.metadata,

                "role": document.metadata.get(
                    "role",
                    "General"
                ),

                "category": document.metadata.get(
                    "category",
                    "General"
                ),

                "difficulty": document.metadata.get(
                    "difficulty",
                    "Medium"
                ),

                "answer": document.metadata.get(
                    "answer",
                    ""
                )
            }

            operations.append(
                UpdateOne(
                    {
                        "_id": doc_id
                    },

                    {
                        "$set": mongo_doc
                    },

                    upsert=True
                )
            )

        if operations:

            result = await collection.bulk_write(
                operations
            )

            logger.info(
                f"Inserted: {result.upserted_count}, "
                f"Updated: {result.modified_count}"
            )

    async def similarity_search(
        self,
        query_embedding,
        top_k: int = 4
    ):

        collection = self._get_collection()

        pipeline = [

            {
                "$vectorSearch": {

                    "index": self.INDEX_NAME,

                    "path": "embedding",

                    "queryVector": query_embedding,

                    "numCandidates": max(
                        top_k * 10,
                        50
                    ),

                    "limit": top_k
                }
            },

            {
                "$project": {

                    "_id": 0,

                    "text": 1,

                    "question": 1,

                    "answer": 1,

                    "role": 1,

                    "category": 1,

                    "difficulty": 1,

                    "metadata": 1,

                    "source": 1,

                    "score": {
                        "$meta":
                        "vectorSearchScore"
                    }
                }
            }
        ]

        try:

            cursor = collection.aggregate(
                pipeline
            )

            results = await cursor.to_list(
                length=top_k
            )

            return results

        except Exception as e:

            logger.error(
                f"MongoDB vector search failed: {e}"
            )

            return []