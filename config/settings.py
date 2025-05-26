"""Setup configuration for the application."""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the application."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    AWS_ENDPOINT: Optional[str] = Field(default="localhost:4566", env="AWS_ENDPOINT")
    AWS_REGION: Optional[str] = Field(default=None, env="AWS_REGION")
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    USERNAME: Optional[str] = Field(default="admin", env="USERNAME")
    PASSWORD: Optional[str] = Field(default="admin", env="PASSWORD")


settings = Settings()
