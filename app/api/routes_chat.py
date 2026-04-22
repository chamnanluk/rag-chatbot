from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas import ChatRequest, ChatResponse
from app.core.config import Settings, get_settings
from app.core.exceptions import RetrievalError
from app.services.chat_service import chat

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat_endpoint(
    payload: ChatRequest,
    settings: Settings = Depends(get_settings),
) -> ChatResponse:
    try:
        result = chat(settings, payload.question)
        return ChatResponse(**result)
    except RetrievalError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
