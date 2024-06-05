import os
import requests
import json
from fastapi import HTTPException

BASE_URL = os.environ.get('OLLAMA_HOST', 'http://host.docker.internal:11434')

class OllamaRepository:
    def generate_text(self, model_name:str, prompt:str, system=None, template=None, context=None, options=None):
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
                            full_response += response_piece

                return full_response

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    def create_model(self, model_name, model_path=None):
        try:
            url = f"{BASE_URL}/api/create"
            payload = {"name": model_name, "path": model_path}

            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        print(f"Status: {chunk.get('status')}")

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    def pull_model(self, model_name, insecure=False):
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

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    def push_model(self, model_name, insecure=False):
        try:
            url = f"{BASE_URL}/api/push"
            payload = {"name": model_name, "insecure": insecure}

            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        print(f"Status: {chunk.get('status')}")

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    def list_models(self):
        try:
            response = requests.get(f"{BASE_URL}/api/tags")
            response.raise_for_status()
            data = response.json()
            return data.get('models', [])

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    def copy_model(self, source, destination):
        try:
            payload = {"source": source, "destination": destination}
            response = requests.post(f"{BASE_URL}/api/copy", json=payload)
            response.raise_for_status()
            return "Copy successful"

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    def delete_model(self, model_name):
        try:
            payload = {"name": model_name}
            response = requests.delete(f"{BASE_URL}/api/delete", json=payload)
            response.raise_for_status()
            return "Delete successful"

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    # Show info about a model.
    def show_model(self, model_name):
        try:
            url = f"{BASE_URL}/api/show"
            payload = {"name": model_name}
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            # Parse the JSON response and return it
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        

    def heartbeat(self):
        try:
            url = f"{BASE_URL}/"
            response = requests.head(url)
            response.raise_for_status()
            return "Ollama is running"
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return "Ollama is not running"