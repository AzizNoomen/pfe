from app.repositories import DocumentRepository
from app.exceptions.service_exceptions import DatabaseConnectionError
from uuid import UUID
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self):
        self.document_repository = DocumentRepository()

    def create(self, title: str, content: str):
        try:
            return self.document_repository.create(title, content)
        except DatabaseConnectionError as e:
            logger.error("Failed to create document: %s", e)
            return None

    def get_by_id(self, id):
        try:
            return self.document_repository.get_by_id(id)
        except DatabaseConnectionError as e:
            logger.error("Failed to fetch document by id: %s", e)
            return None

    def update(self, id, title: str, content: str):
        try:
            return self.document_repository.update(id, title, content)
        except DatabaseConnectionError as e:
            logger.error("Failed to update document: %s", e)
            # Handle the exception as needed, e.g., return None or raise a different exception
            return None

    def delete(self, id):
        try:
            self.document_repository.delete(id)
        except DatabaseConnectionError as e:
            logger.error("Failed to delete document: %s", e)
            # Handle the exception as needed, e.g., raise a different exception

    def get_all(self):
        try:
            return self.document_repository.get_all()
        except DatabaseConnectionError as e:
            logger.error("Failed to fetch all documents: %s", e)
            # Handle the exception as needed, e.g., return an empty list or raise a different exception
            return []