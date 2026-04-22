import sys
from pathlib import Path

# Add project root to PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.config import get_settings
from app.ingest.pipeline import run_ingestion
from app.retrieval.vectorstore import index_documents


if __name__ == "__main__":
    settings = get_settings()
    data_dir = Path("data/raw")
    chunks = run_ingestion(data_dir, settings)
    count = index_documents(settings, chunks)
    print(f"Indexed {count} chunks into collection '{settings.collection_name}'.")
