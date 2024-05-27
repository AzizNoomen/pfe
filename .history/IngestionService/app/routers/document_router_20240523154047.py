from fastapi import APIRouter, Depends
from app.schemas.document_schema import DocumentSchema
from app.services.document_service import DocumentService
from typing import List

router = APIRouter()

@router.post("/documents/", response_model=DocumentSchema)
async def create_document(document: DocumentSchema, service: DocumentService = Depends()):
    return service.create_document(document)

@router.get("/documents/", response_model=List[DocumentSchema])
async def get_all_documents(service: DocumentService = Depends()):
    return service.get_all_documents()


from fastapi import APIRouter, Depends
from app.schemas.document_schema import DocumentSchema
from app.models.document_models import Document
from app.repositories.document_repository import create_node, fetch_all_nodes
from neo4j import GraphDatabase, Session
from typing import List

router = APIRouter()

# Neo4j connection details
NEO4J_URI = "bolt://neo4j:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

def get_session() -> Session:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    session = driver.session()
    try:
        yield session
    finally:
        session.close()

@router.post("/documents", response_model=bool)
async def add_document(document: DocumentSchema, session: Session = Depends(get_session)):
    document_model = Document(**document.dict())
    return create_node(session, document_model)

@router.get("/documents", response_model=List[DocumentSchema])
async def get_documents(session: Session = Depends(get_session)):
    return fetch_all_nodes(session)
