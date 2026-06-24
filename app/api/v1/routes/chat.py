from fastapi import APIRouter, Body, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies.auth import get_current_user
from app.core.responses import ApiResponse
from app.models import User
from app.schemas.api_response import ApiResponseSchema
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_with_documents, stream_chat_with_documents

router = APIRouter()


@router.post("/", response_model=ApiResponseSchema[ChatResponse])
async def chat(
    current_user: User = Depends(get_current_user),
    payload: ChatRequest = Body(...),
):
    """Simple chat response as Markdown text."""

    business_id = str(current_user.business_id)

    answer = chat_with_documents(
        business_id=business_id,
        message=payload.message,
        top_k=payload.top_k,
    )

    return ApiResponse(
        data=ChatResponse.model_validate(answer),
        message="Chat response generated successfully",
    )


@router.post("/stream")
async def stream_chat(
    current_user: User = Depends(get_current_user),
    payload: ChatRequest = Body(...),
):
    """Stream chat response as SSE."""

    business_id = str(current_user.business_id)

    return StreamingResponse(
        stream_chat_with_documents(
            business_id=business_id,
            message=payload.message,
            top_k=payload.top_k,
        ),
        media_type="text/event-stream",
    )
