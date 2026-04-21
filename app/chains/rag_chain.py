from typing import Any, Dict, List

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from app.chains.prompt_builder import build_prompt_template
from app.core.config import Settings
from app.core.exceptions import RetrievalError
from app.retrieval.retriever import build_retriever


def _format_context(documents: List[Document]) -> str:
    blocks = []
    for doc in documents:
        source = doc.metadata.get("source", "unknown")
        blocks.append(f"[source: {source}]\n{doc.page_content}")
    return "\n\n".join(blocks)


def answer_question(settings: Settings, question: str) -> Dict[str, Any]:
    try:
        retriever = build_retriever(settings)
        documents = retriever.invoke(question)
        context = _format_context(documents)

        llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_chat_model,
            temperature=0,
        )
        prompt = build_prompt_template()
        chain = prompt | llm
        response = chain.invoke({"question": question, "context": context})

        return {
            "answer": response.content,
            "sources": [doc.metadata.get("source", "unknown") for doc in documents],
            "num_chunks": len(documents),
        }
    except Exception as exc:
        raise RetrievalError(f"Failed to answer question: {exc}") from exc
