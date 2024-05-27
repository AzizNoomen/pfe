from fastapi import APIRouter, Depends
from ..schemas import DocumentSchema
from ..services import DocumentService

router = APIRouter()

@router.post("/documents/", response_model=DocumentSchema)
def create_document(document: DocumentSchema, service: DocumentService = Depends()):
    return service.create_document(document)

@router.get("/documents/", response_model=List[DocumentSchema])
def get_all_documents(service: DocumentService = Depends()):
    return service.get_all_documents()
