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

    class Config:
        env_file = ".env"
