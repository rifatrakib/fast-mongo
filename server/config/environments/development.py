from server.config.environments.base import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    MODE: str = "Development"
