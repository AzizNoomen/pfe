from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import List
from app.models.graph_models import Node, Edge
from app.schemas.graph_schemas import GraphResponse
from app.services.graph_service import GraphService
from pathlib import Path

router = APIRouter()
graph_service = GraphService()

@router.post("/graph", response_model=GraphResponse)
async def create_graph(nodes: List[Node], edges: List[Edge]):
    try:
        await graph_service.create_graph(nodes, edges)
        return GraphResponse(message="Graph created successfully", nodes_added=len(nodes), edges_added=len(edges))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload_pdfs")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        output_directory = Path("C:/Users/azizn/OneDrive - s7syh/Documents/ELYADATA/Projet Implementation/IngestionService/app/data_output")
        await graph_service.create_graph_from_files(files, output_directory)
        return {"message": "PDFs uploaded and graph created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

