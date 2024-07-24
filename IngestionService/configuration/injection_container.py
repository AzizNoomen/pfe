from dependency_injector import containers, providers
from configuration.config import DataBaseConfig
from app.helpers.db_helpers import DBHelper
from app.repositories.ingestion_repository import IngestionRepository
from app.services.ingestion_service import IngestionService

class DependencyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app"])

    database_config = providers.Singleton(DataBaseConfig)
    db_helpers = providers.Singleton(DBHelper, db_url=database_config.provided.db_url, user=database_config.provided.DB_USER, password=database_config.provided.DB_PASSWORD)

    ingestion_repository = providers.Factory(IngestionRepository, database_helper=db_helpers)

    ingestion_service = providers.Singleton(IngestionService, ingestion_repository = ingestion_repository)


