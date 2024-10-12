from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Depends
from typing import List
from dependency_injector.wiring import Provide, inject
from configuration.injection_container import DependencyContainer
from app.services.ingestion_service import IngestionService
from app.schemas.ingestion_schemas import MessageResponse

router = APIRouter(prefix="/bff")

@router.post("/documents", response_model=MessageResponse)
@inject
async def upload_documents(
    files: List[UploadFile] = File(...),
    chunking_method:str = Query("regular"),
    model_name:str = Query("zephyr:latest"),
    ingestion_service: IngestionService = Depends(Provide[DependencyContainer.ingestion_service])):
    
    try:
        result = await ingestion_service.upload_documents(files, chunking_method, model_name)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
