# services/model_service.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class ModelService(ABC):
    @abstractmethod
    def generate_text(self, model_name: str, prompt: str, system: str = None, template: str = None, context: List[int] = None, options: Dict[str, Any] = None) -> List[str]:
        pass
    
    @abstractmethod
    def create_model(self, model_name: str, model_content: bytes) -> str:
        pass
    
    @abstractmethod
    def pull_model(self, model_name: str, insecure: bool = False) -> str:
        pass
    
    @abstractmethod
    def push_model(self, model_name: str, insecure: bool = False) -> str:
        pass
    
    @abstractmethod
    def list_models(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def copy_model(self, source: str, destination: str) -> str:
        pass
    
    @abstractmethod
    def delete_model(self, model_name: str) -> str:
        pass
    
    @abstractmethod
    def show_model(self, model_name: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def check_ollama_health(self) -> str:
        pass
    
    @abstractmethod
    def encode(self, model_name: str, prompt: str) -> List[float]:
        pass
