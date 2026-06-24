from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import ApiResponse
from app.db.session import get_db
from app.schemas.api_response import ApiResponseSchema
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.services.auth_service import login_user, register_user
from app.api.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=ApiResponseSchema[AuthResponse])
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await register_user(payload=payload, db=db)

    return ApiResponse(
        data=result,
        message="Account created successfully",
    )


@router.post("/login", response_model=ApiResponseSchema[AuthResponse])
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await login_user(payload=payload, db=db)

    return ApiResponse(
        data=result,
        message="Logged in successfully",
    )


@router.get("/me")
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user