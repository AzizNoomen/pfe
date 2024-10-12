import os
from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    APP_TITLE: str = "Generation Service"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8003


app_config = AppConfig()
