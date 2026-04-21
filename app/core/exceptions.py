class RAGError(Exception):
    """Base exception for RAG workflow issues."""


class IngestionError(RAGError):
    """Raised when documents cannot be loaded or chunked."""


class RetrievalError(RAGError):
    """Raised when retrieval or generation fails."""
