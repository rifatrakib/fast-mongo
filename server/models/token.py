from datetime import datetime

from server.models.base import BaseAPI, BaseResponse
from server.models.user import UserBase


class JWTData(BaseResponse, UserBase):
    pass


class JWToken(JWTData):
    exp: datetime
    sub: str


class TokenResponseSchema(BaseAPI):
    token_type: str
    access_token: str
