from pathlib import Path
from typing import List

from langchain_core.documents import Document

from app.core.config import Settings
from app.core.exceptions import IngestionError
from app.ingest.chunker import split_documents
from app.ingest.loaders import load_documents


def run_ingestion(data_dir: Path, settings: Settings) -> List[Document]:
    try:
        documents = load_documents(data_dir)
        if not documents:
            raise IngestionError(f"No supported documents found in {data_dir}")
        return split_documents(
            documents=documents,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
    except Exception as exc:
        if isinstance(exc, IngestionError):
            raise
        raise IngestionError(f"Ingestion pipeline failed: {exc}") from exc
