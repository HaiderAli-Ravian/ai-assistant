from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ApiException
from app.db.session import get_db
from app.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Resolve authenticated user from JWT token.
    """

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        user_id = UUID(payload["sub"])

    except Exception:
        raise ApiException(
            status_code=401,
            message="Invalid authentication token",
        )

    result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise ApiException(
            status_code=401,
            message="User not found",
        )

    return user