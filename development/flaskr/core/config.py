from datetime import timedelta

from secrets import token_urlsafe

from typing import Any
from typing import List
from typing import Optional

from decouple import config

from pydantic import field_validator
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
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    TESTING: bool = False

    # SQLAlchemy Configuration
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = config("POSTGRES_HOST", default="localhost")
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        return f"postgresql://{info.data.get('POSTGRES_USER')}:{info.data.get('POSTGRES_PASSWORD')}@{info.data.get('POSTGRES_HOST')}:5432/{info.data.get('POSTGRES_DB')}?sslmode=disable"

    # JWT Configuration
    JWT_COOKIE_SECURE: bool = config("JWT_COOKIE_SECURE", default=False)
    JWT_TOKEN_LOCATION: List[str]
    JWT_SECRET_KEY: str = token_urlsafe(16)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(days=2)

    # Bcrypt Configuration
    BCRYPT_LOG_ROUNDS: int = 13

    # WTF Configuration
    WTF_CSRF_ENABLED: bool = True

    # Mail Settings
    MAIL_DEFAULT_SENDER: str = "noreply@flask.com"
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 465
    MAIL_USE_TLS: bool = False
    MAIL_USE_SSL: bool = True
    MAIL_DEBUG: bool = False
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    SECURITY_PASSWORD_SALT: str = config(
        "SECURITY_PASSWORD_SALT", default=token_urlsafe(16)
    )


class DevelopmentSettings(Settings):
    DEVELOPMENT: bool = True
    DEBUG: bool = True
    WTF_CSRF_ENABLED: bool = False


class TestingSettings(Settings):
    TESTING: bool = True
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///testdb.sqlite"
    BCRYPT_LOG_ROUNDS: int = 5
    WTF_CSRF_ENABLED: bool = False


prod_settings = Settings()
dev_settings = DevelopmentSettings()
test_settings = TestingSettings()
