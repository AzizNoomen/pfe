from fastapi import APIRouter, Depends
from app.schemas.document_schema import DocumentSchema
from app.services.document_service import DocumentService
from typing import List
from neo4j import Session
from app.dependencies import get_db_session

router = APIRouter()

@router.post("/documents", response_model=DocumentSchema)
@inject
async def create_document(title: str, content: str, session: Session = Depends(get_db_session)):
    document_service = DocumentService(session)  # Pass the session to the DocumentService constructor
    return document_service.create_document(title, content)

@router.get("/documents", response_model=List[DocumentSchema])
async def get_documents(session: Session = Depends(get_db_session)):
    document_service = DocumentService(session)  # Pass the session to the DocumentService constructor
    return document_service.get_documents()
