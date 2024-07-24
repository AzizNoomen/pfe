import os
from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    APP_TITLE: str = "Model Service"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    BASE_URL: str = os.environ.get('OLLAMA_HOST', 'http://ollama:11434')


app_config = AppConfig()
