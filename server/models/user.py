from beanie import Document
from pydantic import EmailStr

from server.models.base import BaseDocument, BaseRequest, BaseResponse


class UserBase(BaseDocument):
    user_name: str
    email: EmailStr
    password: str


class User(Document, UserBase):
    class Settings:
        name = "users"
        indexes = ["user_name", "email"]


class UserRequest(BaseRequest, UserBase):
    pass


class UserResponse(BaseResponse, UserBase):
    pass
