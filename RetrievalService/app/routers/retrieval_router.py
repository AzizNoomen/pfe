from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List

from fastapi.responses import JSONResponse
from app.services.retrieval_service import RetrievalService
from app.schemas.retrieval_schemas import RetrievalResult, HybridSearchResult
from dependency_injector.wiring import Provide, inject
from configuration.injection_container import DependencyContainer

router = APIRouter(prefix="/retrieval_service")

@router.get("/related-documents", response_model=List[HybridSearchResult])
@inject
async def retrieve(
    question: str = Query(...),
    model: str = Query("zephyr:latest"),
    top_n: int = Query(10),
    similarity_threshold: float = Query(0.5),
    reranker:str = Query(None),
    retrieval_service: RetrievalService = Depends(
        Provide[DependencyContainer.retrieval_service])):

    try:
        results = await retrieval_service.retrieve(question, model, top_n, similarity_threshold, reranker)
        return results.to_dict(orient='records')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents", response_model=List[RetrievalResult])
@inject
def get_all(retrieval_service: RetrievalService = Depends(
        Provide[DependencyContainer.retrieval_service])):
    
    try:
        results = retrieval_service.get_all()
        return results.to_dict(orient='records')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/graph", response_class=JSONResponse)
@inject
def get_graph(retrieval_service: RetrievalService = Depends(
        Provide[DependencyContainer.retrieval_service])):
    
    try:
        results = retrieval_service.get_graph()
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
