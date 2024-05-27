from fastapi import APIRouter
from app.services.document_service import DocumentService
from app.schemas.document_schema import DocumentCreate, DocumentUpdate, Document

router = APIRouter()

# Initialize the DocumentService with a Neo4j session
# You can modify this to use a dependency injection or a connection pool
# to manage the Neo4j sessions
document_service = DocumentService(<NEO4J_SESSION_OBJECT>)

@router.post("/documents", response_model=Document)
async def create_document(document: DocumentCreate):
    """
    Create a new document
    """
    return await document_service.create_document(document)

@router.get("/documents", response_model=List[Document])
async def get_documents():
    """
    Get all documents
    """
    return await document_service.get_all_documents()

@router.get("/documents/{document_id}", response_model=Document)
async def get_document(document_id: str):
    """
    Get a document by ID
    """
    return await document_service.get_document_by_id(document_id)

@router.put("/documents/{document_id}", response_model=Document)
async def update_document(document_id: str, document: DocumentUpdate):
    """
    Update a document by ID
    """
    return await document_service.update_document_by_id(document_id, document)

@router.delete("/documents/{document_id}", response_model=Document)
async def delete_document(document_id: str):
    """
    Delete a document by ID
    """
    return await document_service.delete_document_by_id(document_id)
