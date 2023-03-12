from datetime import datetime, timedelta
from typing import Union

from jose import JWTError, jwt
from pydantic import ValidationError

from server.config.factory import settings
from server.models.database.user import User
from server.models.helpers.token import JWTData, JWToken
from server.services.exceptions import EntityDoesNotExist


class JWTEngine:
    def _generate_jwt(
        self,
        *,
        user_data: JWTData,
        expires_delta: Union[datetime, None] = None,
    ) -> str:
        """encode user data using SHA256 algorithm into JWT."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_MIN)

        to_encode = JWToken(
            **user_data.dict(),
            exp=expire,
            sub=settings.JWT_SUBJECT,
        ).dict()

        return jwt.encode(
            to_encode,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def generate_access_token(self, user: User) -> str:
        """generate access token using user id, username, and email."""
        if not user:
            raise EntityDoesNotExist("cannot generate JWT for without User entity!")

        return self._generate_jwt(
            user_data=JWTData(
                id=user.id,
                username=user.username,
                email=user.email,
            ),
            expires_delta=timedelta(minutes=settings.JWT_MIN),
        )

    def retrieve_token_details(self, token: str) -> JWTData:
        """extract, decode, and validate user data from JWT."""
        try:
            payload = jwt.decode(
                token=token,
                key=settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            jwt_data = JWTData(
                id=payload.get("id"),
                username=payload.get("username"),
                email=payload.get("email"),
            )
        except JWTError as token_decode_error:
            raise ValueError("unable to decode JWT") from token_decode_error
        except ValidationError as validation_error:
            raise ValueError("invalid payload in JWT") from validation_error
        return jwt_data


def get_jwt_engine() -> JWTEngine:
    return JWTEngine()


jwt_engine: JWTEngine = get_jwt_engine()
