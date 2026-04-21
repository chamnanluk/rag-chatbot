from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_core.documents import Document

SUPPORTED_SUFFIXES = {".txt", ".md", ".pdf"}


def _load_file(path: Path) -> List[Document]:
    if path.suffix == ".pdf":
        return PyPDFLoader(str(path)).load()
    if path.suffix == ".md":
        return UnstructuredMarkdownLoader(str(path)).load()
    return TextLoader(str(path), autodetect_encoding=True).load()


def load_documents(data_dir: Path) -> List[Document]:
    documents: List[Document] = []
    for file_path in sorted(data_dir.rglob("*")):
        if not file_path.is_file() or file_path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        docs = _load_file(file_path)
        for doc in docs:
            doc.metadata["source"] = str(file_path)
            doc.metadata["file_type"] = file_path.suffix.lower().lstrip(".")
        documents.extend(docs)
    return documents
