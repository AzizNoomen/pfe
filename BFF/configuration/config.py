import os
from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    APP_TITLE: str = "BFF"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8004


app_config = AppConfig()
