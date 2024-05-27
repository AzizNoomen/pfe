from neo4j import Session
from IngestionService.app.repositories.document_repository import DocumentRepository
from app.schemas.document_schema import DocumentSchema
from typing import List

class DocumentService:
    def __init__(self, session: Session):
        self.repository = DocumentRepository(session)

    def create_document(self, document_data: DocumentSchema) -> DocumentSchema:
        document = self.repository.create_document(document_data)
        return document

    def get_all_documents(self) -> List[DocumentSchema]:
        documents = self.repository.get_all_documents()
        return documents
