from langchain_core.vectorstores import VectorStoreRetriever

from app.core.config import Settings
from app.retrieval.vectorstore import get_vectorstore


def build_retriever(settings: Settings) -> VectorStoreRetriever:
    return get_vectorstore(settings).as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.top_k},
    )
