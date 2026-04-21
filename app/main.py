from fastapi import FastAPI

from app.api.routes_chat import router as chat_router
from app.core.config import get_settings
from app.core.logger import configure_logging


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    app = FastAPI(title="RAG Chatbot", version="0.1.0")
    app.include_router(chat_router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
