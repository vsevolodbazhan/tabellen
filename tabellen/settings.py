"""
An application settings. Properties of the `Settings` correspond
to environment variables. All of the specified environment variables
must be set.
"""

from pydantic import BaseSettings

__all__ = ["settings"]


class Settings(BaseSettings):
    SPECIFICATION_DIRECTORY: str
    MONGO_URI: str
    CELERY_APP_NAME: str
    REDIS_URL: str

    class Config:
        case_sensitive = True


settings = Settings()
