from typing import Any, Dict, List
from fastapi import APIRouter, Body, HTTPException, Depends, Query
from dependency_injector.wiring import Provide, inject
from configuration.injection_container import DependencyContainer
from app.services.generation_service import GenerationService
from app.schemas.generation_schemas import GenerationResponse

router = APIRouter(prefix="/generation_service")

@router.post("/answer", response_model=GenerationResponse)
@inject
async def generate_response(
    question: str = Query(...),
    model_name: str = Query("zephyr:latest"),
    results: List[Dict[str, Any]] = Body(...),
    generation_service: GenerationService = Depends(Provide[DependencyContainer.generation_service])):
    
    try:
        response = await generation_service.generate(question, results, model_name)
        return GenerationResponse(answer=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
