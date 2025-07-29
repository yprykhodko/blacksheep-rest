from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # to override info:
    # export app_info='{"title": "x", "version": "0.0.2"}'
    title: str = "blacksheep-starter"
    version: str = "0.0.1"

    is_debug: bool = True
    log_level: str = "INFO"

    db_port: int = 5432
    db_host: str = "localhost"
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "blacksheep_starter"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def connection_string(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


@lru_cache
def load_settings() -> Settings:
    return Settings()
