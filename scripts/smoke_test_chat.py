from app.core.config import get_settings
from app.services.chat_service import chat


if __name__ == "__main__":
    settings = get_settings()
    query = "What documents are currently indexed?"
    result = chat(settings, query)
    print(result["answer"])
    print("Sources:", result["sources"])
