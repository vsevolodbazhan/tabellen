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

    # This variable defines a file with access credentials
    # to Google Sheets API. This file is generated
    # in Google Developer Console.
    SHEETS_CREDENTIALS_FILE: str
    # This variable is a fallback for previous one.
    # It contains access credentials as a JSON string.
    # This is useful for deploying to Heroku since it does not
    # allow to store files outside of a `git` repo.
    SHEETS_CREDENTIALS_JSON: str = ""

    class Config:
        case_sensitive = True


settings = Settings()
