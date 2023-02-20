from pydantic import BaseSettings, FilePath


class BaseConfig(BaseSettings):
    APP_NAME: str
    MODE: str
    MONGODB_URI: str
    MONGO_MAPPER_PATH: FilePath

    class Config:
        env_file = ".env"
