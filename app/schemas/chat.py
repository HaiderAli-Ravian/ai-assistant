from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    top_k: int = 5


class ChatSource(BaseModel):
    filename: str | None = None
    document_id: str | None = None
    cloudinary_url: str | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]