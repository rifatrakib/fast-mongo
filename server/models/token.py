from datetime import datetime

from pydantic import EmailStr

from server.models.base import BaseAPI


class JWTData(BaseAPI):
    id: int
    username: str
    email: EmailStr


class JWToken(JWTData):
    exp: datetime
    sub: str
