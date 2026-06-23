from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    text: str
    score: float | None = None
    metadata: dict


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]