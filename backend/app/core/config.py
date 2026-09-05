from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "GFIP API"
    environment: str = "development"
    database_url: str = "sqlite:///./gfip.db"
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        origins = [value.strip() for value in self.cors_origins.split(",") if value.strip()]
        print(f"DEBUG: Calculated CORS origin list: {origins}")
        return origins

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"DEBUG: Settings loaded: {settings.model_dump()}")
    return settings
