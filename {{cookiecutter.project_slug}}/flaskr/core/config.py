from typing import List, Optional, Any, Dict

from secrets import token_hex

from pydantic import PostgresDsn, field_validator, ValidationInfo

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # TODO: Change to .env.example when finish
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file_encoding="utf-8", env_file=".env"
    )

    FLASK_APP: str
    FLASK_ENV: str
    SECRET_KEY: str = token_hex(16)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

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


settings = Settings()
