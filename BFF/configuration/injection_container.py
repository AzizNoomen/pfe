from dependency_injector import containers, providers
from app.services.ingestion_service import IngestionService
from app.services.qna_service import QnAService
from app.services.graph_visualization_service import GraphVis

class DependencyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app"])

    ingestion_service = providers.Singleton(IngestionService)
    qna_service = providers.Singleton(QnAService)
    graph_vis_service = providers.Singleton(GraphVis)


