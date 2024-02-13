import os

from datetime import timedelta
from secrets import token_urlsafe
from typing import Any
from typing import List
from typing import Optional

from pydantic import field_validator
from pydantic import PostgresDsn
from pydantic import ValidationInfo
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    # TODO: Change to .env.example when finish
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file_encoding="utf-8", env_file=".env"
    )

    # Flask Configuration
    FLASK_APP: str
    SECRET_KEY: str = token_urlsafe(16)
    API_V1_SVR: str = "/api/v1"
    DEBUG: bool = False
    TESTING: bool = False

    # SQLAlchemy Configuration
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", "localhost")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_HOST"),
            path=f"{info.data.get('POSTGRES_DB') or ''}",
        )

    # JWT Configuration
    JWT_COOKIE_SECURE: bool = os.environ.get("JWT_COOKIE_SECURE", False)
    JWT_TOKEN_LOCATION: List[str]
    JWT_SECRET_KEY: str = token_urlsafe(16)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(days=2)

    # WTF Configuration


class DevelopmentSettings(Settings):
    DEVELOPMENT: bool = True
    DEBUG: bool = True
    WTF_CSRF_ENABLED: bool = False
    DEBUG_TB_ENABLED: bool = True


class TestingSettings(Settings):
    TESTING: bool = True
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///testdb.sqlite"
    BCRYPT_LOG_ROUNDS: int = 1
    WTF_CSRF_ENABLED: bool = False
