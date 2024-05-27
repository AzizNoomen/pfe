from fastapi import APIRouter, Depends
from app.schemas.document_schema import DocumentSchema
from app.services import DocumentService
from typing import List

router = APIRouter()

@router.post("/documents/", response_model=DocumentSchema)
async def create_document(document: DocumentSchema, service: DocumentService = Depends()):
    return service.create_document(document)

@router.get("/documents/", response_model=List[DocumentSchema])
async def get_all_documents(service: DocumentService = Depends()):
    return service.get_all_documents()
