from langchain_openai import OpenAIEmbeddings

from app.core.config import Settings


def build_embeddings(settings: Settings) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        api_key=settings.openai_api_key,
        model=settings.openai_embedding_model,
    )
