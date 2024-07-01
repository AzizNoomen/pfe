from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.services.retrieval_service import RetrievalService

router = APIRouter(prefix="/retrieval_service")
retrieval_service = RetrievalService()


@router.post("/retrieve")
async def retrieve(question: str, model: str = "zephyr:latest", top_n: int = 10, similarity_threshold: float = 0.5):
    try:
        results = await retrieval_service.retrieve(question, model, top_n, similarity_threshold)
        return results.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
