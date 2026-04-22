from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_chat_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_CHAT_MODEL")
    openai_embedding_model: str = Field(
        default="text-embedding-3-small", alias="OPENAI_EMBEDDING_MODEL"
    )
    chroma_persist_dir: Path = Field(default=Path("data/chroma"), alias="CHROMA_PERSIST_DIR")
    collection_name: str = Field(default="rag_documents", alias="CHROMA_COLLECTION")
    top_k: int = Field(default=4, alias="TOP_K")
    chunk_size: int = Field(default=800, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=120, alias="CHUNK_OVERLAP")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.chroma_persist_dir.mkdir(parents=True, exist_ok=True)
    return settings
