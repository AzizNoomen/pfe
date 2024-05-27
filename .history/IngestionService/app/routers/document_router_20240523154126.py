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




@router.post("/documents", response_model=bool)
async def add_document(document: DocumentSchema, session: Session = Depends(get_session)):
    document_model = Document(**document.dict())
    return create_node(session, document_model)

@router.get("/documents", response_model=List[DocumentSchema])
async def get_documents(session: Session = Depends(get_session)):
    return fetch_all_nodes(session)
