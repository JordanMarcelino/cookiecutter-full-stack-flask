from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str


class UserSignupResponse(BaseModel):
    email: EmailStr
    created_at: datetime
    updated_at: datetime
