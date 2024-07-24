import os
from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    APP_TITLE: str = "Ingestion Service"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8001

class DataBaseConfig(BaseSettings):
    """Configuration class for connecting to the accompanying database"""
    DB_HOST: str = 'neo-db'
    DB_PORT: int = 7687
    DB_USER: str = 'neo4j'
    DB_PASSWORD: str = 'aziz1234'

    @property
    def db_url(self):
        return f"neo4j://{self.DB_HOST}:{self.DB_PORT}"

app_config = AppConfig()
db_config = DataBaseConfig()
