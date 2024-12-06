"""
config.py

This module initializes and configures application settings using the Pydantic `BaseSettings` class.
It supports environment-specific configurations via `.env` files
Enhances debugging output with `rich`-styled tracebacks.
"""

from pydantic_settings import BaseSettings
from rich.traceback import install as rich_installer
from loguru import logger
from datetime import datetime

rich_installer()
# pylint: disable=R0903


logger.add(
    f"logs/log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
    rotation="1 week",
    retention="1 month",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)


class Settings(BaseSettings):
    """
    Manages application settings
    """

    debug: bool | None = False
    database_url: str | None = None
    py_version: str | None = None
    poetry_version: str | None = None

    class Config:
        """
        Loading configurations from environment variables
        """

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
