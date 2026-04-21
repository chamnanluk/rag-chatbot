from app.chains.rag_chain import answer_question
from app.core.config import Settings
from app.services.citation_service import unique_sources


def chat(settings: Settings, question: str) -> dict:
    result = answer_question(settings, question)
    result["sources"] = unique_sources(result.get("sources", []))
    return result
