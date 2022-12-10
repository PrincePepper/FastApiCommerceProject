import secrets
from functools import lru_cache
from typing import Any, Dict, Optional, List, Union

from pydantic import BaseSettings, EmailStr, PostgresDsn, validator, AnyHttpUrl


@lru_cache()
class Settings(BaseSettings):
    # main
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    WORKERS: int = 1

    API_V1_STR: str = "/api/v1"

    SOURCES_URL: dict
    PASSWORD_1CLAB: str

    SALT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    # 60 minutes * 24 hours * 7 days = 7 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10 * 24 * 7
    JWT_ALGORITHM: str

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER_HOST: str
    POSTGRES_SERVER_PORT: str = "5432"
    POSTGRES_USERNAME: str = "postgres"
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USERNAME"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER_HOST"),
            path=f"/{values.get('POSTGRES_DATABASE') or ''}",
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    SSH_HOST: str
    SSH_USER: str
    SSH_PRIVATE_KEY: str
    SSH_PRIVATE_KEY_PASSWORD: str
    SSH_ROMOTE_BIND_ADDRESS = ("localhost", 5432)

    class Config:
        case_sensitive = True
        env_file = './.env'


settings = Settings()
