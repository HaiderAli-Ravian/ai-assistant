from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.core.responses import ApiResponse
from app.schemas.api_response import ApiResponseSchema
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_with_documents, stream_chat_with_documents

router = APIRouter()


@router.post("/", response_model=ApiResponseSchema[ChatResponse])
async def chat(payload: ChatRequest):
    answer = chat_with_documents(
        message=payload.message,
        top_k=payload.top_k,
    )

    return ApiResponse(
        data=answer,
        message="Chat response generated successfully",
    )

@router.post("/stream")
async def stream_chat(payload: ChatRequest):
    """Stream chat response as Markdown text."""

    return StreamingResponse(
        stream_chat_with_documents(
            message=payload.message,
            top_k=payload.top_k,
        ),
        media_type="text/event-stream",
    )

