from fastapi import APIRouter, HTTPException, File, UploadFile, Depends, Query
from typing import List
from app.schemas.ingestion_schemas import MessageResponse
from app.services.ingestion_service import IngestionService
from dependency_injector.wiring import Provide, inject
from configuration.injection_container import DependencyContainer

router = APIRouter(prefix="/ingestion_service")

@router.post("/documents", response_model=MessageResponse)
@inject
async def upload_documents(
    files: List[UploadFile] = File(...),
    chunking_method:str = Query("regular"),
    ingestion_service: IngestionService = Depends(
        Provide[DependencyContainer.ingestion_service])):
    
    try:
        await ingestion_service.ingest(files, chunking_method)
        return MessageResponse(message="Documents uploaded and graph created successfully")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents", response_model=MessageResponse)
@inject
def delete_all(ingestion_service: IngestionService = Depends(
        Provide[DependencyContainer.ingestion_service])):
    
    try:
        ingestion_service.delete_all()
        return MessageResponse(message="Graph deleted successfully")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))