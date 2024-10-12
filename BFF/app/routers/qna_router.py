from fastapi import APIRouter, HTTPException, Depends, Query
from dependency_injector.wiring import Provide, inject
from configuration.injection_container import DependencyContainer
from app.services.qna_service import QnAService

router = APIRouter(prefix="/bff")

@router.get("/QnA", response_model=str)
@inject
async def retrieve(
    question: str = Query(...),
    retrieval_model: str = Query("zephyr:latest"),
    generation_model: str = Query("llama3:latest"),
    reranker:str = Query(None),
    qna_service: QnAService = Depends(Provide[DependencyContainer.qna_service])):
    
    try:
        results = await qna_service.retrieve(question, retrieval_model, reranker)
        answer = await qna_service.generate(question, results, generation_model)
        return answer
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
