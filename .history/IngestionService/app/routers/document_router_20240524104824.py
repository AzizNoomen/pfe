from fastapi import APIRouter, Depends, APIRoute
from app.schemas.document_schema import DocumentSchema
from app.services.document_service import DocumentService
from typing import List
from app.dependencies import get_db_session
from neo4j import Session

router = APIRouter()

@router.post(path="/documents", response_model=DocumentSchema)
async def create_document(title: str, content: str, session: Session = Depends(get_db_session)):
    document_service = DocumentService(session)
    return document_service.create_document(title, content)

@router.get(path="/documents", response_model=List[DocumentSchema])
async def get_documents(session: Session = Depends(get_db_session)):
    document_service = DocumentService(session)
    return document_service.get_documents()

routes = [
    APIRoute("/documents", get_documents, methods=["GET"]),
    APIRoute("/documents", create_document, methods=["POST"])
]