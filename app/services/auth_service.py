from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ApiException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.business import Business
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest


async def register_user(
    payload: RegisterRequest,
    db: AsyncSession,
) -> dict:
    """Create a business and owner user."""

    existing_user = await db.execute(
        select(User).where(User.email == payload.email)
    )

    if existing_user.scalar_one_or_none():
        raise ApiException(message="Email already registered", status_code=409)

    business = Business(
        name=payload.business_name,
        website_url=payload.website_url,
        phone=payload.phone,
        timezone=payload.timezone,
    )

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=UserRole.OWNER,
        business=business,
    )

    db.add(user)
    await db.commit()

    result = await db.execute(
        select(User)
        .options(selectinload(User.business))
        .where(User.id == user.id)
    )
    user = result.scalar_one()

    access_token = create_access_token(user.id)

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=user,
    )


async def login_user(
    payload: LoginRequest,
    db: AsyncSession,
) -> dict:
    """Authenticate user and return access token."""

    result = await db.execute(
        select(User)
        .options(selectinload(User.business))
        .where(User.email == payload.email)
    )

    user = result.scalar_one_or_none()

    if user is None or not verify_password(payload.password, user.password_hash):
        raise ApiException(message="Invalid email or password", status_code=401)

    access_token = create_access_token(user.id)

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=user,
    )