from pydantic import EmailStr, Field

from server.models.helpers.base import BaseDocument


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
