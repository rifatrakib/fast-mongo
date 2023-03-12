from pydantic import Field

from server.models.helpers.base import BaseAPI, BaseResponse
from server.models.helpers.user import UserBase


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


class TokenResponseSchema(BaseAPI):
    token_type: str
    access_token: str
