from server.config.environments.base import BaseConfig


class StagingConfig(BaseConfig):
    DEBUG: bool = False
    MODE: str = "Staging"
