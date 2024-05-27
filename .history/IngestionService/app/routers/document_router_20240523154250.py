from fastapi import APIRouter, Depends
from app.schemas.document_schema import DocumentSchema
from app.services.document_service import DocumentService
from typing import List
from fastapi import APIRouter, Depends
from app.schemas.document_schema import DocumentSchema
from app.models.document_models import Document
from app.repositories.document_repository import create_node, fetch_all_nodes
from neo4j import GraphDatabase, Session
from typing import List


router = APIRouter()



@router.post("/documents", response_model=bool)
async def add_document(document: DocumentSchema, session: Session = Depends()):
    document_model = Document(**document.dict())
    return create_node(session, document_model)

@router.get("/documents", response_model=List[DocumentSchema])
async def get_documents(session: Session = Depends()):
    return fetch_all_nodes(session)
