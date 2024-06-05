from fastapi import APIRouter
from app.services.ollama_service import OllamaService

router = APIRouter()
ollama_service = OllamaService()

@router.post("/generate_text")
async def generate_text(model_name: str, prompt: str, system: str = None, template: str = None, context: str = None, options: str = None):
    response = ollama_service.generate_text(model_name, prompt, system, template, context, options)
    return {"response": response}

@router.post("/create_model")
async def create_model(model_name: str, model_path: str = None):
    response = ollama_service.create_model(model_name, model_path)
    return {"response": response}

@router.post("/pull_model")
async def pull_model(model_name: str, insecure: bool = False):
    response = ollama_service.pull_model(model_name, insecure)
    return {"response": response}

@router.post("/push_model")
async def push_model(model_name: str, insecure: bool = False):
    response = ollama_service.push_model(model_name, insecure)
    return {"response": response}

@router.get("/list_models")
async def list_models():
    response = ollama_service.list_models()
    return {"response": response}

@router.post("/copy_model")
async def copy_model(source: str, destination: str):
    response = ollama_service.copy_model(source, destination)
    return {"response": response}

@router.delete("/delete_model")
async def delete_model(model_name: str):
    response = ollama_service.delete_model(model_name)
    return {"response": response}

@router.get("/show_model")
async def show_model(model_name: str):
    response = ollama_service.show_model(model_name)
    return {"response": response}

@router.get("/check_ollama_health")
async def check_ollama_health():
    response = ollama_service.check_ollama_health()
    return {"response": response}
