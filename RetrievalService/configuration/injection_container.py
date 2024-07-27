from dependency_injector import containers, providers
from configuration.config import DataBaseConfig
from app.helpers.db_helpers import DBHelper
from app.repositories.retrieval_repository import RetrievalRepository
from app.services.retrieval_service import RetrievalService

class DependencyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app"])

    database_config = providers.Singleton(DataBaseConfig)
    db_helpers = providers.Singleton(DBHelper, db_url=database_config.provided.db_url, user=database_config.provided.DB_USER, password=database_config.provided.DB_PASSWORD)

    retrieval_repository = providers.Factory(RetrievalRepository, database_helper=db_helpers)

    retrieval_service = providers.Singleton(RetrievalService, retrieval_repository = retrieval_repository)


