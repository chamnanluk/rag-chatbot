from app.core.config import get_settings
from app.retrieval.vectorstore import get_vectorstore


if __name__ == "__main__":
    settings = get_settings()
    vectorstore = get_vectorstore(settings)
    vectorstore.delete_collection()
    print(f"Deleted collection '{settings.collection_name}'. Run ingest_docs.py to rebuild.")
