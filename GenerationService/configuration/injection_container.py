from dependency_injector import containers, providers
from app.services.generation_service import GenerationService

class DependencyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app"])
    generation_service = providers.Singleton(GenerationService)
