from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import GEMINI_API_KEY


class EmbeddingModel:

    def __init__(self):

        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GEMINI_API_KEY,
            output_dimensionality=768,
        )

    async def embed_texts(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        return await self.embeddings.aembed_documents(texts)

    async def embed_query(
        self,
        text: str
    ) -> list[float]:

        return await self.embeddings.aembed_query(text)


_embedding_model = None


def get_embedding_model():

    global _embedding_model

    if _embedding_model is None:
        _embedding_model = EmbeddingModel()

    return _embedding_model


async def embed_documents(
    texts: list[str]
) -> list[list[float]]:

    model = get_embedding_model()

    return await model.embed_texts(texts)


async def embed_query(
    text: str
) -> list[float]:

    model = get_embedding_model()

    return await model.embed_query(text)