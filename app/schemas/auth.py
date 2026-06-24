from uuid import UUID

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    business_name: str
    website_url: str | None = None
    phone: str | None = None
    timezone: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class BusinessResponse(BaseModel):
    id: UUID
    name: str
    website_url: str | None = None
    phone: str | None = None
    timezone: str | None = None

    model_config = {"from_attributes": True}


class AuthUserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: str
    business: BusinessResponse

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUserResponse