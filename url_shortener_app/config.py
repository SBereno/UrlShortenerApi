from functools import lru_cache
from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    env_name: str = "Railway"
    base_url: str = os.environ['BASE_URL']
    db_url: str = os.environ['DATABASE_URL']

    #class Config:
    #    env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
