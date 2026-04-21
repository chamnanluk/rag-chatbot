from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate


def _load_prompt(path: Path, default_value: str) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return default_value


def build_prompt_template(prompts_dir: Path = Path("prompts")) -> ChatPromptTemplate:
    system_default = (
        "You are a helpful assistant that answers ONLY from retrieved context. "
        "If context is missing, say you don't know and suggest re-indexing docs."
    )
    answer_default = (
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer clearly and include source paths when available."
    )
    system_prompt = _load_prompt(prompts_dir / "system_prompt.txt", system_default)
    answer_template = _load_prompt(prompts_dir / "answer_template.txt", answer_default)
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", answer_template),
    ])
