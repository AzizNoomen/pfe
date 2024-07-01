from fastapi import APIRouter, File, UploadFile, Body
import logging
from fastapi.responses import StreamingResponse
from app.services.ollama_service import OllamaService
from app.schemas.ollama_schema import (
    EncodeRequest,
    OllamaModelListResponse,
    GenericResponse,
    ShowModelFullResponse,
    GenerateTextRequest
)

router = APIRouter(prefix="/ollama")
ollama_service = OllamaService()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/generate_text", response_model=GenericResponse)
async def generate_text(request_body: GenerateTextRequest = Body(...)):
    logger.info("Generate text endpoint reached successfully")
    response = ollama_service.generate_text(**request_body.dict())
    return StreamingResponse(response, media_type="text/plain")

@router.post("/create_model", response_model=GenericResponse)
async def create_model(model_name: str, model_file: UploadFile = File(...)):
    model_content = await model_file.read()
    response = ollama_service.create_model(model_name, model_content)
    return {"response": response}

@router.post("/pull_model", response_model=GenericResponse)
async def pull_model(model_name: str, insecure: bool = False):
    response = ollama_service.pull_model(model_name, insecure)
    return {"response": response}

@router.post("/push_model", response_model=GenericResponse)
async def push_model(model_name: str, insecure: bool = False):
    response = ollama_service.push_model(model_name, insecure)
    return {"response": response}

@router.get("/list_models", response_model=OllamaModelListResponse)
async def list_models():
    response = ollama_service.list_models()
    return {"response": response}

@router.post("/copy_model", response_model=GenericResponse)
async def copy_model(source: str, destination: str):
    response = ollama_service.copy_model(source, destination)
    return {"response": response}

@router.delete("/delete_model", response_model=GenericResponse)
async def delete_model(model_name: str):
    response = ollama_service.delete_model(model_name)
    return {"response": response}

@router.get("/show_model", response_model=ShowModelFullResponse)
async def show_model(model_name: str):
    response = ollama_service.show_model(model_name)
    return {"response": response}

@router.get("/check_ollama_health", response_model=GenericResponse)
async def check_ollama_health():
    response = ollama_service.check_ollama_health()
    return {"response": response}

@router.post("/encode", response_model=list)
async def encode(request_body: EncodeRequest = Body(...)):
    response = ollama_service.encode(**request_body.dict())
    return response