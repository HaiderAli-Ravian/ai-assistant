from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponseSchema(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: T


class ApiErrorSchema(BaseModel):
    success: bool = False
    message: str
    error: dict