from fastapi import APIRouter, Depends, File, UploadFile, Body, status, Query
from app.exceptions.api_exception_handler import APIRequestException
from configuration.dependencies import DependencyContainer
from app.services.ollama_service import OllamaService
from fastapi.responses import StreamingResponse
from dependency_injector.wiring import Provide, inject
from app.schemas.ollama_schema import (EncodeRequest, EncodeResponse, OllamaModelListResponse, GenericResponse, ShowModelFullResponse, GenerateTextRequest)

router = APIRouter(prefix="/ollama")

@router.post("/text-generation", response_model=GenericResponse)
@inject
def generate_text(request_body: GenerateTextRequest = Body(...),
                ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])
                ):
    try:
        response = ollama_service.generate_text(**request_body.dict())
        return StreamingResponse(response, media_type="text/plain")
    
    except ValueError as value_error:
        raise APIRequestException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(value_error))


@router.post("/create-model", response_model=GenericResponse)
@inject
def create_model(model_name: str = Query(...),
                model_file: UploadFile = File(...),
                ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])
                ):
    try:
        model_content = model_file.read()
        response = ollama_service.create_model(model_name, model_content)
        return {"response": response}
    
    except ValueError as value_error:
        raise APIRequestException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(value_error))


@router.post("/pull-model", response_model=GenericResponse)
@inject
def pull_model(model_name: str = Query(...),
                insecure: bool = Query(False),
                ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])
                ):
    try:
        response = ollama_service.pull_model(model_name, insecure)
        return {"response": response}
    
    except ValueError as value_error:
        raise APIRequestException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(value_error))


@router.post("/push-model", response_model=GenericResponse)
@inject
def push_model(model_name: str = Query(...),
                insecure: bool = Query(False),
                ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])
                ):
    try:
        response = ollama_service.push_model(model_name, insecure)
        return {"response": response}
    
    except ValueError as value_error:
        raise APIRequestException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(value_error))


@router.get("/models", response_model=OllamaModelListResponse)
@inject
def list_models(ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])):
    try:
        response = ollama_service.list_models()
        return {"response": response}

    except ValueError as value_error:
        raise APIRequestException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(value_error))


@router.post("/copy-model", response_model=GenericResponse)
@inject
def copy_model(source: str = Query(...),
                destination: str = Query(...),
                ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])
                ):
    try:
        response = ollama_service.copy_model(source, destination)
        return {"response": response}
    
    except ValueError as value_error:
        raise APIRequestException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(value_error))


@router.delete("/model", response_model=GenericResponse)
@inject
def delete_model(model_name: str = Query(...),
                ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])
                ):
    try:
        response = ollama_service.delete_model(model_name)
        return {"response": response}
    
    except ValueError as value_error:
        raise APIRequestException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(value_error))


@router.get("/model", response_model=ShowModelFullResponse)
@inject
def show_model(model_name: str = Query(...),
                ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])
                ):
    try:
        response = ollama_service.show_model(model_name)
        return {"response": response}
    
    except ValueError as value_error:
        raise APIRequestException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(value_error))


@router.get("/ollama-health", response_model=GenericResponse)
@inject
def check_ollama_health(ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])):
    response = ollama_service.check_ollama_health()
    return {"response": response}
    

@router.post("/encode", response_model=EncodeResponse)
@inject
def encode(request_body: EncodeRequest = Body(...),
            ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])):
    try:
        response = ollama_service.encode(**request_body.dict())
        return response
    
    except ValueError as value_error:
        raise APIRequestException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(value_error))