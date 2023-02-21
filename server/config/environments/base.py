from pydantic import BaseSettings, FilePath


class BaseConfig(BaseSettings):
    APP_NAME: str
    MODE: str

    # database configuration variables
    MONGODB_URI: str
    MONGO_MAPPER_PATH: FilePath

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

    class Config:
        env_file = ".env"
