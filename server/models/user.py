from datetime import datetime

from beanie import Document
from pydantic import EmailStr

from server.models.base import BaseDocument, BaseRequest, BaseResponse


class UserBase(BaseDocument):
    username: str
    email: EmailStr


class User(Document, UserBase):
    hashed_password: str
    hash_salt: str
    is_active: bool = False
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "users"
        indexes = ["username", "email"]


class UserRequest(BaseRequest, UserBase):
    password: str


class UserResponse(BaseResponse, UserBase):
    is_active: bool
    is_verified: bool
