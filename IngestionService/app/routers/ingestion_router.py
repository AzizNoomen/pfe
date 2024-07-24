from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from typing import List
from app.services.ingestion_service import IngestionService
from dependency_injector.wiring import Provide, inject
from configuration.injection_container import DependencyContainer

router = APIRouter(prefix="/ingestion_service")

@router.post("/documents")
@inject
async def upload_documents(
    files: List[UploadFile] = File(...),
    chunking_method:str = "regular",
    ingestion_service: IngestionService = Depends(
        Provide[DependencyContainer.ingestion_service])):
    try:
        documents = ingestion_service.load_documents(files)
        df = ingestion_service.chunking(documents,chunking_method)
        dfg1 = await ingestion_service.generate_graph(df)
        dfg2 = ingestion_service.contextual_proximity(dfg1)
        dfg = ingestion_service.merge_relationships(dfg1, dfg2)
        await ingestion_service.contruct_graph(dfg)
        await ingestion_service.merge_nodes()
        return {"message": "Documents uploaded and graph created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_all")
@inject
def delete_all(ingestion_service: IngestionService = Depends(
        Provide[DependencyContainer.ingestion_service])):
    try:
        ingestion_service.delete_all()
        return {"message": "Graph deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))