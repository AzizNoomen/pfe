import logging
from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.schemas import DocumentSchema, DocumentCreateSchema, DocumentUpdateSchema
from app.services import DocumentService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


document_service = DocumentService()
router = APIRouter()

@router.post("/documents/", response_model=DocumentSchema)
def create_document(document: DocumentCreateSchema):
    created_document = document_service.create(title=document.title, content=document.content)
    if created_document:
        return created_document
    raise HTTPException(status_code=500, detail="Document could not be created")

@router.get("/documents/{id}", response_model=DocumentSchema)
def get_document(id: UUID):
    document = document_service.get_by_id(id)
    if document:
        return document
    raise HTTPException(status_code=404, detail="Document not found")

@router.put("/documents/{id}", response_model=DocumentSchema)
def update_document(id: UUID, document: DocumentUpdateSchema):
    existing_document = document_service.get_by_id(id)
    if not existing_document:
        raise HTTPException(status_code=404, detail="Document not found")

    updated_document = document_service.update(
        id=id,
        title=document.title or existing_document.title, 
        content=document.content or existing_document.content
    )
    if updated_document:
        return updated_document
    raise HTTPException(status_code=500, detail="Document could not be updated")

@router.delete("/documents/{id}", response_model=dict)
def delete_document(id: UUID):
    existing_document = document_service.get_by_id(id)
    if not existing_document:
        raise HTTPException(status_code=404, detail="Document not found")

    document_service.delete(id)
    return {"message": "Document deleted successfully"}