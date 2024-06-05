from app.repositories.ollama_repository import OllamaRepository

class OllamaService:
    def __init__(self):
        self.ollama_repository = OllamaRepository()

    def generate_text(self, model_name, prompt, system=None, template=None, context=None, options=None):
        return self.ollama_repository.generate_text(model_name, prompt, system, template, context, options)

    def create_model(self, model_name, model_path=None):
        return self.ollama_repository.create_model(model_name, model_path)

    def pull_model(self, model_name, insecure=False):
        return self.ollama_repository.pull_model(model_name, insecure)

    def push_model(self, model_name, insecure=False):
        return self.ollama_repository.push_model(model_name, insecure)

    def list_models(self):
        return self.ollama_repository.list_models()

    def copy_model(self, source, destination):
        return self.ollama_repository.copy_model(source, destination)

    def delete_model(self, model_name):
        return self.ollama_repository.delete_model(model_name)

    def show_model(self, model_name):
        return self.ollama_repository.show_model(model_name)

    def check_ollama_health(self):
        return self.ollama_repository.heartbeat()
