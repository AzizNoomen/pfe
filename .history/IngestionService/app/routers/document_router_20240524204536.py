import logging
from fastapi import APIRouter, Depends
from app.schemas.document_schema import DocumentSchema
from app.services.document_service import DocumentService
from typing import List
from app.dependencies import get_db_session
from neo4j import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/documents", response_model=DocumentSchema)
async def create_document(document_data: DocumentSchema, session: Session = Depends(get_db_session)):
    logger.info("Creating a document with title: %s", document_data.title)
    document_service = DocumentService(session)
    result = document_service.create_document(document_data)
    return result


@router.get("/documents", response_model=List[DocumentSchema])
async def get_documents(session: Session = Depends(get_db_session)):
    logger.info("Fetching documents.")
    document_service = DocumentService(session)
    documents = document_service.get_documents()
    logger.info("Fetched %d documents.", len(documents))
    return documents
