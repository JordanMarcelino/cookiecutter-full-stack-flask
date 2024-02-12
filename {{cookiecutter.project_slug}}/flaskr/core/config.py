import os

from datetime import timedelta
from secrets import token_hex
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
    FLASK_ENV: str
    SECRET_KEY: str = token_hex(16)

    # SQLAlchemy Configuration
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        if os.environ.get("POSTGRES_HOST") is not None:
            host = os.environ.get("POSTGRES_HOST")
        else:
            host = info.data.get("POSTGRES_HOST")

        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=host,
            path=f"{info.data.get('POSTGRES_DB') or ''}",
        )

    # JWT Configuration
    JWT_COOKIE_SECURE: bool = False
    JWT_TOKEN_LOCATION: List[str]
    JWT_SECRET_KEY: str = token_hex(16)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(days=2)

    @field_validator("JWT_COOKIE_SECURE")
    def secure_cookie(cls, v: Optional[bool], info: ValidationInfo) -> bool:
        if os.environ.get("JWT_COOKIE_SECURE") is not None:
            return bool(os.environ.get("JWT_COOKIE_SECURE"))

        return v


settings = Settings()
