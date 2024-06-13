from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import List
from app.services.graph_service import GraphService
from pathlib import Path

router = APIRouter()
graph_service = GraphService()

@router.post("/upload_pdfs")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        df = graph_service.load_documents(files)
        dfg1 = await graph_service.generate_graph(df)
        dfg2 = graph_service.contextual_proximity(dfg1)
        dfg = graph_service.merge_relationships(dfg1, dfg2)
        await graph_service.contruct_graph(dfg)
        return {"message": "PDFs uploaded and graph created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

