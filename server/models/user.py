from datetime import datetime
from typing import Union

from beanie import Document, Insert, Update, before_event
from pydantic import EmailStr, Field

from server.models.base import BaseDocument, BaseRequest, BaseResponse


class UserBase(BaseDocument):
    username: str = Field(
        title="username",
        decription="""
            Unique username containing letters, numbers, and
            any of (., _, -, @) in between 6 to 32 characters.
        """,
        regex=r"^[\w.@_-]{6,32}$",
        min_length=6,
        max_length=32,
    )
    email: EmailStr = Field(
        title="email",
        decription="Unique email that can be used for user account activation.",
    )


class User(Document, UserBase):
    hashed_password: str = Field(
        title="hashed password",
        decription="Generated hash for the user provided password string.",
    )
    hash_salt: str = Field(
        title="hashed salt",
        decription="A mark for increasing security on password hash.",
    )
    is_active: bool = Field(
        default=False,
        title="active status",
        decription="Whether user is active, determined via email confirmation.",
    )
    is_verified: bool = Field(
        default=False,
        title="verification status",
        decription="Whether user is verified, determined via phone number verification.",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        title="verification status",
        decription="Whether user is verified, determined via phone number verification.",
    )
    updated_at: Union[datetime, None] = Field(
        default=None,
        title="verification status",
        decription="Whether user is verified, determined via phone number verification.",
    )

    class Settings:
        name = "users"
        indexes = ["username", "email"]

    @before_event(Insert)
    def nullify_update_time_on_create(self):
        """set time of update as None before inserting user data."""
        self.updated_at = None

    @before_event(Update)
    def time_of_last_update(self):
        """set time of update as current UTC time before updating user data."""
        self.updated_at = datetime.utcnow()


class UserRequest(BaseRequest, UserBase):
    password: str = Field(
        title="password",
        decription="""
            Password containing at least 1 uppercase letter, 1 lowercase letter,
            1 number, 1 character that is neither letter nor number, and
            between 8 to 32 characters.
        """,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$",
        min_length=8,
        max_length=64,
    )


class UserResponse(BaseResponse, UserBase):
    is_active: bool = Field(
        default=False,
        title="active status",
        decription="Whether user is active, determined via email confirmation.",
    )
    is_verified: bool = Field(
        default=False,
        title="verification status",
        decription="Whether user is verified, determined via phone number verification.",
    )
