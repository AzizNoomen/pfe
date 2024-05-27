from fastapi import APIRouter
from app.schemas.document_schema import DocumentSchema
from app.services.document_service import DocumentService

router = APIRouter()

document_service = DocumentService()

@router.post("/documents", response_model=DocumentSchema)
async def create_document(title: str, content: str):
    return document_service.create_document(title, content)

@router.get("/documents", response_model=List[DocumentSchema])
async def get_documents():
    return document_service.get_documents()
