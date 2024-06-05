from app.repositories.ollama_repository import OllamaRepository
from fastapi import HTTPException, status

class OllamaService:
    def __init__(self):
        self.ollama_repository = OllamaRepository()

    def generate_text(self, model_name, prompt, system=None, template=None, context=None, options=None):
        models = self.list_models()

        # Check if the specified model_name exists in the list of models
        if any(model['name'] == model_name for model in models):
            # Pull the model
            return self.ollama_repository.generate_text(model_name, prompt, system, template, context, options)
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model '{model_name}' doesn't exist, please specify the tag or change the model")

        
    def create_model(self, model_name, model_path=None):
        return self.ollama_repository.create_model(model_name, model_path)

    def pull_model(self, model_name: str, insecure: bool = False):
        models = self.list_models()

        # Check if the specified model_name exists in the list of models
        if all(model['name'] != model_name for model in models):
            # Pull the model
            return self.ollama_repository.pull_model(model_name, insecure)
        
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Model '{model_name}' already exists")


    def push_model(self, model_name, insecure=False):
        models = self.list_models()

        # Check if the specified model_name exists in the list of models
        if all(model['name'] != model_name for model in models):
            # Pull the model
            return self.ollama_repository.push_model(model_name, insecure)
        
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Model '{model_name}' already exists")
        

    def list_models(self):
        return self.ollama_repository.list_models()

    def copy_model(self, source, destination):
        return self.ollama_repository.copy_model(source, destination)

    def delete_model(self, model_name):
        models = self.list_models()

        # Check if the specified model_name exists in the list of models
        if any(model['name'] == model_name for model in models):
            # Pull the model
            return self.ollama_repository.delete_model(model_name)
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model '{model_name}' doesn't exist, please specify the tag or change the model")


    def show_model(self, model_name):
        models = self.list_models()

        # Check if the specified model_name exists in the list of models
        if any(model['name'] == model_name for model in models):
            # Pull the model
            return self.ollama_repository.show_model(model_name)
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model '{model_name}' doesn't exist, please specify the tag or change the model")
        

    def check_ollama_health(self):
        return self.ollama_repository.heartbeat()
