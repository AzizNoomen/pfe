import os
import requests
import json
from fastapi import HTTPException
from typing import Generator
from app.exceptions.service_exceptions import InvalidModelFileException, ModelAlreadyExistsException, ModelNotFoundException
from app.schemas.ollama_schema import GenericResponse, OllamaModelListResponse, ShowModelFullResponse
from configuration.config import app_config
from configuration.logging import logger
from app.services.model_service import ModelService

class OllamaService(ModelService):

    def generate_text(self, model_name: str, prompt: str, system: str = None, template: str = None, context: str = None, options: str = None) -> Generator[str, None, None]:
        available_models = self.list_models()

        if not any(model['name'] == model_name for model in available_models):
            raise ModelNotFoundException(model_name)
        
        try:
            url = f"{app_config.BASE_URL}/api/generate"
            payload = {
                "model": model_name,
                "prompt": prompt,
                "system": system,
                "template": template,
                "context": context,
                "options": options
                }
            
            payload = {k: v for k, v in payload.items() if v is not None}

            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()
                full_response = ""

                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if not chunk.get("done"):
                            response_piece = chunk.get("response", "")
                            yield response_piece
                            full_response += response_piece
                return full_response

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        

    def create_model(self, model_name: str, model_content: bytes) -> str:
        if not model_name.endswith(".txt"):
            raise InvalidModelFileException(os.path.splitext(model_name)[1])
        
        try:
            with open(f"{model_name}.txt", "wb") as file:
                file.write(model_content)

            return f"Model '{model_name}' created successfully"
        
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        

    def pull_model(self, model_name: str, insecure: bool = False) -> str:
        available_models = self.list_models()

        if not all(model['name'] != model_name for model in available_models):
            raise ModelAlreadyExistsException(model_name)
        
        try:
            url = f"{app_config.BASE_URL}/api/pull"
            payload = {"name": model_name, "insecure": insecure}

            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if 'Completed' in chunk:
                            logger.info(f" - Completed: {chunk['Completed']}")
                            return f"Model '{model_name}' pulled successfully"
                        
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        


    def push_model(self, model_name: str, insecure: bool = False) -> str:
        
        try:
            url = f"{app_config.BASE_URL}/api/push"
            payload = {"name": model_name, "insecure": insecure}

            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        logger.info(f"Status: {chunk.get('status')}")
                        return f"Model '{model_name}' pushed successfully"

        except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        


    def list_models(self) -> OllamaModelListResponse:
        try:
            response = requests.get(f"{app_config.BASE_URL}/api/tags")
            response.raise_for_status()
            data = response.json()
            return data.get('models', [])

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


    def copy_model(self, source: str, destination: str) -> str:
        try:
            payload = {"source": source, "destination": destination}
            response = requests.post(f"{app_config.BASE_URL}/api/copy", json=payload)
            response.raise_for_status()
            return "Copy successful"

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


    def delete_model(self, model_name: str) -> str:
        available_models = self.list_models()

        if not any(model['name'] == model_name for model in available_models):
            raise ModelNotFoundException(model_name)
        
        try:
            payload = {"name": model_name}
            response = requests.delete(f"{app_config.BASE_URL}/api/delete", json=payload)
            response.raise_for_status()
            return "Delete successful"

        except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        

    def show_model(self, model_name: str) -> ShowModelFullResponse:
        available_models = self.list_models()

        if not any(model['name'] == model_name for model in available_models):
            raise ModelNotFoundException(model_name)
        
        try:
            url = f"{app_config.BASE_URL}/api/show"
            payload = {"name": model_name}
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data
        
        except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


    def check_ollama_health(self) -> str:
        try:
            url = f"{app_config.BASE_URL}/"
            response = requests.head(url)
            response.raise_for_status()
            return "Ollama is running"
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


    def encode(self, prompt: str, model_name: str = "all-minilm") -> list:
        available_models = self.list_models()

        if not any(model['name'] == model_name for model in available_models):
            raise ModelNotFoundException(model_name)
        
        try:
            url = f"{app_config.BASE_URL}/api/embeddings"
            payload = {
                "model": model_name,
                "prompt": prompt
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
            embeddings = response.json()
            return embeddings
        
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
