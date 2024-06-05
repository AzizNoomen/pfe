# app/repositories/ollama_repository.py
import os
import requests
import json

BASE_URL = os.environ.get('OLLAMA_HOST', 'http://host.docker.internal:11434')

class OllamaRepository:
    def generate_text(self, model_name, prompt, system=None, template=None, context=None, options=None):
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
            print(f"An error occurred: {e}")
            return None

    # Create a model from a Modelfile. Use the callback function to override the default handler.
    def create_model(self, model_name, model_path=None, callback=None):
        try:
            url = f"{BASE_URL}/api/create"
            payload = {"name": model_name, "path": model_path}
            
            # Making a POST request with the stream parameter set to True to handle streaming responses
            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()

                # Iterating over the response line by line and displaying the status
                for line in response.iter_lines():
                    if line:
                        # Parsing each line (JSON chunk) and extracting the status
                        chunk = json.loads(line)

                        if callback:
                            callback(chunk)
                        else:
                            print(f"Status: {chunk.get('status')}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    # Pull a model from a the model registry. Cancelled pulls are resumed from where they left off, and multiple
    # calls to will share the same download progress. Use the callback function to override the default handler.
    def pull_model(self, model_name, insecure=False, callback=None):
        try:
            url = f"{BASE_URL}/api/pull"
            payload = {
                "name": model_name,
                "insecure": insecure
            }

            # Making a POST request with the stream parameter set to True to handle streaming responses
            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()

                # Iterating over the response line by line and displaying the details
                for line in response.iter_lines():
                    if line:
                        # Parsing each line (JSON chunk) and extracting the details
                        chunk = json.loads(line)
                        # If a callback function is provided, call it with the chunk
                        if callback:
                            callback(chunk)
                        else:
                            # Print the status message directly to the console
                            print(chunk.get('status', ''), end='', flush=True)
                        
                        # If there's layer data, you might also want to print that (adjust as necessary)
                        if 'digest' in chunk:
                            print(f" - Digest: {chunk['digest']}", end='', flush=True)
                            print(f" - Total: {chunk['total']}", end='', flush=True)
                        if 'Compeletd' in chunk:
                            print(f" - Completed: {chunk['completed']}", end='\n', flush=True)
                        else:
                            print()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    # Push a model to the model registry. Use the callback function to override the default handler.
    def push_model(self, model_name, insecure=False, callback=None):
        try:
            url = f"{BASE_URL}/api/push"
            payload = {
                "name": model_name,
                "insecure": insecure
            }

            # Making a POST request with the stream parameter set to True to handle streaming responses
            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()

                # Iterating over the response line by line and displaying the details
                for line in response.iter_lines():
                    if line:
                        # Parsing each line (JSON chunk) and extracting the details
                        chunk = json.loads(line)

                        # If a callback function is provided, call it with the chunk
                        if callback:
                            callback(chunk)
                        else:
                            # Print the status message directly to the console
                            print(chunk.get('status', ''), end='', flush=True)
                        
                        # If there's layer data, you might also want to print that (adjust as necessary)
                        if 'digest' in chunk:
                            print(f" - Digest: {chunk['digest']}", end='', flush=True)
                            print(f" - Total: {chunk['total']}", end='', flush=True)
                            print(f" - Completed: {chunk['completed']}", end='\n', flush=True)
                        else:
                            print()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    # List models that are available locally.
    def list_models(self):
        try:
            response = requests.get(f"{BASE_URL}/api/tags")
            response.raise_for_status()
            data = response.json()
            models = data.get('models', [])
            print("available models \n",models)
            return models

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    # Copy a model. Creates a model with another name from an existing model.
    def copy_model(self, source, destination):
        try:
            # Create the JSON payload
            payload = {
                "source": source,
                "destination": destination
            }
            
            response = requests.post(f"{BASE_URL}/api/copy", json=payload)
            response.raise_for_status()
            
            # If the request was successful, return a message indicating that the copy was successful
            return "Copy successful"

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    # Delete a model and its data.
    def delete_model(self, model_name):
        try:
            url = f"{BASE_URL}/api/delete"
            payload = {"name": model_name}
            response = requests.delete(url, json=payload)
            response.raise_for_status()
            return "Delete successful"
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

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