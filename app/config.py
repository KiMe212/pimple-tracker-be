from functools import lru_cache
from urllib.parse import quote_plus

import structlog
from pydantic_settings import BaseSettings as PydanticSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(PydanticSettings):
    model_config = SettingsConfigDict(extra="allow", env_file=".env", env_file_encoding="utf-8")


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow", env_prefix="DATABASE_")

    host: str = "localhost"
    port: int = 5432
    user: str = "db-user"
    password: str = "password-for-db-user"
    name: str = "db-name"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{quote_plus(self.password)}@{self.host}:{self.port}/{self.name}"


class UvicornSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="UVICORN_",
        env_file=".env",
        extra="ignore",
    )

    log_level: str = "info"
    reload: bool = True
    limit_max_requests: int | None = None


class Settings(BaseSettings, case_sensitive=False):
    model_config = SettingsConfigDict(extra="allow")

    uvicorn: UvicornSettings = UvicornSettings()
    db: DBSettings = DBSettings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


config: Settings = get_settings()
log = structlog.get_logger()
