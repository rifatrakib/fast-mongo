from datetime import datetime

from server.models.helpers.base import BaseResponse
from server.models.helpers.user import UserBase


class JWTData(BaseResponse, UserBase):
    pass


class JWToken(JWTData):
    exp: datetime
    sub: str
