import os
import requests
import json
from fastapi import HTTPException, status
from typing import Generator
from app.schemas.ollama_schema import GenericResponse, OllamaModelListResponse, ShowModelFullResponse

BASE_URL = os.environ.get('OLLAMA_HOST', 'http://ollama:11434')

import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaService:
    def generate_text(self, model_name: str, prompt: str, system: str = None, template: str = None, context: str = None, options: str = None) -> Generator[str, None, None]:
        models = self.list_models()

        # Check if the specified model_name exists in the list of models
        if any(model['name'] == model_name for model in models):
            try:
                url = f"{BASE_URL}/api/generate"
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
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model '{model_name}' doesn't exist, please specify the tag or change the model")

    def create_model(self, model_name: str, model_content: bytes) -> str:
        try:
            with open(f"{model_name}.txt", "wb") as file:
                file.write(model_content)

            return f"Model '{model_name}' created successfully"
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        
    def pull_model(self, model_name: str, insecure: bool = False) -> str:
        models = self.list_models()

        # Check if the specified model_name exists in the list of models
        if all(model['name'] != model_name for model in models):
            try:
                url = f"{BASE_URL}/api/pull"
                payload = {"name": model_name, "insecure": insecure}

                with requests.post(url, json=payload, stream=True) as response:
                    response.raise_for_status()

                    for line in response.iter_lines():
                        if line:
                            chunk = json.loads(line)
                            if 'Completed' in chunk:
                                print(f" - Completed: {chunk['Completed']}")
                                return f"Model '{model_name}' pulled successfully"
                        
            except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Model '{model_name}' already exists")

    def push_model(self, model_name: str, insecure: bool = False) -> str:
        models = self.list_models()

        # Check if the specified model_name exists in the list of models
        if all(model['name'] != model_name for model in models):
            try:
                url = f"{BASE_URL}/api/push"
                payload = {"name": model_name, "insecure": insecure}

                with requests.post(url, json=payload, stream=True) as response:
                    response.raise_for_status()

                    for line in response.iter_lines():
                        if line:
                            chunk = json.loads(line)
                            print(f"Status: {chunk.get('status')}")
                            return f"Model '{model_name}' pushed successfully"

            except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Model '{model_name}' already exists")

    def list_models(self) -> OllamaModelListResponse:
        try:
            response = requests.get(f"{BASE_URL}/api/tags")
            response.raise_for_status()
            data = response.json()
            return data.get('models', [])

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    def copy_model(self, source: str, destination: str) -> str:
        try:
            payload = {"source": source, "destination": destination}
            response = requests.post(f"{BASE_URL}/api/copy", json=payload)
            response.raise_for_status()
            return "Copy successful"

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    def delete_model(self, model_name: str) -> str:
        models = self.list_models()

        # Check if the specified model_name exists in the list of models
        if any(model['name'] == model_name for model in models):
            try:
                payload = {"name": model_name}
                response = requests.delete(f"{BASE_URL}/api/delete", json=payload)
                response.raise_for_status()
                return "Delete successful"

            except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model '{model_name}' doesn't exist, please specify the tag or change the model")

    def show_model(self, model_name: str) -> ShowModelFullResponse:
        models = self.list_models()

        # Check if the specified model_name exists in the list of models
        if any(model['name'] == model_name for model in models):
            try:
                url = f"{BASE_URL}/api/show"
                payload = {"name": model_name}
                response = requests.post(url, json=payload)
                response.raise_for_status()
                
                # Parse the JSON response and return it
                data = response.json()
                return data
            except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model '{model_name}' doesn't exist, please specify the tag or change the model")

    def check_ollama_health(self) -> str:
        try:
            url = f"{BASE_URL}/"
            response = requests.head(url)
            response.raise_for_status()
            return "Ollama is running"
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    def encode(self, prompt: str, model: str = "all-minilm") -> list:
        try:
            url = f"{BASE_URL}/api/embeddings"
            payload = {
                "model": model,
                "prompt": prompt
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
            embeddings = response.json()['embedding']
            return embeddings
        
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
