from langchain_core.documents import Document

from app.ingest.chunker import split_documents


def test_split_documents_creates_chunks() -> None:
    docs = [Document(page_content="A" * 2000, metadata={"source": "x"})]
    chunks = split_documents(docs, chunk_size=500, chunk_overlap=50)
    assert len(chunks) >= 4
    assert all(chunk.metadata.get("source") == "x" for chunk in chunks)
