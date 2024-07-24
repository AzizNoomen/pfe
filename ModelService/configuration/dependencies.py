from dependency_injector import containers, providers
from app.services.ollama_service import OllamaService

class DependencyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app"])
    ollama_service = providers.Singleton(OllamaService)
