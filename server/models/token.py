from datetime import datetime

from server.models.base import BaseResponse
from server.models.user import UserBase


class JWTData(BaseResponse, UserBase):
    pass


class JWToken(JWTData):
    exp: datetime
    sub: str
