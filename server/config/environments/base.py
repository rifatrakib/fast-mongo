from typing import Union

from pydantic import BaseSettings, EmailStr, HttpUrl


class BaseConfig(BaseSettings):
    APP_NAME: str
    MODE: str

    # database configuration variables
    MONGODB_URI: str

    # hash generation variables
    HASH_SALT: str
    PASSWORD_HASH_ALGORITHM: str
    SALT_HASH_ALGORITHM: str

    # token management variables
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_SUBJECT: str
    JWT_TOKEN_PREFIX: str
    JWT_MIN: int
    JWT_HOUR: int
    JWT_DAY: int

    # mail server config
    MAIL_USERNAME: Union[EmailStr, str]
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool

    # random generator config
    RANDOM_BYTE_LENGTH: int
    ACTIVATION_URL: HttpUrl

    class Config:
        env_file = ".env"
