from fastapi import APIRouter, HTTPException, Depends
from dependency_injector.wiring import Provide, inject
from fastapi.responses import JSONResponse
from configuration.injection_container import DependencyContainer
from app.services.graph_visualization_service import GraphVis

router = APIRouter(prefix="/bff")

@router.get("/graph", response_class=JSONResponse)
@inject
async def visualize(
    graph_service: GraphVis = Depends(Provide[DependencyContainer.graph_vis_service])):
    
    try:
        results = await graph_service.vis()
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
