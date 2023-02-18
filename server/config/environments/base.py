from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    APP_NAME: str
    MODE: str

    class Config:
        env_file = ".env"
