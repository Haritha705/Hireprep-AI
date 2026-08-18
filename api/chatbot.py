from fastapi import APIRouter
from pydantic import BaseModel

from ai.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])
chat_service = ChatService()


class ChatRequest(BaseModel):
    message: str


@router.post("")
async def chat(request: ChatRequest):
    response = await chat_service.chat(request.message)
    return {"response": response}
