from app.schemas.document_schema import DocumentSchema
from app.repositories import DocumentRepository
from uuid import UUID

class DocumentService:
    def __init__(self):
        self.document_repository = DocumentRepository()

    def create(self, title, content):
        return self.document_repository.create(title, content)

    def get_by_id(self, id: UUID):
        return self.document_repository.get_by_id(id)

    def update(self, id: UUID, title, content):
        return self.document_repository.update(id, title, content)

    def delete(self, id: UUID):
        return self.document_repository.delete(id)

    def get_all(self):
        return  self.document_repository.get_all()