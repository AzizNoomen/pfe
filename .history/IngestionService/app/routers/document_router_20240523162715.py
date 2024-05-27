from fastapi import APIRouter, Depends
from app.dependencies import get_db_session

router = APIRouter()

@router.post("/documents", response_model=DocumentSchema)
async def create_document(title: str, content: str, session: Session = Depends(get_db_session)):
    return document_service.create_document(title, content)

@router.get("/documents", response_model=List[DocumentSchema])
async def get_documents(session: Session = Depends(get_db_session)):
    return document_service.get_documents()
