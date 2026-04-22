from typing import Iterable, List

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import Settings
from app.retrieval.embeddings import build_embeddings


def get_vectorstore(settings: Settings) -> Chroma:
    return Chroma(
        collection_name=settings.collection_name,
        embedding_function=build_embeddings(settings),
        persist_directory=str(settings.chroma_persist_dir),
    )


def index_documents(settings: Settings, chunks: Iterable[Document]) -> int:
    vectorstore = get_vectorstore(settings)
    documents: List[Document] = list(chunks)
    if not documents:
        return 0
    vectorstore.add_documents(documents)
    return len(documents)
